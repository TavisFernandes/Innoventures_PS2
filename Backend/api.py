"""
Flask API for PlugMind: chat endpoint + intent-based plugin suggestion (hot-swap).
"""
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv(Path(__file__).resolve().parent / ".env")
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Plugin IDs that match frontend plugins.ts
PLUGIN_IDS = ["default", "legal", "medical", "finance", "engineering", "hr", "cybersecurity"]

# Keyword hints per domain for intent classification (hot-swap)
INTENT_KEYWORDS = {
    "legal": [
        "contract", "nda", "compliance", "gdpr", "cease and desist", "clause", "liability",
        "legal", "law", "lawyer", "attorney", "court", "litigation", "agreement", "terms", "legal advice",
        "intellectual property", "copyright", "trademark", "patent", "regulation", "statute",
    ],
    "finance": [
        "stock", "stocks", "market", "trading", "portfolio", "investment", "invest", "shares", "equity", "bull", "bear",
        "finance", "financial", "revenue", "profit", "etf", "mutual fund", "rate", "interest",
        "budget", "roi", "valuation", "dividend", "balance sheet", "cash flow", "forex",
        "loan", "loans", "borrow", "lend", "approval", "credit", "get loan", "take loan", "loan amount", "how much",
    ],
    "medical": [
        "medical", "health", "drug", "medication", "diagnosis", "symptom", "treatment", "clinical",
        "patient", "doctor", "hospital", "lab", "prescription", "interaction", "therapy",
    ],
    "engineering": [
        "architecture", "code", "debug", "api", "database", "ci/cd", "system design", "optimization",
        "engineering", "technical", "algorithm", "backend", "frontend", "deployment",
    ],
    "hr": [
        "hr", "human resources", "employee", "onboarding", "performance review", "hiring",
        "recruitment", "policy", "workforce", "attrition", "engagement", "talent",
    ],
    "cybersecurity": [
        "security", "cyber", "vulnerability", "threat", "incident response", "cve", "firewall",
        "encryption", "breach", "mitre", "attack",
    ],
}


def classify_plugin_from_message(message: str) -> str:
    """Classify user message to suggest best plugin (for hot-swap). Returns plugin id."""
    if not message or not message.strip():
        return "default"
    text = message.lower().strip()
    # Count matches per domain
    scores = {}
    for plugin_id, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for k in keywords if k in text or re.search(rf"\b{re.escape(k)}\b", text))
        if score > 0:
            scores[plugin_id] = score
    if not scores:
        return "default"
    return max(scores, key=scores.get)


def query_openrouter(user_message: str, system_prompt: str, api_key: str, max_tokens: int = 1200):
    """Call OpenRouter chat completions."""
    import requests
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.5,
    }
    resp = requests.post(api_url, headers=headers, json=data, timeout=30)
    if resp.status_code != 200:
        return None
    try:
        return resp.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return None


# Generic, short replies for greetings and out-of-domain chat (no plugin needed)
GENERIC_GREETING_REPLIES = {
    "hi": "I'm fine, thanks! How can I help you today?",
    "hello": "Hello! How can I assist you?",
    "hey": "Hey! What can I do for you?",
    "how are you": "I am fine, thank you! How can I help you?",
    "how do you do": "I'm doing well, thanks. How can I assist you?",
    "good morning": "Good morning! How can I help you today?",
    "good afternoon": "Good afternoon! What can I do for you?",
    "good evening": "Good evening! How can I assist you?",
    "what's up": "All good! How can I help?",
    "hey there": "Hi there! What can I do for you?",
}


def is_generic_greeting(message: str) -> bool:
    """True if the message is a simple greeting or casual chat (out of plugins)."""
    text = message.lower().strip()
    if not text or len(text) > 120:
        return False
    if text in GENERIC_GREETING_REPLIES:
        return True
    words = text.split()
    if len(words) > 6:
        return False
    greeting_words = {"hi", "hello", "hey", "how", "are", "you", "good", "morning", "afternoon", "evening", "whats", "up", "there", "doing"}
    return bool(set(words) & greeting_words)


def get_generic_reply(message: str) -> str | None:
    """Return a short generic reply for greetings, or None to use LLM."""
    text = message.lower().strip()
    if text in GENERIC_GREETING_REPLIES:
        return GENERIC_GREETING_REPLIES[text]
    if is_generic_greeting(text):
        if "how are you" in text or "how are u" in text:
            return "I am fine. How can I help you today?"
        return "I'm doing well, thanks! How can I help you today?"
    return None


# System prompts — clear, structured, helpful responses
SYSTEM_PROMPTS = {
    "default": "You are a friendly, helpful assistant. For greetings and casual chat, reply in one short sentence. For general questions, give clear, accurate answers with a few sentences or bullet points where helpful. Be concise but complete.",
    "legal": "You are a Legal Expert AI. Give clear, well-structured answers. Explain legal concepts in plain language, use short paragraphs or bullet points, and include practical takeaways. Always end with a brief disclaimer that your response does not constitute legal advice and that users should consult a qualified attorney for their situation.",
    "medical": "You are a Medical Advisor AI. Give clear, evidence-based explanations. Use plain language and structure (e.g. short paragraphs or bullet points). Always remind users to consult a healthcare professional for personal medical decisions.",
    "finance": "You are a Financial Strategist AI. Give clear, structured answers with definitions, examples, and practical implications where relevant. Use bullet points or short paragraphs. Add a brief disclaimer that this is informational and not investment advice.",
    "engineering": "You are an Engineering Lead AI. Give clear technical explanations with structure (steps, options, tradeoffs). Use bullet points or short paragraphs. Be precise and practical.",
    "hr": "You are an HR Specialist AI. Give clear, actionable guidance. Use structure (bullet points or short paragraphs) and include practical examples or templates where helpful.",
    "cybersecurity": "You are a Cybersecurity Analyst AI. Give clear, structured answers: explain the issue, risks, and recommended actions. Use bullet points or short paragraphs. Be practical and precise.",
}


@app.route("/api/chat", methods=["POST"])
def chat():
    """Accept user message; return AI reply and suggestedPluginId for hot-swap."""
    try:
        body = request.get_json() or {}
        message = (body.get("message") or "").strip()
        current_plugin_id = (body.get("currentPluginId") or "default").strip() or "default"

        if not message:
            return jsonify({"error": "message is required"}), 400

        # Intent-based plugin suggestion (hot-swap) — chatbot automatically chooses plugin
        suggested_plugin_id = classify_plugin_from_message(message)
        if suggested_plugin_id not in PLUGIN_IDS:
            suggested_plugin_id = "default"

        # Out-of-domain: generic answers for greetings / casual chat (no specialist plugin)
        if suggested_plugin_id == "default":
            generic = get_generic_reply(message)
            if generic is not None:
                return jsonify({
                    "reply": generic,
                    "suggestedPluginId": "default",
                })

        # Finance plugin: loan approval (logistic regression) or stock/investment guidance
        if suggested_plugin_id == "finance":
            try:
                from loan_approval import (
                    is_loan_related,
                    loan_assessment_reply,
                    get_required_loan_fields_message,
                )
            except ImportError:
                pass
            else:
                if is_loan_related(message):
                    try:
                        t = message.lower().strip()
                        if any(
                            phrase in t
                            for phrase in (
                                "i don't have", "i do not have", "i can't provide", "i cannot provide",
                                "don't have that", "can't provide", "unable to provide", "insufficient",
                            )
                        ):
                            reply = (
                                "**Insufficient data.** Without your applicant income, loan amount, "
                                "loan term, and credit history, I cannot run the loan approval model. "
                                "Please provide these when you have them, or ask a lender directly."
                            )
                        else:
                            collected = body.get("collected_loan_data")
                            if isinstance(collected, dict):
                                collected = {k: v for k, v in collected.items() if v is not None}
                            reply, _ = loan_assessment_reply(message, collected if collected else None)
                        return jsonify({"reply": reply, "suggestedPluginId": "finance"})
                    except Exception:
                        pass
                # Stock / investment: portfolio risk guidance for "how much to invest" / stocks
                t = message.lower()
                if any(w in t for w in ("how much", "invest", "portfolio", "allocation", "diversif", "stocks")):
                    try:
                        from stock_predictor import get_portfolio_risk
                        portfolio_value = 0
                        for m in re.finditer(r"\$?\s*([\d,]+(?:\.\d+)?)\s*k?", message):
                            try:
                                v = float(m.group(1).replace(",", ""))
                                if "k" in message[max(0, m.start() - 2) : m.end() + 2].lower():
                                    v *= 1000
                                if v > portfolio_value:
                                    portfolio_value = v
                            except ValueError:
                                pass
                        risk_result = get_portfolio_risk({
                            "total_value": portfolio_value or 10000,
                            "largest_holding_pct": 0.25,
                            "diversification_score": 0.5,
                        })
                        recs = risk_result.get("recommendations", [])
                        reply = (
                            "**Investment guidance (Finance Plugin):**\n\n"
                                + (("\n".join("• " + r for r in recs) + "\n\n") if recs else "")
                                + "Only invest what you can afford to lose. "
                                "Diversify across assets and time (e.g. dollar-cost averaging). "
                                "This is not investment advice; consider a financial advisor."
                            )
                        return jsonify({"reply": reply, "suggestedPluginId": "finance"})
                    except Exception:
                        pass
            # Fall through to LLM for other finance questions

        system_prompt = SYSTEM_PROMPTS.get(suggested_plugin_id, SYSTEM_PROMPTS["default"])
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            reply = (
                f"I would answer as the **{suggested_plugin_id}** expert, but OPENROUTER_API_KEY is not set. "
                "Set it in the Backend .env to enable live AI responses."
            )
        else:
            content = query_openrouter(message, system_prompt, api_key)
            reply = content if content else "I couldn't generate a response. Please try again."

        return jsonify({
            "reply": reply,
            "suggestedPluginId": suggested_plugin_id,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

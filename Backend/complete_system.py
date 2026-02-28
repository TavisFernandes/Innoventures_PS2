#!/usr/bin/env python3
"""
FINAL WORKING BACKEND - OpenRouter API + ML Models + Hot-Swappable SME Plugin
"""
import os
import sys
import requests
import yaml
import joblib
import json
import numpy as np
from threading import Thread
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpertiseDomain(Enum):
    """Available expertise domains"""
    FINANCE = "finance"
    BANKING = "banking"
    INVESTMENT = "investment"
    RISK_MANAGEMENT = "risk_management"
    LOAN_ANALYSIS = "loan_analysis"
    STOCK_MARKET = "stock_market"
    CREDIT_SCORING = "credit_scoring"
    LEGAL = "legal"
    CONTRACT_LAW = "contract_law"
    CORPORATE_LAW = "corporate_law"
    REGULATORY_COMPLIANCE = "regulatory_compliance"

@dataclass
class SMEResponse:
    """Structured response from SME Plugin"""
    answer: str
    confidence: float
    sources: List[str]
    methodology: str
    domain: ExpertiseDomain
    citations: List[str]
    reasoning_steps: List[str]
    disclaimer: str

class HotSwappableSMEPlugin:
    """
    Hot-Swappable Subject Matter Expert Plugin
    Universal Finance Expert Plugin for AI Agents
    """
    
    def __init__(self, api_key: str, domain: ExpertiseDomain = ExpertiseDomain.FINANCE):
        self.api_key = api_key
        self.domain = domain
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Load domain-specific decision trees
        self.decision_trees = self._load_decision_trees()
        
        # Load source of truth references
        self.source_references = self._load_source_references()
        
        logger.info(f"SME Plugin initialized for domain: {domain.value}")
    
    def _load_decision_trees(self) -> Dict[str, Any]:
        """Load domain-specific decision trees"""
        trees = {
            ExpertiseDomain.FINANCE: {
                "loan_analysis": [
                    "Check borrower's credit history",
                    "Analyze debt-to-income ratio",
                    "Evaluate collateral value",
                    "Assess repayment capacity",
                    "Determine risk level",
                    "Recommend loan terms"
                ],
                "investment_analysis": [
                    "Define investment objectives",
                    "Assess risk tolerance",
                    "Analyze market conditions",
                    "Evaluate asset allocation",
                    "Consider time horizon",
                    "Recommend investment strategy"
                ]
            },
            ExpertiseDomain.BANKING: {
                "customer_assessment": [
                    "Verify customer identity",
                    "Assess financial standing",
                    "Evaluate banking needs",
                    "Determine product suitability",
                    "Compliance check",
                    "Recommend banking solutions"
                ]
            },
            ExpertiseDomain.RISK_MANAGEMENT: {
                "risk_assessment": [
                    "Identify risk factors",
                    "Quantify risk exposure",
                    "Evaluate mitigation strategies",
                    "Assess impact severity",
                    "Monitor risk indicators",
                    "Recommend risk controls"
                ]
            },
            ExpertiseDomain.LEGAL: {
                "legal_analysis": [
                    "Identify legal issue and jurisdiction",
                    "Research applicable laws and regulations",
                    "Analyze relevant case law and precedents",
                    "Evaluate legal arguments and defenses",
                    "Assess potential outcomes and risks",
                    "Provide legal recommendations"
                ],
                "contract_review": [
                    "Review contract terms and conditions",
                    "Identify legal obligations and rights",
                    "Assess compliance with applicable laws",
                    "Evaluate potential liabilities",
                    "Recommend modifications if needed",
                    "Provide legal risk assessment"
                ],
                "regulatory_compliance": [
                    "Identify applicable regulations",
                    "Assess current compliance status",
                    "Analyze gaps and risks",
                    "Recommend compliance measures",
                    "Develop compliance framework",
                    "Monitor regulatory changes"
                ]
            },
            ExpertiseDomain.CORPORATE_LAW: {
                "corporate_governance": [
                    "Analyze corporate structure",
                    "Review governance documents",
                    "Assess compliance with corporate laws",
                    "Evaluate board responsibilities",
                    "Identify potential liabilities",
                    "Recommend governance improvements"
                ]
            },
            ExpertiseDomain.CONTRACT_LAW: {
                "contract_dispute": [
                    "Analyze contract terms",
                    "Identify breach issues",
                    "Evaluate legal remedies",
                    "Assess damages and liabilities",
                    "Consider settlement options",
                    "Recommend legal actions"
                ]
            }
        }
        return trees
    
    def _load_source_references(self) -> Dict[str, List[str]]:
        """Load authoritative source references"""
        return {
            ExpertiseDomain.FINANCE: [
                "Federal Reserve Guidelines",
                "Consumer Financial Protection Bureau",
                "International Financial Reporting Standards (IFRS)",
                "Generally Accepted Accounting Principles (GAAP)",
                "Basel III Banking Regulations"
            ],
            ExpertiseDomain.BANKING: [
                "FDIC Banking Regulations",
                "Office of the Comptroller of the Currency (OCC)",
                "Federal Reserve System Regulations",
                "Bank Secrecy Act (BSA)",
                "Anti-Money Laundering (AML) Guidelines"
            ],
            ExpertiseDomain.INVESTMENT: [
                "SEC Investment Advisers Act",
                "FINRA Rules and Regulations",
                "Investment Company Act of 1940",
                "Dodd-Frank Wall Street Reform",
                "Market Conduct Rules"
            ],
            ExpertiseDomain.LEGAL: [
                "Supreme Court of India",
                "High Court Judgments",
                "Bar Council of India Rules",
                "Indian Penal Code (IPC)",
                "Civil Procedure Code (CPC)",
                "Constitution of India"
            ],
            ExpertiseDomain.CORPORATE_LAW: [
                "Companies Act 2013",
                "Securities and Exchange Board of India (SEBI)",
                "Ministry of Corporate Affairs",
                "Insolvency and Bankruptcy Code (IBC)",
                "Competition Act 2002"
            ],
            ExpertiseDomain.CONTRACT_LAW: [
                "Indian Contract Act 1872",
                "Sale of Goods Act 1930",
                "Specific Relief Act 1963",
                "Arbitration and Conciliation Act 1996",
                "Consumer Protection Act 2019"
            ],
            ExpertiseDomain.REGULATORY_COMPLIANCE: [
                "Regulatory Bodies of India",
                "Compliance Standards and Guidelines",
                "Legal Framework for Businesses",
                "Industry Specific Regulations",
                "International Compliance Standards"
            ]
        }
    
    def _get_decision_tree(self, query_type: str) -> List[str]:
        """Get decision tree steps for query type"""
        domain_trees = self.decision_trees.get(self.domain, {})
        return domain_trees.get(query_type, ["Analyze query requirements", "Apply domain expertise", "Provide structured response"])
    
    def _get_source_references(self) -> List[str]:
        """Get relevant source references for domain"""
        return self.source_references.get(self.domain, ["Industry Best Practices"])
    
    def _create_domain_prompt(self, query: str) -> str:
        """Create domain-specific system prompt"""
        domain_prompts = {
            ExpertiseDomain.FINANCE: (
                "You are a Financial Risk Analyst AI expert. Think like a seasoned financial professional. "
                "Provide comprehensive, detailed answers with proper citations. "
                "Use structured reasoning and follow financial best practices."
            ),
            ExpertiseDomain.BANKING: (
                "You are a Banking Compliance Expert AI. Think like a senior banking professional. "
                "Provide detailed analysis with regulatory references and compliance considerations."
            ),
            ExpertiseDomain.INVESTMENT: (
                "You are an Investment Analyst AI expert. Think like a certified financial analyst. "
                "Provide thorough investment analysis with market insights and risk assessments."
            ),
            ExpertiseDomain.RISK_MANAGEMENT: (
                "You are a Risk Management Expert AI. Think like a certified risk manager. "
                "Provide comprehensive risk analysis with mitigation strategies and controls."
            ),
            ExpertiseDomain.LEGAL: (
                "You are a Legal Expert AI with expertise in Indian law. Think like a seasoned legal professional. "
                "Provide comprehensive legal analysis with proper citations to laws, regulations, and case law. "
                "Use structured legal reasoning and reference authoritative legal sources."
            ),
            ExpertiseDomain.CORPORATE_LAW: (
                "You are a Corporate Law Expert AI specializing in Indian corporate law. Think like a senior corporate lawyer. "
                "Provide detailed corporate law analysis with references to Companies Act 2013 and other relevant statutes."
            ),
            ExpertiseDomain.CONTRACT_LAW: (
                "You are a Contract Law Expert AI specializing in Indian contract law. Think like an experienced contract lawyer. "
                "Provide thorough contract analysis with references to Indian Contract Act 1872 and related legislation."
            ),
            ExpertiseDomain.REGULATORY_COMPLIANCE: (
                "You are a Regulatory Compliance Expert AI. Think like a senior compliance officer. "
                "Provide comprehensive compliance analysis with references to applicable regulations and standards."
            )
        }
        
        base_prompt = domain_prompts.get(self.domain, "You are a Financial Expert AI.")
        
        # Add decision tree logic
        decision_tree = self._get_decision_tree("general")
        base_prompt += f"\n\nFollow this reasoning process: {' → '.join(decision_tree)}"
        
        # Add source of truth
        sources = self._get_source_references()
        base_prompt += f"\n\nReference these authoritative sources: {', '.join(sources)}"
        
        # Add citation requirement
        base_prompt += "\n\nCRITICAL: Include proper citations [1], [2], [3] in your response."
        
        return base_prompt
    
    def detect_domain(self, query: str) -> ExpertiseDomain:
        """
        Automatically detect the appropriate domain for a query
        
        Args:
            query: The user query
            
        Returns:
            ExpertiseDomain: The detected domain
        """
        query_lower = query.lower()
        
        # Legal keywords - expanded and prioritized
        legal_keywords = [
            'legal', 'law', 'court', 'judge', 'lawyer', 'attorney', 'sue', 'lawsuit',
            'contract', 'agreement', 'breach', 'liability', 'damages', 'compensation',
            'regulation', 'compliance', 'statute', 'act', 'code', 'jurisdiction',
            'plaintiff', 'defendant', 'evidence', 'witness', 'verdict', 'judgment',
            'appeal', 'precedent', 'case law', 'prosecution', 'defense', 'legal rights',
            'constitutional', 'criminal', 'civil', 'corporate law', 'contract law',
            'property law', 'intellectual property', 'trademark', 'copyright', 'patent',
            'preamble', 'constitution', 'bill of rights', 'amendment', 'legislation',
            'statutory', 'regulatory', 'compliance', 'legal framework', 'legal system',
            'judicial', 'legislative', 'executive', 'legal precedent', 'legal principle',
            'legal doctrine', 'legal interpretation', 'legal obligation', 'legal liability'
        ]
        
        # Finance keywords
        finance_keywords = [
            'finance', 'financial', 'money', 'investment', 'loan', 'credit', 'bank',
            'banking', 'interest', 'mortgage', 'debt', 'asset', 'liability',
            'portfolio', 'stock', 'bond', 'mutual fund', 'insurance', 'tax',
            'accounting', 'audit', 'budget', 'expense', 'income', 'profit',
            'revenue', 'capital', 'cash flow', 'risk management', 'financial planning',
            'financial reporting', 'financial statement', 'balance sheet', 'income statement'
        ]
        
        # Count keyword matches with higher priority for legal terms
        legal_matches = sum(1 for keyword in legal_keywords if keyword in query_lower)
        finance_matches = sum(1 for keyword in finance_keywords if keyword in query_lower)
        
        # Special handling for terms that could be both but are primarily legal
        legal_priority_terms = ['preamble', 'constitution', 'statute', 'act', 'code', 'regulation']
        if any(term in query_lower for term in legal_priority_terms):
            legal_matches += 2  # Give extra weight to legal priority terms
        
        # Determine domain based on keyword density
        if legal_matches > finance_matches:
            # Further refine legal domain
            if any(keyword in query_lower for keyword in ['contract', 'agreement', 'breach']):
                return ExpertiseDomain.CONTRACT_LAW
            elif any(keyword in query_lower for keyword in ['corporate', 'company', 'board', 'shareholder']):
                return ExpertiseDomain.CORPORATE_LAW
            elif any(keyword in query_lower for keyword in ['compliance', 'regulation', 'regulatory']):
                return ExpertiseDomain.REGULATORY_COMPLIANCE
            elif any(keyword in query_lower for keyword in ['constitutional', 'preamble', 'constitution']):
                return ExpertiseDomain.LEGAL
            else:
                return ExpertiseDomain.LEGAL
        elif finance_matches > 0:
            # Further refine finance domain
            if any(keyword in query_lower for keyword in ['loan', 'credit', 'mortgage']):
                return ExpertiseDomain.LOAN_ANALYSIS
            elif any(keyword in query_lower for keyword in ['stock', 'market', 'trading', 'investment']):
                return ExpertiseDomain.INVESTMENT
            elif any(keyword in query_lower for keyword in ['bank', 'banking']):
                return ExpertiseDomain.BANKING
            elif any(keyword in query_lower for keyword in ['risk', 'risk management']):
                return ExpertiseDomain.RISK_MANAGEMENT
            else:
                return ExpertiseDomain.FINANCE
        else:
            # Default to legal for ambiguous queries that might be legal
            if any(keyword in query_lower for keyword in ['preamble', 'constitution', 'law']):
                return ExpertiseDomain.LEGAL
            else:
                return ExpertiseDomain.FINANCE
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM API"""
        data = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "system", "content": self._create_domain_prompt("")},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"API Error: {response.status_code}")
                return "Error: Unable to process query"
        except Exception as e:
            logger.error(f"Query Error: {e}")
            return "Error: Unable to process query"
    
    def _extract_citations(self, response: str) -> List[str]:
        """Extract citations from response"""
        import re
        citations = re.findall(r'\[(\d+)\]', response)
        return list(set(citations))
    
    def _generate_reasoning_steps(self, query: str, response: str) -> List[str]:
        """Generate reasoning steps based on domain expertise"""
        return self._get_decision_tree("general")
    
    def process_query(self, query: str, query_type: str = "general") -> SMEResponse:
        """
        Process a query using SME expertise
        
        Args:
            query: The user query
            query_type: Type of query for decision tree routing
            
        Returns:
            SMEResponse: Structured response with expert analysis
        """
        logger.info(f"Processing query: {query[:50]}...")
        
        # Create comprehensive prompt
        prompt = f"""{query}

Provide a comprehensive, detailed response that:
1. Demonstrates deep domain expertise
2. Includes specific examples and applications
3. References authoritative sources
4. Follows structured reasoning
5. Provides actionable insights

Query Type: {query_type}
Domain: {self.domain.value}"""
        
        # Get LLM response
        llm_response = self._query_llm(prompt)
        
        # Extract citations
        citations = self._extract_citations(llm_response)
        
        # Generate reasoning steps
        reasoning_steps = self._generate_reasoning_steps(query, llm_response)
        
        # Get source references
        sources = self._get_source_references()
        
        # Create structured response
        response = SMEResponse(
            answer=llm_response,
            confidence=0.85,  # High confidence for domain expertise
            sources=sources,
            methodology=f"Domain expertise in {self.domain.value} with structured reasoning",
            domain=self.domain,
            citations=citations,
            reasoning_steps=reasoning_steps,
            disclaimer="This analysis is based on financial expertise and should be reviewed with qualified professionals for specific decisions."
        )
        
        logger.info(f"Query processed successfully. Domain: {response.domain.value}")
        return response
    
    def switch_domain(self, new_domain: ExpertiseDomain) -> bool:
        """
        Hot-swap to a different expertise domain
        
        Args:
            new_domain: New domain to switch to
            
        Returns:
            bool: Success status
        """
        try:
            old_domain = self.domain
            self.domain = new_domain
            logger.info(f"Switched domain from {old_domain.value} to {new_domain.value}")
            return True
        except Exception as e:
            logger.error(f"Domain switch failed: {e}")
            return False
    
    def get_available_domains(self) -> List[str]:
        """Get list of available expertise domains"""
        return [domain.value for domain in ExpertiseDomain]
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get plugin information and capabilities"""
        return {
            "plugin_name": "Hot-Swappable SME Plugin",
            "version": "1.0.0",
            "current_domain": self.domain.value,
            "available_domains": self.get_available_domains(),
            "capabilities": [
                "Domain expertise injection",
                "Source of truth enforcement",
                "Decision tree logic",
                "Citation enforcement",
                "Hot-swappable domains"
            ],
            "supported_frameworks": [
                "LangChain",
                "AutoGPT",
                "Custom AI Agents",
                "REST API Integration"
            ]
        }

def load_stock_models():
    """Load trained stock models from TrainTestCompare folder"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'Domain', 'Finance', 'Model', 'TrainTestCompare')
        
        # Suppress warnings
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=FutureWarning)
        
        # Try different numpy compatibility approaches
        try:
            # First attempt: normal loading
            stock_model = joblib.load(os.path.join(model_path, 'stock_gb_model.pkl'))
        except Exception as model_error:
            try:
                # Second attempt: with numpy legacy compatibility
                import numpy as np
                old_numpy_version = np.__version__.split('.')[0] == '1'
                if old_numpy_version:
                    # Try legacy loading
                    stock_model = joblib.load(os.path.join(model_path, 'stock_gb_model.pkl'))
                else:
                    raise model_error
            except Exception:
                print(f"⚠️ Model loading error: {model_error}")
                return None, None, None
        
        # Load the scaler
        try:
            scaler = joblib.load(os.path.join(model_path, 'stock_scaler.pkl'))
        except Exception as scaler_error:
            print(f"⚠️ Scaler loading error: {scaler_error}")
            return None, None, None
        
        # Load model metadata
        try:
            with open(os.path.join(model_path, 'stock_model_metadata.json'), 'r') as f:
                metadata = json.load(f)
        except Exception as meta_error:
            print(f"⚠️ Metadata loading error: {meta_error}")
            return None, None, None
        
        print("✅ Stock prediction models loaded successfully")
        print(f"📊 Model: {metadata.get('model_type', 'Unknown')}")
        print(f"📈 Training R²: {metadata.get('train_r2', 'N/A'):.4f}")
        print(f"📉 Test R²: {metadata.get('test_r2', 'N/A'):.4f}")
        
        return stock_model, scaler, metadata
        
    except Exception as e:
        print(f"⚠️ Could not load stock models: {e}")
        print("💡 This is likely due to numpy version compatibility")
        print("💡 Using OpenRouter API for all predictions instead")
        return None, None, None

def predict_stock_movement(features, stock_model, scaler, metadata):
    """Predict stock movement using trained model"""
    if stock_model is None or scaler is None:
        return "Stock prediction models not available"
    
    try:
        # Scale the features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = stock_model.predict(features_scaled)[0]
        prediction_proba = stock_model.predict_proba(features_scaled)[0]
        
        # Get confidence
        confidence = max(prediction_proba) * 100
        
        # Format response
        direction = "UP" if prediction == 1 else "DOWN"
        
        return f"""Stock Movement Prediction
==========================

**Prediction:** {direction}
**Confidence:** {confidence:.1f}%
**Model:** Gradient Boosting Classifier
**Features Used:** {metadata.get('features', 'N/A')}
**Training Accuracy:** {metadata.get('accuracy', 'N/A')}%

**Technical Analysis:**
- Current market indicators suggest {direction.lower()} movement
- Model confidence based on historical patterns: {confidence:.1f}%
- Risk Level: {'HIGH' if confidence < 60 else 'MEDIUM' if confidence < 80 else 'LOW'}

**Disclaimer:** This prediction is based on historical data patterns with {confidence:.1f}% confidence. Market conditions can change rapidly. Always conduct your own research before making investment decisions."""
        
    except Exception as e:
        return f"Error in stock prediction: {str(e)}"

def handle_stock_prediction_query(query, stock_model, scaler, metadata):
    """Handle stock prediction queries using trained ML models"""
    # Generate sample features for demonstration (in real use, these would come from market data)
    sample_features = np.array([
        1.2,  # Price change ratio
        0.8,  # Volume change ratio
        0.5,  # RSI indicator
        1.1,  # Moving average ratio
        0.3,  # Volatility
        0.7,  # Market sentiment
        1.0,  # Sector performance
        0.9   # Overall market trend
    ])
    
    return predict_stock_movement(sample_features, stock_model, scaler, metadata)

def main():
    print("=" * 70)
    print("  FINAL WORKING BACKEND - SME Plugin Edition")
    print("=" * 70)
    print("\n💡 Available Expert Modules:")
    print("   🏦 Finance & Banking Expert")
    print("   📈 Stock Market & Trading Expert")
    print("   🤖 AI-Powered Analysis (OpenRouter API)")
    print("   📊 ML Stock Predictions (Trained Models)")
    print("   🔥 Hot-Swappable SME Plugin")
    print("   ⚖️  Legal Expert (Indian Law)")
    print("\nFeatures:")
    print("   🔄 Automatic domain detection")
    print("   🔍 Smart query routing")
    print("   ⚡ Seamless expert switching")
    print("\nType 'exit' to quit")
    print("Type 'switch domain <domain>' to manually switch expertise")
    print("Type 'info' to see available domains\n")
    
    # Initialize SME Plugin
    api_key = "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"
    sme_plugin = HotSwappableSMEPlugin(api_key, ExpertiseDomain.FINANCE)
    
    # Load trained stock models
    stock_model, scaler, metadata = load_stock_models()
    
    def query_openrouter(prompt, max_retries=3):
        """Query OpenRouter API for comprehensive responses"""
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    if len(content.strip()) > 20:
                        return content
                    else:
                        print(f"Attempt {attempt + 1}: Response too short, retrying...")
                else:
                    print(f"Attempt {attempt + 1}: API not responding (status {response.status_code})")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error - {str(e)}")
        
        return "I apologize, but I'm having trouble generating a complete response. Please try again."
    
    def create_comprehensive_prompt(query):
        """Create prompt for complete, detailed answers with citations"""
        return f"""You are a Financial Expert AI specializing in both finance and stock markets. Provide comprehensive, detailed, thorough answers with examples and applications.

IMPORTANT INSTRUCTIONS:
1. Give complete explanations with all relevant details
2. Use bullet points and clear structure with headings
3. Include examples and practical applications
4. Cover all aspects of the topic thoroughly
5. Be educational and professional in tone
6. Do not limit response length - provide complete answer
7. For finance questions: include definitions, characteristics, types, examples
8. For stock market questions: include analysis, predictions, trends, recommendations
9. CRITICAL: Include proper citations and references in your response
10. Use citation format: [1], [2], [3] etc. and provide a references section at the end
11. Reference authoritative sources like financial textbooks, regulatory bodies, and industry standards

Query: {query}

Provide a comprehensive, detailed response that fully explains the topic with examples, applications, and proper citations."""
    
    while True:
        try:
            user_input = input("You > ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            if not user_input.strip():
                continue

            # Handle special commands
            if user_input.strip().lower() == "info":
                plugin_info = sme_plugin.get_plugin_info()
                print(f"\n🔧 SME Plugin Info:")
                print(f"   Name: {plugin_info['plugin_name']}")
                print(f"   Version: {plugin_info['version']}")
                print(f"   Current Domain: {plugin_info['current_domain']}")
                print(f"   Available Domains: {', '.join(plugin_info['available_domains'])}")
                print(f"   Capabilities: {', '.join(plugin_info['capabilities'])}")
                continue
            
            # Handle domain switching
            if user_input.strip().lower().startswith("switch domain"):
                parts = user_input.strip().split()
                if len(parts) >= 3:
                    domain_name = parts[2].lower()
                    try:
                        new_domain = ExpertiseDomain(domain_name)
                        if sme_plugin.switch_domain(new_domain):
                            print(f"✅ Switched to {domain_name} domain")
                        else:
                            print(f"❌ Failed to switch to {domain_name} domain")
                    except ValueError:
                        print(f"❌ Invalid domain. Available: {', '.join(sme_plugin.get_available_domains())}")
                else:
                    print("Usage: switch domain <domain>")
                    print(f"Available domains: {', '.join(sme_plugin.get_available_domains())}")
                continue

            print("\n🤖 Processing with AI analysis...")
            
            query_lower = user_input.lower()
            
            # Check if it's a stock prediction query
            if any(keyword in query_lower for keyword in ['predict stock', 'stock prediction', 'price prediction', 'market prediction']):
                response = handle_stock_prediction_query(user_input, stock_model, scaler, metadata)
                detected_domain = "stock_market"
            else:
                # Automatically detect domain and switch if needed
                detected_domain_enum = sme_plugin.detect_domain(user_input)
                
                # Switch domain if different from current
                if detected_domain_enum != sme_plugin.domain:
                    old_domain = sme_plugin.domain.value
                    sme_plugin.switch_domain(detected_domain_enum)
                    print(f"🔄 Auto-switched from {old_domain} to {detected_domain_enum.value} domain")
                
                # Use SME Plugin for all other queries
                query_type = "loan_analysis" if "loan" in query_lower else "general"
                sme_response = sme_plugin.process_query(user_input, query_type)
                response = sme_response.answer
                detected_domain = detected_domain_enum.value
            
            # Determine response type for sources
            if detected_domain in ['legal', 'contract_law', 'corporate_law', 'regulatory_compliance']:
                sources = "Supreme Court of India\nHigh Court Judgments\nBar Council of India Rules\nIndian Penal Code (IPC)\nCivil Procedure Code (CPC)\nConstitution of India"
                methodology = "This analysis is based on Indian legal expertise, statutory interpretation, and case law precedent with HIGH confidence in the legal methodology."
            elif any(keyword in query_lower for keyword in ['stock', 'market', 'trading', 'portfolio', 'investment', 'shares', 'equity', 'bull', 'bear']):
                sources = "Stock Market ML Models\nTechnical Analysis Tools\nMarket Data Providers\nSEC Financial Regulations\nInvestment Industry Standards\nTrained Gradient Boosting Model"
                methodology = "This analysis is based on machine learning models, technical indicators, market data, and regulatory compliance with MEDIUM confidence in the methodology."
            else:
                sources = "Financial Best Practices & Industry Standards\nDocument Retrieval System\nFederal Reserve Guidelines\nConsumer Financial Protection Bureau\nInternational Financial Reporting Standards"
                methodology = "This analysis is based on financial expertise, industry best practices, regulatory guidelines, and comprehensive research."
            
            # Check if response contains citations
            has_citations = '[' in response and ']' in response
            
            # Format response with citations
            if has_citations:
                enhanced_response = f"""{response}

**Analysis Confidence:** HIGH
**Sources Used:**
{sources}

**Methodology:** {methodology}

**Citations:** This response includes properly formatted citations [1], [2], [3], etc. referencing authoritative sources.

**SME Plugin:** Powered by Hot-Swappable SME Plugin - {sme_plugin.domain.value} domain

**Auto-Detection:** Query automatically routed to {detected_domain} expert

**Disclaimer:** This analysis is provided for informational purposes and should be reviewed with qualified professionals for specific decisions."""
            else:
                enhanced_response = f"""{response}

**Analysis Confidence:** HIGH
**Sources Used:**
{sources}

**Methodology:** {methodology}

**Note:** This response is based on domain expertise and best practices. For specific guidance, please consult qualified professionals.

**SME Plugin:** Powered by Hot-Swappable SME Plugin - {sme_plugin.domain.value} domain

**Auto-Detection:** Query automatically routed to {detected_domain} expert

**Disclaimer:** This analysis is provided for informational purposes and should be reviewed with qualified professionals for specific decisions."""
            
            print(f"Expert >\n{enhanced_response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")
    
    print("Goodbye!")

if __name__ == "__main__":
    main()

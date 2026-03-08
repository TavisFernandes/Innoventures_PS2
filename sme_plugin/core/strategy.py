from .plugin import Strategy
import re

class FinanceStrategy(Strategy):
    def get_system_prompt(self) -> str:
        return (
            "You are a rapid Financial Analyst AI. Answer in 2-3 sentences maximum.\n"
            "Rules: 1) Use only provided context. 2) Under 100 words total. "
            "3) Direct answer only - no explanations. 4) Use bullets if needed. "
            "5) No markdown or asterisks. 6) Stop immediately at 150 tokens. "
            "Be brutally concise. Speed is critical."
        )

    def inject_constraints(self, context: str, query: str) -> str:
        if not context:
            return (
                f"Query: {query}\n\n"
                "Note: No domain documents were provided for context. Answer only using your baseline knowledge, "
                "but emphasize that this answer is not grounded in specific user documents."
            )
        
        return (
            f"Context Documents:\n{context}\n\n"
            f"User Query: {query}\n\n"
            "Instruction: Answer the query exclusively using the context documents above. "
            "Follow the structural rules established in your system prompt. "
            "Include direct citations or references to the context provided. "
            "Use clean formatting without asterisks (**). Use simple text with clear headings."
        )
    
    def format_response(self, response: str) -> str:
        """Clean up response formatting to remove asterisks and improve structure"""
        # Remove asterisks used for bold formatting
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        
        # Clean up excessive whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        # Ensure proper section breaks
        cleaned = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', cleaned)
        
        return cleaned.strip()

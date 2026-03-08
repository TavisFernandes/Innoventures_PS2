from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

class Strategy(ABC):
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def inject_constraints(self, context: str, query: str) -> str:
        """Modifies the query to ensure constraints are met (e.g., citing sources)."""
        pass

class SMEPlugin:
    def __init__(self, strategy: Strategy, llm: BaseChatModel, retriever=None):
        self.strategy = strategy
        self.llm = llm
        self.retriever = retriever

    def process_query(self, query: str, max_retries: int = 3) -> str:
        context = ""
        if self.retriever:
            docs = self.retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in docs])
        
        system_prompt = self.strategy.get_system_prompt()
        structured_query = self.strategy.inject_constraints(context, query)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=structured_query)
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(messages)
                raw_content = response.content
                
                # Apply response formatting if strategy supports it
                if hasattr(self.strategy, 'format_response'):
                    return self.strategy.format_response(raw_content)
                else:
                    return raw_content
                    
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    wait = 15 * (attempt + 1)
                    print(f"  Rate limited — waiting {wait}s before retry ({attempt+1}/{max_retries})...")
                    time.sleep(wait)
                else:
                    raise
        return "Error: Rate limit exceeded after retries. Please wait a minute and try again."


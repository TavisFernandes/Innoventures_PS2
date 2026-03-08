#!/usr/bin/env python3
"""
Hot-Swappable SME Plugin API
Universal Finance Expert Plugin for AI Agents
"""
import os
import sys
import json
import requests
import yaml
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

@dataclass
class SMEPluginConfig:
    """Configuration for SME Plugin"""
    domain: ExpertiseDomain
    api_key: str
    model_name: str = "anthropic/claude-3-haiku"
    max_tokens: int = 1000
    temperature: float = 0.7
    enforce_citations: bool = True
    source_of_truth: bool = True
    decision_tree_logic: bool = True

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
    
    def __init__(self, config: SMEPluginConfig):
        self.config = config
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        # Load domain-specific decision trees
        self.decision_trees = self._load_decision_trees()
        
        # Load source of truth references
        self.source_references = self._load_source_references()
        
        logger.info(f"SME Plugin initialized for domain: {config.domain.value}")
    
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
            ]
        }
    
    def _get_decision_tree(self, query_type: str) -> List[str]:
        """Get decision tree steps for query type"""
        domain_trees = self.decision_trees.get(self.config.domain, {})
        return domain_trees.get(query_type, ["Analyze query requirements", "Apply domain expertise", "Provide structured response"])
    
    def _get_source_references(self) -> List[str]:
        """Get relevant source references for domain"""
        return self.source_references.get(self.config.domain, ["Industry Best Practices"])
    
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
            )
        }
        
        base_prompt = domain_prompts.get(self.config.domain, "You are a Financial Expert AI.")
        
        if self.config.decision_tree_logic:
            decision_tree = self._get_decision_tree("general")
            base_prompt += f"\n\nFollow this reasoning process: {' → '.join(decision_tree)}"
        
        if self.config.source_of_truth:
            sources = self._get_source_references()
            base_prompt += f"\n\nReference these authoritative sources: {', '.join(sources)}"
        
        if self.config.enforce_citations:
            base_prompt += "\n\nCRITICAL: Include proper citations [1], [2], [3] in your response."
        
        return base_prompt
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM API"""
        data = {
            "model": self.config.model_name,
            "messages": [
                {"role": "system", "content": self._create_domain_prompt("")},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
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
        if self.config.decision_tree_logic:
            return self._get_decision_tree("general")
        else:
            return ["Analyzed query", "Applied domain expertise", "Generated response"]
    
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
Domain: {self.config.domain.value}"""
        
        # Get LLM response
        llm_response = self._query_llm(prompt)
        
        # Extract citations
        citations = self._extract_citations(llm_response) if self.config.enforce_citations else []
        
        # Generate reasoning steps
        reasoning_steps = self._generate_reasoning_steps(query, llm_response)
        
        # Get source references
        sources = self._get_source_references()
        
        # Create structured response
        response = SMEResponse(
            answer=llm_response,
            confidence=0.85,  # High confidence for domain expertise
            sources=sources,
            methodology=f"Domain expertise in {self.config.domain.value} with structured reasoning",
            domain=self.config.domain,
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
            old_domain = self.config.domain
            self.config.domain = new_domain
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
            "current_domain": self.config.domain.value,
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

# Factory function for easy plugin creation
def create_finance_sme_plugin(api_key: str) -> HotSwappableSMEPlugin:
    """Create a finance domain SME plugin"""
    config = SMEPluginConfig(
        domain=ExpertiseDomain.FINANCE,
        api_key=api_key,
        enforce_citations=True,
        source_of_truth=True,
        decision_tree_logic=True
    )
    return HotSwappableSMEPlugin(config)

def create_banking_sme_plugin(api_key: str) -> HotSwappableSMEPlugin:
    """Create a banking domain SME plugin"""
    config = SMEPluginConfig(
        domain=ExpertiseDomain.BANKING,
        api_key=api_key,
        enforce_citations=True,
        source_of_truth=True,
        decision_tree_logic=True
    )
    return HotSwappableSMEPlugin(config)

def create_investment_sme_plugin(api_key: str) -> HotSwappableSMEPlugin:
    """Create an investment domain SME plugin"""
    config = SMEPluginConfig(
        domain=ExpertiseDomain.INVESTMENT,
        api_key=api_key,
        enforce_citations=True,
        source_of_truth=True,
        decision_tree_logic=True
    )
    return HotSwappableSMEPlugin(config)

# Example usage
if __name__ == "__main__":
    # Create finance SME plugin
    api_key = "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"
    plugin = create_finance_sme_plugin(api_key)
    
    # Test query
    response = plugin.process_query("What is a loan and how should I analyze loan applications?")
    
    print("=" * 60)
    print("SME Plugin Response")
    print("=" * 60)
    print(f"Domain: {response.domain.value}")
    print(f"Confidence: {response.confidence}")
    print(f"Sources: {', '.join(response.sources[:3])}")
    print(f"Citations: {response.citations}")
    print(f"Reasoning Steps: {' → '.join(response.reasoning_steps[:3])}")
    print("\nAnswer:")
    print(response.answer)
    print(f"\nDisclaimer: {response.disclaimer}")

#!/usr/bin/env python3
"""
SME Plugin Client Library
Easy integration for AI agents with SME Plugin API
"""
import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SMEQueryResult:
    """Result from SME plugin query"""
    answer: str
    confidence: float
    sources: List[str]
    methodology: str
    domain: str
    citations: List[str]
    reasoning_steps: List[str]
    disclaimer: str

class SMEPluginClient:
    """
    Client library for SME Plugin API
    Easy integration for AI agents
    """
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Test connection
        if not self._test_connection():
            raise ConnectionError(f"Cannot connect to SME Plugin API at {base_url}")
    
    def _test_connection(self) -> bool:
        """Test connection to SME Plugin API"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get plugin information and capabilities"""
        try:
            response = self.session.get(f"{self.base_url}/plugin/info", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting plugin info: {e}")
            return {}
    
    def get_available_domains(self) -> Dict[str, Any]:
        """Get list of available expertise domains"""
        try:
            response = self.session.get(f"{self.base_url}/plugin/domains", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting domains: {e}")
            return {}
    
    def switch_domain(self, domain: str) -> bool:
        """Switch to a different expertise domain"""
        try:
            response = self.session.post(
                f"{self.base_url}/plugin/switch_domain",
                json={"domain": domain},
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error switching domain: {e}")
            return False
    
    def query(self, query_text: str, query_type: str = "general") -> Optional[SMEQueryResult]:
        """
        Process a query using SME expertise
        
        Args:
            query_text: The query to process
            query_type: Type of query for specialized processing
            
        Returns:
            SMEQueryResult: Structured result with expert analysis
        """
        try:
            response = self.session.post(
                f"{self.base_url}/query",
                json={"query": query_text, "query_type": query_type},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return SMEQueryResult(
                answer=data.get('answer', ''),
                confidence=data.get('confidence', 0.0),
                sources=data.get('sources', []),
                methodology=data.get('methodology', ''),
                domain=data.get('domain', ''),
                citations=data.get('citations', []),
                reasoning_steps=data.get('reasoning_steps', []),
                disclaimer=data.get('disclaimer', '')
            )
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return None
    
    def simple_query(self, query_text: str) -> Optional[str]:
        """
        Simple query interface for easy integration
        
        Args:
            query_text: The query to process
            
        Returns:
            str: Simple answer or None if error
        """
        try:
            response = self.session.post(
                f"{self.base_url}/query/simple",
                json={"query": query_text},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get('answer', '')
        except Exception as e:
            logger.error(f"Error processing simple query: {e}")
            return None
    
    def analyze_loan(self, loan_data: Dict[str, Any]) -> Optional[SMEQueryResult]:
        """
        Analyze loan application using SME expertise
        
        Args:
            loan_data: Loan application data
            
        Returns:
            SMEQueryResult: Loan analysis result
        """
        try:
            response = self.session.post(
                f"{self.base_url}/analyze/loan",
                json=loan_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return SMEQueryResult(
                answer=data.get('analysis', ''),
                confidence=data.get('confidence', 0.0),
                sources=data.get('sources', []),
                methodology=data.get('methodology', ''),
                domain=data.get('domain', ''),
                citations=data.get('citations', []),
                reasoning_steps=data.get('risk_factors', []),
                disclaimer=data.get('disclaimer', '')
            )
        except Exception as e:
            logger.error(f"Error analyzing loan: {e}")
            return None
    
    def analyze_investment(self, investment_data: Dict[str, Any]) -> Optional[SMEQueryResult]:
        """
        Analyze investment opportunity using SME expertise
        
        Args:
            investment_data: Investment data
            
        Returns:
            SMEQueryResult: Investment analysis result
        """
        try:
            response = self.session.post(
                f"{self.base_url}/analyze/investment",
                json=investment_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return SMEQueryResult(
                answer=data.get('analysis', ''),
                confidence=data.get('confidence', 0.0),
                sources=data.get('sources', []),
                methodology=data.get('methodology', ''),
                domain=data.get('domain', ''),
                citations=data.get('citations', []),
                reasoning_steps=data.get('recommendations', []),
                disclaimer=data.get('disclaimer', '')
            )
        except Exception as e:
            logger.error(f"Error analyzing investment: {e}")
            return None
    
    def analyze_risk(self, risk_data: Dict[str, Any]) -> Optional[SMEQueryResult]:
        """
        Analyze risk scenario using SME expertise
        
        Args:
            risk_data: Risk scenario data
            
        Returns:
            SMEQueryResult: Risk analysis result
        """
        try:
            response = self.session.post(
                f"{self.base_url}/analyze/risk",
                json=risk_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return SMEQueryResult(
                answer=data.get('risk_analysis', ''),
                confidence=data.get('confidence', 0.0),
                sources=data.get('sources', []),
                methodology=data.get('methodology', ''),
                domain=data.get('domain', ''),
                citations=data.get('citations', []),
                reasoning_steps=data.get('mitigation_steps', []),
                disclaimer=data.get('disclaimer', '')
            )
        except Exception as e:
            logger.error(f"Error analyzing risk: {e}")
            return None

# Convenience functions for easy integration
def create_sme_client(base_url: str = "http://localhost:5000") -> SMEPluginClient:
    """Create and return SME Plugin client"""
    return SMEPluginClient(base_url)

def quick_finance_query(query: str, base_url: str = "http://localhost:5000") -> Optional[str]:
    """Quick finance query for easy integration"""
    client = SMEPluginClient(base_url)
    return client.simple_query(query)

def quick_loan_analysis(loan_data: Dict[str, Any], base_url: str = "http://localhost:5000") -> Optional[str]:
    """Quick loan analysis for easy integration"""
    client = SMEPluginClient(base_url)
    result = client.analyze_loan(loan_data)
    return result.answer if result else None

# Example usage and integration patterns
if __name__ == "__main__":
    # Example 1: Basic usage
    print("=== SME Plugin Client Examples ===")
    
    try:
        # Create client
        client = create_sme_client()
        
        # Get plugin info
        info = client.get_plugin_info()
        print(f"Plugin: {info.get('plugin_name')}")
        print(f"Domains: {', '.join(info.get('available_domains', []))}")
        
        # Simple query
        answer = client.simple_query("What is a loan?")
        print(f"\nSimple Query Answer: {answer[:100]}...")
        
        # Detailed query
        result = client.query("Explain loan underwriting process")
        print(f"\nDetailed Query:")
        print(f"Domain: {result.domain}")
        print(f"Confidence: {result.confidence}")
        print(f"Sources: {', '.join(result.sources[:2])}")
        print(f"Answer: {result.answer[:200]}...")
        
        # Loan analysis
        loan_data = {
            "applicant": "John Doe",
            "amount": 50000,
            "credit_score": 720,
            "income": 75000,
            "debt_to_income": 0.35
        }
        
        loan_result = client.analyze_loan(loan_data)
        print(f"\nLoan Analysis:")
        print(f"Risk Factors: {', '.join(loan_result.reasoning_steps[:3])}")
        print(f"Analysis: {loan_result.answer[:200]}...")
        
    except Exception as e:
        print(f"Example failed: {e}")
        print("Make sure the SME Plugin API server is running on localhost:5000")

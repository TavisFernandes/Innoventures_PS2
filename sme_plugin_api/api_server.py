#!/usr/bin/env python3
"""
SME Plugin REST API Server
Universal Finance Expert Plugin API for AI Agents
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Any
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from sme_plugin import (
    HotSwappableSMEPlugin, 
    SMEPluginConfig, 
    ExpertiseDomain,
    create_finance_sme_plugin,
    create_banking_sme_plugin,
    create_investment_sme_plugin
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Global plugin instance
sme_plugin = None

def initialize_plugin():
    """Initialize the SME plugin with finance domain"""
    global sme_plugin
    api_key = "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"
    sme_plugin = create_finance_sme_plugin(api_key)
    logger.info("SME Plugin initialized with Finance domain")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "plugin": "SME Plugin API",
        "version": "1.0.0"
    })

@app.route('/plugin/info', methods=['GET'])
def get_plugin_info():
    """Get plugin information and capabilities"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    return jsonify(sme_plugin.get_plugin_info())

@app.route('/plugin/domains', methods=['GET'])
def get_available_domains():
    """Get list of available expertise domains"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    return jsonify({
        "available_domains": sme_plugin.get_available_domains(),
        "current_domain": sme_plugin.config.domain.value
    })

@app.route('/plugin/switch_domain', methods=['POST'])
def switch_domain():
    """Hot-swap to a different expertise domain"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data or 'domain' not in data:
        return jsonify({"error": "Domain parameter required"}), 400
    
    try:
        new_domain = ExpertiseDomain(data['domain'])
        success = sme_plugin.switch_domain(new_domain)
        
        if success:
            return jsonify({
                "message": f"Successfully switched to {new_domain.value} domain",
                "current_domain": sme_plugin.config.domain.value
            })
        else:
            return jsonify({"error": "Domain switch failed"}), 500
            
    except ValueError:
        return jsonify({"error": f"Invalid domain. Available: {[d.value for d in ExpertiseDomain]}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def process_query():
    """Process a query using SME expertise"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter required"}), 400
    
    query = data['query']
    query_type = data.get('query_type', 'general')
    
    try:
        response = sme_plugin.process_query(query, query_type)
        
        return jsonify({
            "answer": response.answer,
            "confidence": response.confidence,
            "sources": response.sources,
            "methodology": response.methodology,
            "domain": response.domain.value,
            "citations": response.citations,
            "reasoning_steps": response.reasoning_steps,
            "disclaimer": response.disclaimer
        })
        
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/query/simple', methods=['POST'])
def process_simple_query():
    """Simple query endpoint for easy integration"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter required"}), 400
    
    query = data['query']
    
    try:
        response = sme_plugin.process_query(query)
        
        return jsonify({
            "answer": response.answer,
            "confidence": response.confidence,
            "domain": response.domain.value,
            "sources": response.sources[:3],  # Limit to top 3 sources
            "citations": response.citations
        })
        
    except Exception as e:
        logger.error(f"Simple query processing error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/loan', methods=['POST'])
def analyze_loan():
    """Specialized loan analysis endpoint"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Loan data required"}), 400
    
    # Construct loan analysis query
    query = f"Analyze this loan application: {json.dumps(data)}"
    
    try:
        # Switch to finance domain if not already
        if sme_plugin.config.domain != ExpertiseDomain.FINANCE:
            sme_plugin.switch_domain(ExpertiseDomain.FINANCE)
        
        response = sme_plugin.process_query(query, "loan_analysis")
        
        return jsonify({
            "analysis": response.answer,
            "confidence": response.confidence,
            "risk_factors": response.reasoning_steps,
            "sources": response.sources,
            "citations": response.citations,
            "disclaimer": response.disclaimer
        })
        
    except Exception as e:
        logger.error(f"Loan analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/investment', methods=['POST'])
def analyze_investment():
    """Specialized investment analysis endpoint"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Investment data required"}), 400
    
    # Construct investment analysis query
    query = f"Analyze this investment opportunity: {json.dumps(data)}"
    
    try:
        # Switch to investment domain if not already
        if sme_plugin.config.domain != ExpertiseDomain.INVESTMENT:
            sme_plugin.switch_domain(ExpertiseDomain.INVESTMENT)
        
        response = sme_plugin.process_query(query, "investment_analysis")
        
        return jsonify({
            "analysis": response.answer,
            "confidence": response.confidence,
            "recommendations": response.reasoning_steps,
            "sources": response.sources,
            "citations": response.citations,
            "disclaimer": response.disclaimer
        })
        
    except Exception as e:
        logger.error(f"Investment analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/risk', methods=['POST'])
def analyze_risk():
    """Specialized risk analysis endpoint"""
    if not sme_plugin:
        return jsonify({"error": "Plugin not initialized"}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Risk data required"}), 400
    
    # Construct risk analysis query
    query = f"Analyze this risk scenario: {json.dumps(data)}"
    
    try:
        # Switch to risk management domain if not already
        if sme_plugin.config.domain != ExpertiseDomain.RISK_MANAGEMENT:
            sme_plugin.switch_domain(ExpertiseDomain.RISK_MANAGEMENT)
        
        response = sme_plugin.process_query(query, "risk_assessment")
        
        return jsonify({
            "risk_analysis": response.answer,
            "confidence": response.confidence,
            "mitigation_steps": response.reasoning_steps,
            "sources": response.sources,
            "citations": response.citations,
            "disclaimer": response.disclaimer
        })
        
    except Exception as e:
        logger.error(f"Risk analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Initialize plugin
    initialize_plugin()
    
    # Start the server
    print("🚀 SME Plugin API Server Starting...")
    print("📍 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /plugin/info - Plugin information")
    print("  GET  /plugin/domains - Available domains")
    print("  POST /plugin/switch_domain - Switch expertise domain")
    print("  POST /query - Process general query")
    print("  POST /query/simple - Simple query endpoint")
    print("  POST /analyze/loan - Loan analysis")
    print("  POST /analyze/investment - Investment analysis")
    print("  POST /analyze/risk - Risk analysis")
    print("\n🔗 Server running on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

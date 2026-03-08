import requests

def test_openrouter_key():
    """Test if OpenRouter API key is valid"""
    api_key = "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"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {"role": "user", "content": "Hello, test message"}
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                              headers=headers, json=data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API key is working!")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_openrouter_key()

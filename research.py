#!/usr/bin/env python3
"""
Perplexity API Research Script
"""

import os
import sys
import json
import requests
from datetime import datetime

def research_with_perplexity(query):
    """Perplexity APIを使用してリサーチを実行"""
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    # Perplexity API エンドポイント
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are a research assistant. Provide comprehensive, accurate information with sources."
            },
            {
                "role": "user",
                "content": f"Research the following topic and provide detailed information: {query}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # 結果を保存
        os.makedirs('output', exist_ok=True)
        
        research_data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results": content,
            "model": "perplexity-sonar"
        }
        
        with open('output/research_results.json', 'w', encoding='utf-8') as f:
            json.dump(research_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Research completed for: {query}")
        print(f"📄 Results saved to output/research_results.json")
        
        return content
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling Perplexity API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python research.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    research_with_perplexity(query)

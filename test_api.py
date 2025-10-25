"""
Quick API test script
Test the API without running the full app
"""

import requests
import json

def test_api():
    """Test the local API"""
    print("🧪 Testing LandGen API...")
    print("-" * 60)
    
    # API endpoint
    url = "http://localhost:8000/api/generate"
    
    # Test username
    username = "torvalds"
    
    print(f"\n📝 Request:")
    print(f"   POST {url}")
    print(f"   Body: {{'username': '{username}'}}")
    
    try:
        print(f"\n⏳ Sending request...")
        response = requests.post(
            url,
            json={"username": username},
            timeout=30
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success!")
            print(f"   User: {data['user']['name']} (@{data['user']['login']})")
            print(f"   Repos: {len(data['repositories'])}")
            print(f"\n📦 Top Repositories:")
            for i, repo in enumerate(data['repositories'][:3], 1):
                print(f"   {i}. {repo['name']} - ⭐ {repo['stargazers_count']}")
                if repo.get('ai_summary'):
                    print(f"      AI: {repo['ai_summary'][:80]}...")
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to API")
        print(f"   Make sure the API is running:")
        print(f"   cd api && uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_api()


"""
Local testing script for LandGen API
Run this to test the API locally before deployment
"""

import asyncio
from main import fetch_github_user, fetch_github_repos, generate_ai_summary, fetch_readme

async def test_api():
    """Test the API functions"""
    print("🧪 Testing LandGen API...")
    print("-" * 50)
    
    # Test username
    username = "torvalds"  # Example: Linus Torvalds
    
    try:
        # Test 1: Fetch user
        print(f"\n1️⃣ Fetching user: {username}")
        user = await fetch_github_user(username)
        print(f"✅ User found: {user.get('name')} (@{user.get('login')})")
        print(f"   Repos: {user.get('public_repos')} | Followers: {user.get('followers')}")
        
        # Test 2: Fetch repos
        print(f"\n2️⃣ Fetching top repositories...")
        repos = await fetch_github_repos(username, max_repos=3)
        print(f"✅ Found {len(repos)} repositories:")
        for i, repo in enumerate(repos, 1):
            print(f"   {i}. {repo['name']} - ⭐ {repo['stargazers_count']}")
        
        # Test 3: Fetch README and generate AI summary (if API key available)
        if repos:
            first_repo = repos[0]
            print(f"\n3️⃣ Testing README fetch for: {first_repo['name']}")
            readme = await fetch_readme(username, first_repo['name'])
            if readme:
                print(f"✅ README fetched ({len(readme)} chars)")
                print(f"\n4️⃣ Generating AI summary...")
                summary = await generate_ai_summary(
                    first_repo['name'],
                    first_repo.get('description'),
                    readme
                )
                if summary:
                    print(f"✅ AI Summary generated:")
                    print(f"   {summary}")
                else:
                    print(f"⚠️ AI summary not available (check GEMINI_API_KEY)")
            else:
                print(f"⚠️ No README found")
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api())


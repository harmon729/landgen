"""
Vercel Serverless Function for /api/generate endpoint
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import List, Optional
import google.generativeai as genai
from mangum import Mangum

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class GenerateRequest(BaseModel):
    username: str


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    forks_count: int
    language: Optional[str]
    topics: List[str]
    created_at: str
    updated_at: str
    homepage: Optional[str]
    ai_summary: Optional[str] = None


class UserProfile(BaseModel):
    login: str
    name: Optional[str]
    avatar_url: str
    bio: Optional[str]
    location: Optional[str]
    email: Optional[str]
    blog: Optional[str]
    twitter_username: Optional[str]
    public_repos: int
    followers: int
    following: int
    created_at: str


class GenerateResponse(BaseModel):
    success: bool
    user: UserProfile
    repositories: List[Repository]
    message: str


async def fetch_github_user(username: str) -> dict:
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}",
            headers=headers,
            timeout=10.0
        )
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"GitHub API error: {response.text}"
            )
        
        return response.json()


async def fetch_github_repos(username: str, max_repos: int = 6) -> List[dict]:
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}/repos",
            headers=headers,
            params={
                "sort": "updated",
                "direction": "desc",
                "per_page": max_repos
            },
            timeout=10.0
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch repositories: {response.text}"
            )
        
        return response.json()


async def fetch_readme(username: str, repo_name: str) -> Optional[str]:
    headers = {
        "Accept": "application/vnd.github.v3.raw"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.github.com/repos/{username}/{repo_name}/readme",
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 200:
                readme_text = response.text
                return readme_text[:2000] if len(readme_text) > 2000 else readme_text
            
            return None
        except Exception:
            return None


async def generate_ai_summary(repo_name: str, description: Optional[str], readme: Optional[str]) -> Optional[str]:
    if not GEMINI_API_KEY:
        return None
    
    try:
        context = f"Repository: {repo_name}\n"
        if description:
            context += f"Description: {description}\n"
        if readme:
            context += f"README excerpt:\n{readme}\n"
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Based on the following GitHub repository information, write a concise 50-word summary that highlights the key features and purpose of this project. Be clear, technical, and engaging.

{context}

Summary (max 50 words):"""
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        words = summary.split()
        if len(words) > 60:
            summary = ' '.join(words[:60]) + '...'
        
        return summary
    
    except Exception as e:
        print(f"AI summary generation failed: {e}")
        return None


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_website(request: GenerateRequest):
    username = request.username.strip()
    
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    try:
        user_data = await fetch_github_user(username)
        user_profile = UserProfile(
            login=user_data["login"],
            name=user_data.get("name"),
            avatar_url=user_data["avatar_url"],
            bio=user_data.get("bio"),
            location=user_data.get("location"),
            email=user_data.get("email"),
            blog=user_data.get("blog"),
            twitter_username=user_data.get("twitter_username"),
            public_repos=user_data["public_repos"],
            followers=user_data["followers"],
            following=user_data["following"],
            created_at=user_data["created_at"]
        )
        
        repos_data = await fetch_github_repos(username)
        
        repositories = []
        for repo in repos_data:
            readme = None
            ai_summary = None
            
            if len(repositories) == 0 and GEMINI_API_KEY:
                readme = await fetch_readme(username, repo["name"])
                if readme:
                    ai_summary = await generate_ai_summary(
                        repo["name"],
                        repo.get("description"),
                        readme
                    )
            
            repository = Repository(
                id=repo["id"],
                name=repo["name"],
                full_name=repo["full_name"],
                description=repo.get("description"),
                html_url=repo["html_url"],
                stargazers_count=repo["stargazers_count"],
                forks_count=repo["forks_count"],
                language=repo.get("language"),
                topics=repo.get("topics", []),
                created_at=repo["created_at"],
                updated_at=repo["updated_at"],
                homepage=repo.get("homepage"),
                ai_summary=ai_summary
            )
            repositories.append(repository)
        
        return GenerateResponse(
            success=True,
            user=user_profile,
            repositories=repositories,
            message=f"Successfully generated website for {username}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Vercel handler
handler = Mangum(app, lifespan="off")


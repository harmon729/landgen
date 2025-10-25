"""
LandGen API - FastAPI Backend
Generate personal websites from GitHub profiles
"""

import os
from pathlib import Path
from typing import List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="LandGen API",
    description="AI-powered personal website generator",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP - in production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
# load_dotenv(Path(__file__).parent.parent / ".env.local")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class GenerateRequest(BaseModel):
    """Request model for website generation"""

    username: str


class Repository(BaseModel):
    """Repository data model"""

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
    """GitHub user profile model"""

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
    """Response model for generated website"""

    success: bool
    user: UserProfile
    repositories: List[Repository]
    message: str


async def fetch_github_user(username: str) -> dict:
    """Fetch GitHub user profile"""
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}", headers=headers, timeout=10.0
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"GitHub user '{username}' not found"
            )
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"GitHub API error: {response.text}",
            )

        return response.json()


async def fetch_github_repos(username: str, max_repos: int = 6) -> List[dict]:
    """Fetch user's top repositories"""
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        # Fetch all repos, sorted by stars
        response = await client.get(
            f"https://api.github.com/users/{username}/repos",
            headers=headers,
            params={"sort": "updated", "direction": "desc", "per_page": max_repos},
            timeout=10.0,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch repositories: {response.text}",
            )

        return response.json()


async def fetch_readme(username: str, repo_name: str) -> Optional[str]:
    """Fetch repository README content"""
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.github.com/repos/{username}/{repo_name}/readme",
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 200:
                # Limit README size to prevent token overflow
                readme_text = response.text
                return readme_text[:2000] if len(readme_text) > 2000 else readme_text

            return None
        except Exception:
            return None


async def generate_ai_summary(
    repo_name: str, description: Optional[str], readme: Optional[str]
) -> Optional[str]:
    """Generate AI summary using Gemini"""
    if not GEMINI_API_KEY:
        return None
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        model = "gemini-2.5-flash"
        # Prepare context for AI
        context = f"Repository: {repo_name}\n"
        if description:
            context += f"Description: {description}\n"
        if readme:
            context += f"README excerpt:\n{readme}\n"

        # Generate summary using Gemini
        prompt = f"""Based on the following GitHub repository information, write a concise 50-word summary that highlights the key features and purpose of this project. Be clear, technical, and engaging.

{context}

Summary (max 50 words):"""

        response = client.models.generate_content(model=model, contents=prompt)
        print(f"API Response: {response}")
        print(f"Response type: {type(response)}")
        print(f"Response text: {response.text}")
        summary = response.text.strip()

        # Ensure it's not too long
        words = summary.split()
        if len(words) > 60:
            summary = " ".join(words[:60]) + "..."

        return summary

    except Exception as e:
        print(f"AI summary generation failed: {e}")
        return None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "LandGen API is running", "version": "0.1.0"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_website(request: GenerateRequest):
    """
    Generate a personal website from GitHub username

    This endpoint:
    1. Fetches user profile from GitHub
    2. Fetches top repositories
    3. Generates AI summaries for repos (if README available)
    4. Returns structured data for frontend rendering
    """
    username = request.username.strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    try:
        # Step 1: Fetch user profile
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
            created_at=user_data["created_at"],
        )

        # Step 2: Fetch repositories
        repos_data = await fetch_github_repos(username)

        # Step 3: Process repositories and generate AI summaries
        repositories = []
        for repo in repos_data:
            # Fetch README for the first repo only (to save time in MVP)
            readme = None
            ai_summary = None

            if len(repositories) == 0 and GEMINI_API_KEY:  # Only for first repo
                readme = await fetch_readme(username, repo["name"])
                if readme:
                    ai_summary = await generate_ai_summary(
                        repo["name"], repo.get("description"), readme
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
                ai_summary=ai_summary,
            )
            repositories.append(repository)

        return GenerateResponse(
            success=True,
            user=user_profile,
            repositories=repositories,
            message=f"Successfully generated website for {username}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

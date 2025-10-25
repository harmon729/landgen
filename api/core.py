"""
LandGen API - Core Business Logic
Shared functions for GitHub API and AI summary generation
"""

import os
from typing import List, Optional

import httpx
from fastapi import HTTPException
from google import genai
from pydantic import BaseModel

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# Pydantic Models
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


# GitHub API Functions
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
                readme_text = response.text
                return readme_text[:2000] if len(readme_text) > 2000 else readme_text

            return None
        except Exception:
            return None


# AI Summary Generation
async def generate_ai_summary(
    repo_name: str, description: Optional[str], readme: Optional[str]
) -> Optional[str]:
    """Generate AI summary using Gemini"""
    import sys

    if not GEMINI_API_KEY:
        return None

    try:
        context = f"Repository: {repo_name}\n"
        if description:
            context += f"Description: {description}\n"
        if readme:
            context += f"README excerpt:\n{readme}\n"

        client = genai.Client(api_key=GEMINI_API_KEY)
        # Try different models in order of preference (for v1beta API)
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.5-flash-lite",
        ]

        last_error = None
        for model in models_to_try:
            try:
                prompt = f"""Based on the following GitHub repository information, write a concise 50-word summary that highlights the key features and purpose of this project. Be clear, technical, and engaging.

{context}

Summary (max 50 words):"""

                response = client.models.generate_content(model=model, contents=prompt)
                summary = response.text.strip()

                # Ensure it's not too long
                words = summary.split()
                if len(words) > 60:
                    summary = " ".join(words[:60]) + "..."

                print(f"[OK] Used model: {model} for {repo_name}")
                sys.stdout.flush()
                return summary

            except Exception as model_error:
                last_error = model_error
                error_msg = str(model_error).replace("\n", " ")[:150]
                print(f"[ERROR] Model {model} failed: {error_msg}")
                sys.stdout.flush()
                continue

        # All models failed
        if last_error:
            error_msg = str(last_error).replace("\n", " ")[:150]
            print(f"[WARN] AI summary generation failed (all models): {error_msg}")
            sys.stdout.flush()
        return None

    except Exception as e:
        error_msg = str(e).replace("\n", " ")[:150]
        print(f"[WARN] AI summary generation error: {error_msg}")
        sys.stdout.flush()
        return None


# Main Business Logic
async def process_generate_request(username: str) -> GenerateResponse:
    """
    Main business logic for generating website

    This function:
    1. Fetches user profile from GitHub
    2. Fetches top repositories
    3. Generates AI summaries for repos (if README available)
    4. Returns structured data for frontend rendering
    """
    username = username.strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    try:
        print(f"[START] Processing request for user: {username}")
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

        # Step 3: Process repositories and generate AI summaries (in parallel)
        repositories = []
        ai_summaries_count = 0
        max_ai_summaries = 6  # Limit AI summaries to first 6 repos for performance

        # Collect repos that need AI summaries
        ai_tasks = []
        for i, repo in enumerate(repos_data):
            if i < max_ai_summaries and GEMINI_API_KEY:
                ai_tasks.append((i, repo))

        # Generate AI summaries in parallel
        ai_results = {}
        if ai_tasks:
            import asyncio
            import sys

            print(
                f"[INFO] Starting parallel AI generation for {len(ai_tasks)} repositories..."
            )
            sys.stdout.flush()

            async def get_ai_summary_for_repo(index, repo):
                try:
                    print(
                        f"[INFO] [{index + 1}/{len(ai_tasks)}] Fetching README for {repo['name']}"
                    )
                    sys.stdout.flush()

                    readme = await fetch_readme(username, repo["name"])
                    if readme:
                        print(
                            f"[INFO] [{index + 1}/{len(ai_tasks)}] Generating AI summary for {repo['name']}"
                        )
                        sys.stdout.flush()

                        summary = await generate_ai_summary(
                            repo["name"], repo.get("description"), readme
                        )

                        if summary:
                            print(
                                f"[OK] [{index + 1}/{len(ai_tasks)}] AI summary generated for {repo['name']}"
                            )
                            sys.stdout.flush()

                        return (index, summary)
                    else:
                        print(
                            f"[SKIP] [{index + 1}/{len(ai_tasks)}] No README found for {repo['name']}"
                        )
                        sys.stdout.flush()
                except Exception as e:
                    print(
                        f"[WARN] [{index + 1}/{len(ai_tasks)}] Failed AI summary for {repo['name']}: {str(e)[:100]}"
                    )
                    sys.stdout.flush()
                return (index, None)

            # Run AI generation tasks in parallel
            results = await asyncio.gather(
                *[get_ai_summary_for_repo(i, repo) for i, repo in ai_tasks],
                return_exceptions=True,
            )

            for result in results:
                if isinstance(result, tuple) and result[1]:
                    ai_results[result[0]] = result[1]
                    ai_summaries_count += 1

            print(
                f"[INFO] Completed: {ai_summaries_count}/{len(ai_tasks)} AI summaries generated successfully"
            )
            sys.stdout.flush()

        # Build repository list with AI summaries
        for i, repo in enumerate(repos_data):
            ai_summary = ai_results.get(i)

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

        print(
            f"[INFO] Generated {ai_summaries_count} AI summaries out of {len(repositories)} repositories"
        )

        return GenerateResponse(
            success=True,
            user=user_profile,
            repositories=repositories,
            message=f"Successfully generated website for {username}",
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        print(f"[ERROR] Exception in process_generate_request: {error_details}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

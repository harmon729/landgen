/**
 * Type definitions for LandGen
 */

export interface Repository {
  id: number
  name: string
  full_name: string
  description: string | null
  html_url: string
  stargazers_count: number
  forks_count: number
  language: string | null
  topics: string[]
  created_at: string
  updated_at: string
  homepage: string | null
  ai_summary: string | null
}

export interface UserProfile {
  login: string
  name: string | null
  avatar_url: string
  bio: string | null
  location: string | null
  email: string | null
  blog: string | null
  twitter_username: string | null
  public_repos: number
  followers: number
  following: number
  created_at: string
}

export interface GenerateResponse {
  success: boolean
  user: UserProfile
  repositories: Repository[]
  message: string
}


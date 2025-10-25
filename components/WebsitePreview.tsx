'use client'

import Image from 'next/image'
import { GenerateResponse } from '@/types'

interface WebsitePreviewProps {
  data: GenerateResponse
  onReset: () => void
}

export default function WebsitePreview({ data, onReset }: WebsitePreviewProps) {
  const { user, repositories } = data

  return (
    <div className="max-w-6xl mx-auto">
      {/* Action Bar */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            ✨ Your Website is Ready!
          </h2>
          <p className="text-gray-600">
            Here's a preview of your generated personal website
          </p>
        </div>
        <button
          onClick={onReset}
          className="px-6 py-3 bg-white border-2 border-gray-300 rounded-xl font-semibold hover:border-gray-400 transition-all flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Generate Another
        </button>
      </div>

      {/* Website Preview */}
      <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border border-gray-200">
        {/* Hero Section */}
        <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 p-12 text-white">
          <div className="flex items-center gap-8">
            <Image
              src={user.avatar_url}
              alt={user.name || user.login}
              width={150}
              height={150}
              className="rounded-full border-4 border-white shadow-2xl"
            />
            <div className="flex-1">
              <h1 className="text-5xl font-bold mb-2">
                {user.name || user.login}
              </h1>
              <p className="text-xl text-blue-100 mb-4">
                @{user.login}
              </p>
              {user.bio && (
                <p className="text-lg text-white/90 mb-4 max-w-2xl">
                  {user.bio}
                </p>
              )}
              <div className="flex gap-6 text-sm">
                {user.location && (
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {user.location}
                  </div>
                )}
                {user.blog && (
                  <a href={user.blog.startsWith('http') ? user.blog : `https://${user.blog}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:underline">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                    Website
                  </a>
                )}
                {user.twitter_username && (
                  <a href={`https://twitter.com/${user.twitter_username}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:underline">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
                    </svg>
                    @{user.twitter_username}
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-8 flex gap-8 text-center">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">{user.public_repos}</div>
              <div className="text-sm text-blue-100">Repositories</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">{user.followers}</div>
              <div className="text-sm text-blue-100">Followers</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-4">
              <div className="text-3xl font-bold">{user.following}</div>
              <div className="text-sm text-blue-100">Following</div>
            </div>
          </div>
        </div>

        {/* Projects Section */}
        <div className="p-12">
          <h2 className="text-3xl font-bold mb-8 text-gray-900">
            Featured Projects
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            {repositories.map((repo) => (
              <div
                key={repo.id}
                className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow bg-gradient-to-br from-white to-gray-50"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <a
                      href={repo.html_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xl font-semibold text-blue-600 hover:text-blue-700 hover:underline inline-flex items-center gap-2"
                    >
                      {repo.name}
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  </div>
                </div>

                {/* AI Summary (if available) */}
                {repo.ai_summary && (
                  <div className="mb-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      <div>
                        <p className="text-sm font-semibold text-purple-900 mb-1">AI Summary</p>
                        <p className="text-sm text-purple-800">{repo.ai_summary}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Description */}
                {repo.description && (
                  <p className="text-gray-700 mb-4">
                    {repo.description}
                  </p>
                )}

                {/* Topics */}
                {repo.topics.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {repo.topics.slice(0, 5).map((topic) => (
                      <span
                        key={topic}
                        className="px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                )}

                {/* Stats */}
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  {repo.language && (
                    <div className="flex items-center gap-1">
                      <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                      {repo.language}
                    </div>
                  )}
                  <div className="flex items-center gap-1">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                    {repo.stargazers_count}
                  </div>
                  <div className="flex items-center gap-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                    </svg>
                    {repo.forks_count}
                  </div>
                </div>

                {/* Homepage link */}
                {repo.homepage && (
                  <a
                    href={repo.homepage}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-4 inline-flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700 font-medium"
                  >
                    View Demo
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Success message */}
      <div className="mt-8 bg-green-50 border border-green-200 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <svg className="w-6 h-6 text-green-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 className="font-semibold text-green-900 mb-1">
              Website Generated Successfully!
            </h3>
            <p className="text-sm text-green-800">
              This is a preview of what your personal website could look like. In the full version (V1), 
              you'll be able to deploy this to your own subdomain and keep it automatically updated!
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}


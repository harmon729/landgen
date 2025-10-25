'use client';

import React, { useState } from 'react';
import axios from 'axios';
import GeneratorForm from '@/components/GeneratorForm';
import WebsitePreview from '@/components/WebsitePreview';
import type { GenerateResponse } from '@/types';

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (username: string) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // In development, call backend directly (with CORS support)
      // In production, use Vercel routes (/api/generate -> api/generate.py)
      const apiUrl = process.env.NODE_ENV === 'development' 
        ? 'http://localhost:8000/api/generate'
        : '/api/generate'

      // Call our API endpoint
      const response = await axios.post<GenerateResponse>(
        apiUrl,
        { username },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 600000, // 10 minute timeout
        }
      )

      setResult(response.data)
    } catch (err: any) {
      console.error('Error generating website:', err)
      
      if (err.response?.status === 404) {
        setError(`GitHub user "${username}" not found. Please check the username and try again.`)
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timed out. Please try again.')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Failed to generate website. Please try again later.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">L</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  LandGen
                </h1>
                <p className="text-xs text-gray-500">AI-Powered Website Generator</p>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              v0.1 MVP
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        {!result ? (
          <>
            {/* Hero Section */}
            <div className="text-center mb-12 max-w-3xl mx-auto">
              <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Transform Your GitHub Into a Beautiful Portfolio
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Enter your GitHub username and let AI generate a stunning personal website in seconds.
                No coding required.
              </p>
              
              {/* Features */}
              <div className="grid md:grid-cols-3 gap-6 mb-12">
                <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Instant Generation</h3>
                  <p className="text-sm text-gray-600">Generate in seconds, not hours</p>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">AI-Powered</h3>
                  <p className="text-sm text-gray-600">Smart summaries by Gemini AI</p>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <svg className="w-6 h-6 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Beautiful Design</h3>
                  <p className="text-sm text-gray-600">Modern, responsive layouts</p>
                </div>
              </div>
            </div>

            {/* Generator Form */}
            <GeneratorForm 
              onGenerate={handleGenerate}
              loading={loading}
              error={error}
            />
          </>
        ) : (
          /* Website Preview */
          <WebsitePreview 
            data={result}
            onReset={handleReset}
          />
        )}
      </div>

      {/* Footer */}
      <footer className="border-t bg-white/50 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Built with ❤️ by <span className="font-semibold">Harmon Hsu</span>
            </p>
            <p className="text-sm text-gray-500">
              Powered by Next.js, FastAPI, and Google Gemini AI
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}


import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { searchAPI } from '../api'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalCandidates: 0,
    totalJobs: 0,
    recentMatches: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [candidates, jobs] = await Promise.all([
        searchAPI.searchCandidates({ limit: 1000 }),
        searchAPI.searchJobs({ limit: 1000 }),
      ])
      
      setStats({
        totalCandidates: candidates.length,
        totalJobs: jobs.length,
        recentMatches: 0, // TODO: Add match history endpoint
      })
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ icon, title, value, color }) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
          <p className={`text-3xl font-bold mt-2 ${color}`}>{value}</p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  )

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Welcome to your AI-powered recruitment platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon="👥"
          title="Total Candidates"
          value={loading ? '...' : stats.totalCandidates}
          color="text-blue-600 dark:text-blue-400"
        />
        <StatCard
          icon="💼"
          title="Active Jobs"
          value={loading ? '...' : stats.totalJobs}
          color="text-green-600 dark:text-green-400"
        />
        <StatCard
          icon="🎯"
          title="Matches Today"
          value={loading ? '...' : stats.recentMatches}
          color="text-purple-600 dark:text-purple-400"
        />
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/upload"
            className="flex items-center space-x-3 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 transition-colors"
          >
            <span className="text-2xl">📤</span>
            <div>
              <h3 className="font-semibold">Upload Resume</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Add new candidate profiles
              </p>
            </div>
          </Link>

          <Link
            to="/upload"
            className="flex items-center space-x-3 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 transition-colors"
          >
            <span className="text-2xl">💼</span>
            <div>
              <h3 className="font-semibold">Post Job</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Create new job posting
              </p>
            </div>
          </Link>

          <Link
            to="/matches"
            className="flex items-center space-x-3 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 transition-colors"
          >
            <span className="text-2xl">🎯</span>
            <div>
              <h3 className="font-semibold">Find Matches</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                AI-powered candidate matching
              </p>
            </div>
          </Link>

          <Link
            to="/search"
            className="flex items-center space-x-3 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 transition-colors"
          >
            <span className="text-2xl">🔍</span>
            <div>
              <h3 className="font-semibold">Search Database</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Filter candidates and jobs
              </p>
            </div>
          </Link>
        </div>
      </div>

      {/* Features Overview */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Platform Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex space-x-3">
            <span className="text-2xl">🧠</span>
            <div>
              <h3 className="font-semibold mb-1">AI-Powered Matching</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Semantic similarity using Sentence-BERT embeddings for accurate candidate-job matching
              </p>
            </div>
          </div>

          <div className="flex space-x-3">
            <span className="text-2xl">📄</span>
            <div>
              <h3 className="font-semibold mb-1">Smart Resume Parsing</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Automatic extraction of skills, experience, and education from PDF/DOCX files
              </p>
            </div>
          </div>

          <div className="flex space-x-3">
            <span className="text-2xl">⚡</span>
            <div>
              <h3 className="font-semibold mb-1">Real-time Analysis</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Instant similarity scores and skill overlap calculations
              </p>
            </div>
          </div>

          <div className="flex space-x-3">
            <span className="text-2xl">🔒</span>
            <div>
              <h3 className="font-semibold mb-1">Secure & Scalable</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                JWT authentication, PostgreSQL database, and production-ready architecture
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { searchAPI, matchAPI } from '../api'

export default function MatchesPage() {
  const [mode, setMode] = useState('candidate') // 'candidate' or 'job'
  const [candidates, setCandidates] = useState([])
  const [jobs, setJobs] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [topK, setTopK] = useState(10)
  const [minSimilarity, setMinSimilarity] = useState(50)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [candidatesData, jobsData] = await Promise.all([
        searchAPI.searchCandidates({ limit: 100 }),
        searchAPI.searchJobs({ limit: 100 }),
      ])
      setCandidates(candidatesData)
      setJobs(jobsData)
    } catch (error) {
      console.error('Error loading data:', error)
    }
  }

  const handleFindMatches = async () => {
    if (!selectedId) return

    setLoading(true)
    setMatches([])

    try {
      let result
      if (mode === 'candidate') {
        result = await matchAPI.matchCandidateToJobs(selectedId, {
          top_k: topK,
          min_similarity: minSimilarity / 100,
        })
      } else {
        result = await matchAPI.matchJobToCandidates(selectedId, {
          top_k: topK,
          min_similarity: minSimilarity / 100,
        })
      }
      setMatches(result.matches || [])
    } catch (error) {
      console.error('Error finding matches:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">AI Matching</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Find the best candidate-job matches using semantic similarity
        </p>
      </div>

      {/* Mode Selection */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Match Mode</h2>
        <div className="flex space-x-4">
          <button
            onClick={() => {
              setMode('candidate')
              setSelectedId('')
              setMatches([])
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              mode === 'candidate'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }`}
          >
            👤 Find Jobs for Candidate
          </button>
          <button
            onClick={() => {
              setMode('job')
              setSelectedId('')
              setMatches([])
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              mode === 'job'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }`}
          >
            💼 Find Candidates for Job
          </button>
        </div>
      </div>

      {/* Selection and Parameters */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">
          {mode === 'candidate' ? 'Select Candidate' : 'Select Job'}
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              {mode === 'candidate' ? 'Candidate' : 'Job'} *
            </label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="input-field"
            >
              <option value="">-- Select {mode === 'candidate' ? 'Candidate' : 'Job'} --</option>
              {mode === 'candidate'
                ? candidates.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} - {c.experience_years} years exp
                    </option>
                  ))
                : jobs.map((j) => (
                    <option key={j.id} value={j.id}>
                      {j.title} at {j.company}
                    </option>
                  ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Number of Matches
            </label>
            <input
              type="number"
              value={topK}
              onChange={(e) => setTopK(parseInt(e.target.value))}
              min="1"
              max="50"
              className="input-field"
            />
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Minimum Similarity: {minSimilarity}%
          </label>
          <input
            type="range"
            value={minSimilarity}
            onChange={(e) => setMinSimilarity(parseInt(e.target.value))}
            min="0"
            max="100"
            className="w-full"
          />
        </div>

        <button
          onClick={handleFindMatches}
          disabled={loading || !selectedId}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Finding Matches...' : '🎯 Find Matches'}
        </button>
      </div>

      {/* Results */}
      {matches.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">
            Top {matches.length} Matches
          </h2>
          
          <div className="space-y-4">
            {matches.map((match, index) => (
              <div
                key={index}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-primary-500 transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-lg">
                      {mode === 'candidate' ? match.job_title : match.candidate_name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {mode === 'candidate' 
                        ? `${match.company} • ${match.location}`
                        : `${match.experience_years} years experience • ${match.email}`
                      }
                    </p>
                  </div>
                  <div className="text-right">
                    <div
                      className={`text-2xl font-bold ${
                        match.similarity_score >= 80
                          ? 'text-green-600'
                          : match.similarity_score >= 60
                          ? 'text-yellow-600'
                          : 'text-gray-600'
                      }`}
                    >
                      {match.similarity_score.toFixed(1)}%
                    </div>
                    <p className="text-xs text-gray-500">Similarity</p>
                  </div>
                </div>

                {/* Skill Overlap */}
                {match.skill_overlap && (
                  <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="font-medium">Skill Overlap:</span>
                      <span className="text-primary-600 dark:text-primary-400">
                        {match.skill_overlap.overlap_percentage.toFixed(0)}% 
                        ({match.skill_overlap.overlap_count} skills)
                      </span>
                    </div>
                    
                    {match.skill_overlap.overlapping_skills.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {match.skill_overlap.overlapping_skills.map((skill) => (
                          <span
                            key={skill}
                            className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs rounded"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}

                    {match.skill_overlap.missing_skills.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">
                          Missing skills:
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {match.skill_overlap.missing_skills.map((skill) => (
                            <span
                              key={skill}
                              className="px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 text-xs rounded"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="card text-center py-8">
          <div className="text-4xl mb-4">🔄</div>
          <p className="text-gray-600 dark:text-gray-400">
            Analyzing embeddings and computing similarity scores...
          </p>
        </div>
      )}

      {!loading && matches.length === 0 && selectedId && (
        <div className="card text-center py-8">
          <div className="text-4xl mb-4">🔍</div>
          <p className="text-gray-600 dark:text-gray-400">
            No matches found. Try adjusting the minimum similarity threshold.
          </p>
        </div>
      )}
    </div>
  )
}

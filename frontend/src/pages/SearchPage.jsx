import { useState } from 'react'
import { searchAPI } from '../api'

export default function SearchPage() {
  const [searchMode, setSearchMode] = useState('candidates')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState([])

  // Candidate search filters
  const [candidateFilters, setCandidateFilters] = useState({
    name: '',
    skills: '',
    min_experience: '',
    max_experience: '',
  })

  // Job search filters
  const [jobFilters, setJobFilters] = useState({
    title: '',
    company: '',
    skills: '',
    location: '',
    job_type: '',
    seniority_level: '',
  })

  const handleSearch = async () => {
    setLoading(true)
    setResults([])

    try {
      let data
      if (searchMode === 'candidates') {
        data = await searchAPI.searchCandidates(candidateFilters)
      } else {
        data = await searchAPI.searchJobs(jobFilters)
      }
      setResults(data)
    } catch (error) {
      console.error('Error searching:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Search</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Filter and search through candidates and jobs
        </p>
      </div>

      {/* Search Mode Toggle */}
      <div className="card">
        <div className="flex space-x-4">
          <button
            onClick={() => {
              setSearchMode('candidates')
              setResults([])
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              searchMode === 'candidates'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }`}
          >
            👥 Search Candidates
          </button>
          <button
            onClick={() => {
              setSearchMode('jobs')
              setResults([])
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              searchMode === 'jobs'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }`}
          >
            💼 Search Jobs
          </button>
        </div>
      </div>

      {/* Search Filters */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Filters</h2>

        {searchMode === 'candidates' ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Name</label>
                <input
                  type="text"
                  value={candidateFilters.name}
                  onChange={(e) =>
                    setCandidateFilters({ ...candidateFilters, name: e.target.value })
                  }
                  className="input-field"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Skills (comma-separated)</label>
                <input
                  type="text"
                  value={candidateFilters.skills}
                  onChange={(e) =>
                    setCandidateFilters({ ...candidateFilters, skills: e.target.value })
                  }
                  className="input-field"
                  placeholder="Python, React, Machine Learning"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Min Experience (years)</label>
                <input
                  type="number"
                  value={candidateFilters.min_experience}
                  onChange={(e) =>
                    setCandidateFilters({ ...candidateFilters, min_experience: e.target.value })
                  }
                  className="input-field"
                  placeholder="0"
                  min="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Max Experience (years)</label>
                <input
                  type="number"
                  value={candidateFilters.max_experience}
                  onChange={(e) =>
                    setCandidateFilters({ ...candidateFilters, max_experience: e.target.value })
                  }
                  className="input-field"
                  placeholder="20"
                  min="0"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Job Title</label>
                <input
                  type="text"
                  value={jobFilters.title}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, title: e.target.value })
                  }
                  className="input-field"
                  placeholder="Python Developer"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Company</label>
                <input
                  type="text"
                  value={jobFilters.company}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, company: e.target.value })
                  }
                  className="input-field"
                  placeholder="TechCorp"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Skills (comma-separated)</label>
                <input
                  type="text"
                  value={jobFilters.skills}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, skills: e.target.value })
                  }
                  className="input-field"
                  placeholder="Python, FastAPI, AWS"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Location</label>
                <input
                  type="text"
                  value={jobFilters.location}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, location: e.target.value })
                  }
                  className="input-field"
                  placeholder="Remote"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Job Type</label>
                <select
                  value={jobFilters.job_type}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, job_type: e.target.value })
                  }
                  className="input-field"
                >
                  <option value="">All Types</option>
                  <option value="full-time">Full-time</option>
                  <option value="part-time">Part-time</option>
                  <option value="contract">Contract</option>
                  <option value="freelance">Freelance</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Seniority Level</label>
                <select
                  value={jobFilters.seniority_level}
                  onChange={(e) =>
                    setJobFilters({ ...jobFilters, seniority_level: e.target.value })
                  }
                  className="input-field"
                >
                  <option value="">All Levels</option>
                  <option value="junior">Junior</option>
                  <option value="mid">Mid-level</option>
                  <option value="senior">Senior</option>
                </select>
              </div>
            </div>
          </div>
        )}

        <button
          onClick={handleSearch}
          disabled={loading}
          className="btn-primary mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Searching...' : '🔍 Search'}
        </button>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">
            {results.length} Result{results.length !== 1 ? 's' : ''} Found
          </h2>

          <div className="space-y-4">
            {searchMode === 'candidates'
              ? results.map((candidate) => (
                  <div
                    key={candidate.id}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                  >
                    <h3 className="font-semibold text-lg">{candidate.name}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {candidate.email} • {candidate.experience_years} years experience
                    </p>
                    {candidate.skills && candidate.skills.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {candidate.skills.map((skill) => (
                          <span
                            key={skill}
                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              : results.map((job) => (
                  <div
                    key={job.id}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                  >
                    <h3 className="font-semibold text-lg">{job.title}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {job.company} • {job.location} • {job.job_type}
                    </p>
                    <p className="text-sm mt-2 text-gray-700 dark:text-gray-300">
                      {job.description.substring(0, 200)}...
                    </p>
                    {job.required_skills && job.required_skills.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {job.required_skills.map((skill) => (
                          <span
                            key={skill}
                            className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs rounded"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && (
        <div className="card text-center py-8">
          <div className="text-4xl mb-4">🔍</div>
          <p className="text-gray-600 dark:text-gray-400">
            No results found. Try adjusting your search filters.
          </p>
        </div>
      )}
    </div>
  )
}

import { useState } from 'react'
import { uploadAPI } from '../api'

export default function UploadPage() {
  const [activeTab, setActiveTab] = useState('resume')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  // Resume upload state
  const [resumeFile, setResumeFile] = useState(null)

  // Job upload state
  const [jobData, setJobData] = useState({
    title: '',
    company: '',
    description: '',
    location: 'Remote',
    job_type: 'full-time',
  })

  const handleResumeUpload = async (e) => {
    e.preventDefault()
    if (!resumeFile) return

    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      const result = await uploadAPI.uploadResume(resumeFile)
      setMessage({
        type: 'success',
        text: `Resume uploaded successfully! Candidate: ${result.name}`,
      })
      setResumeFile(null)
      e.target.reset()
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Failed to upload resume',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleJobUpload = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      const result = await uploadAPI.uploadJob(jobData)
      setMessage({
        type: 'success',
        text: `Job posted successfully! ${result.title} at ${result.company}`,
      })
      setJobData({
        title: '',
        company: '',
        description: '',
        location: 'Remote',
        job_type: 'full-time',
      })
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Failed to post job',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Upload</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Add candidates and job postings to the platform
        </p>
      </div>

      {/* Tabs */}
      <div className="flex space-x-4 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setActiveTab('resume')}
          className={`pb-2 px-4 transition-colors ${
            activeTab === 'resume'
              ? 'border-b-2 border-primary-600 text-primary-600 dark:text-primary-400'
              : 'text-gray-600 dark:text-gray-400'
          }`}
        >
          📄 Upload Resume
        </button>
        <button
          onClick={() => setActiveTab('job')}
          className={`pb-2 px-4 transition-colors ${
            activeTab === 'job'
              ? 'border-b-2 border-primary-600 text-primary-600 dark:text-primary-400'
              : 'text-gray-600 dark:text-gray-400'
          }`}
        >
          💼 Post Job
        </button>
      </div>

      {/* Message Display */}
      {message.text && (
        <div
          className={`p-4 rounded-lg ${
            message.type === 'success'
              ? 'bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800'
              : 'bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Resume Upload Form */}
      {activeTab === 'resume' && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Upload Candidate Resume</h2>
          <form onSubmit={handleResumeUpload} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Resume File (PDF or DOCX)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={(e) => setResumeFile(e.target.files[0])}
                className="input-field"
                required
              />
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                The system will automatically extract candidate information, skills, and experience.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading || !resumeFile}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Processing...' : 'Upload Resume'}
            </button>
          </form>
        </div>
      )}

      {/* Job Upload Form */}
      {activeTab === 'job' && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Post New Job</h2>
          <form onSubmit={handleJobUpload} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Job Title *</label>
                <input
                  type="text"
                  value={jobData.title}
                  onChange={(e) => setJobData({ ...jobData, title: e.target.value })}
                  className="input-field"
                  placeholder="Senior Python Developer"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Company *</label>
                <input
                  type="text"
                  value={jobData.company}
                  onChange={(e) => setJobData({ ...jobData, company: e.target.value })}
                  className="input-field"
                  placeholder="TechCorp Inc"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Job Description *</label>
              <textarea
                value={jobData.description}
                onChange={(e) => setJobData({ ...jobData, description: e.target.value })}
                className="input-field"
                rows="6"
                placeholder="We are looking for an experienced Python developer with expertise in FastAPI, machine learning, and cloud technologies..."
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Location</label>
                <input
                  type="text"
                  value={jobData.location}
                  onChange={(e) => setJobData({ ...jobData, location: e.target.value })}
                  className="input-field"
                  placeholder="Remote"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Job Type</label>
                <select
                  value={jobData.job_type}
                  onChange={(e) => setJobData({ ...jobData, job_type: e.target.value })}
                  className="input-field"
                >
                  <option value="full-time">Full-time</option>
                  <option value="part-time">Part-time</option>
                  <option value="contract">Contract</option>
                  <option value="freelance">Freelance</option>
                  <option value="internship">Internship</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Posting...' : 'Post Job'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}

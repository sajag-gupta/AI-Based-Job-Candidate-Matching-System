import api from './axios'

export const authAPI = {
  login: async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const response = await api.post('/auth/login', formData)
    return response.data
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  getCurrentUser: async (token) => {
    const response = await api.get('/auth/me', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
    return response.data
  },
}

export const uploadAPI = {
  uploadResume: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/upload/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  uploadJob: async (jobData) => {
    const response = await api.post('/upload/job', jobData)
    return response.data
  },
}

export const matchAPI = {
  matchCandidateToJobs: async (candidateId, params = {}) => {
    const response = await api.get(`/match/candidate/${candidateId}`, { params })
    return response.data
  },

  matchJobToCandidates: async (jobId, params = {}) => {
    const response = await api.get(`/match/job/${jobId}`, { params })
    return response.data
  },
}

export const searchAPI = {
  searchCandidates: async (params = {}) => {
    const response = await api.get('/search/candidates', { params })
    return response.data
  },

  searchJobs: async (params = {}) => {
    const response = await api.get('/search/jobs', { params })
    return response.data
  },
}

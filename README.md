# AI-Powered Job & Candidate Matching Platform

A production-ready, full-stack AI web application that leverages NLP and semantic embeddings to intelligently match candidates with job opportunities.

## 🌟 Features

### Core Functionality
- **Smart Resume Parsing**: Automatically extract candidate information, skills, experience, and education from PDF/DOCX files
- **AI-Powered Matching**: Semantic similarity computation using Sentence-BERT embeddings for accurate candidate-job matching
- **Intelligent Job Classification**: Automatic categorization of jobs by domain and seniority level
- **Advanced Search & Filtering**: Filter candidates and jobs by skills, experience, location, and more
- **Real-time Similarity Scores**: Instant computation of match percentages with detailed skill overlap analysis

### Technical Highlights
- **Monorepo Architecture**: Single-port deployment with FastAPI serving React build
- **Secure Authentication**: JWT-based auth with role-based access control (Recruiter/Admin)
- **Production Database**: PostgreSQL (Neon Cloud) with connection pooling
- **Modern Frontend**: React 18 + TailwindCSS with dark mode support
- **API Documentation**: Auto-generated Swagger/OpenAPI docs at `/docs`
- **Robust Error Handling**: Unified error schema with correlation IDs and logging

## 🏗️ Architecture

```
/ai-job-matcher
├── backend/                    # Python FastAPI backend
│   ├── api/                   # API routes
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── upload.py         # Resume/job upload
│   │   ├── match.py          # Matching engine endpoints
│   │   ├── search.py         # Search & filter endpoints
│   │   └── schemas.py        # Pydantic models
│   ├── core/                 # Core utilities
│   │   ├── security.py       # JWT & password hashing
│   │   └── logging_config.py # Logging setup
│   ├── database/             # Database layer
│   │   ├── models.py         # SQLAlchemy models
│   │   └── connection.py     # DB connection
│   ├── services/             # Business logic
│   │   ├── nlp_service.py    # NLP utilities
│   │   ├── embedding_service.py  # Sentence-BERT
│   │   ├── matching_service.py   # Matching algorithm
│   │   ├── resume_parser.py  # Resume parsing
│   │   └── job_parser.py     # Job parsing
│   ├── config.py             # Pydantic settings
│   ├── main.py               # FastAPI app
│   └── init_db.py            # DB initialization script
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── api/              # API client
│   │   ├── store/            # Zustand state management
│   │   └── App.jsx           # Main app component
│   └── index.html
├── data/uploads/             # Uploaded resume files
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── package.json              # Node dependencies
└── README.md
```

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (Neon Cloud account configured)

## 🚀 Setup & Installation

### 1. Clone and Navigate
```bash
cd "E:\Workspace\projects\AI-powered Job & Candidate Matching Platform"
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python backend/init_db.py
```

### 3. Frontend Setup
```bash
# Install Node dependencies
npm install

# Build frontend for production
npm run build
```

## 🎯 Running the Application

### Development Mode

**Option 1: Run backend and frontend separately**

Terminal 1 (Backend):
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run FastAPI server
python backend/main.py
```

Terminal 2 (Frontend):
```bash
# Run Vite dev server with HMR
npm run dev
```

**Option 2: Single-port deployment (Production mode)**
```bash
# Build frontend
npm run build

# Run backend (serves frontend on same port)
python backend/main.py
```

The application will be available at:
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🔐 Default Credentials

```
Email: recruiter@jobmatcher.com
Password: recruiter123

Email: admin@jobmatcher.com
Password: admin123
```

## 📊 Database Schema

### Tables
- **users**: User accounts with JWT authentication
- **candidates**: Candidate profiles with parsed resume data
- **jobs**: Job postings with extracted requirements
- **embeddings**: Vector embeddings (384-dim Sentence-BERT)
- **match_results**: Cached matching results with similarity scores

## 🧠 AI/ML Pipeline

1. **Document Upload**: User uploads resume (PDF/DOCX)
2. **Text Extraction**: PyPDF2/python-docx extracts raw text
3. **NLP Processing**: Extract skills, experience, education using regex and keyword matching
4. **Embedding Generation**: Sentence-BERT converts text to 384-dim vector
5. **Similarity Computation**: Cosine similarity between candidate and job embeddings
6. **Ranking**: Sort matches by similarity score with skill overlap analysis

### Model Details
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding Dimension**: 384
- **Similarity Metric**: Cosine similarity
- **Threshold**: Configurable (default: 50%)

## 🔧 Environment Variables

The `.env` file contains:
```env
# App Configuration
APP_NAME=AI_Job_Matcher
APP_ENV=production
DEBUG=False
PORT=8000

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://...

# AI/NLP Model
HUGGINGFACE_API_TOKEN=...
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIM=384

# Authentication
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Logging
LOG_LEVEL=INFO
```

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Upload
- `POST /upload/resume` - Upload and parse resume (PDF/DOCX)
- `POST /upload/job` - Upload job description

### Matching
- `GET /match/candidate/{id}` - Get top matching jobs for candidate
- `GET /match/job/{id}` - Get top matching candidates for job

### Search
- `GET /search/candidates` - Search candidates with filters
- `GET /search/jobs` - Search jobs with filters

## 🎨 Frontend Features

- **Responsive Design**: Mobile-friendly TailwindCSS layout
- **Dark Mode**: Automatic theme toggle
- **Real-time Updates**: Live similarity score calculation
- **Skill Visualization**: Color-coded skill overlap display
- **Intuitive UX**: Clean, modern interface with emoji icons

## 🧪 Testing

### Manual Testing
1. Login with demo credentials
2. Upload sample resume (PDF/DOCX)
3. Create job posting
4. Navigate to Matches page
5. Select candidate/job and click "Find Matches"
6. Review similarity scores and skill overlap

### API Testing
Visit http://localhost:8000/docs for interactive Swagger UI

## 📦 Deployment

### Single-Port Production Deployment

```bash
# 1. Build frontend
npm run build

# 2. Run backend (serves frontend automatically)
python backend/main.py
```

The FastAPI server will serve the built React app from `/frontend/dist` on port 8000.

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/
COPY .env .

# Copy frontend build
COPY frontend/dist/ ./frontend/dist/

# Create uploads directory
RUN mkdir -p data/uploads

EXPOSE 8000

CMD ["python", "backend/main.py"]
```

## 🔍 Troubleshooting

### Issue: Database connection error
**Solution**: Verify `DATABASE_URL` in `.env` and ensure Neon database is accessible

### Issue: Model download fails
**Solution**: Check internet connection and `HUGGINGFACE_API_TOKEN` in `.env`

### Issue: Frontend not loading
**Solution**: Run `npm run build` to ensure frontend is built before starting backend

### Issue: CORS errors
**Solution**: Ensure backend CORS middleware is configured (already set up in `main.py`)

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern async web framework
- **Sentence-BERT**: Semantic text embeddings
- **SQLAlchemy**: ORM for PostgreSQL
- **Pydantic**: Data validation
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **scikit-learn**: ML utilities

### Frontend
- **React 18**: UI library
- **TailwindCSS**: Utility-first CSS
- **Vite**: Build tool
- **Zustand**: State management
- **Axios**: HTTP client
- **React Router**: Navigation

### Database & Auth
- **PostgreSQL**: Primary database (Neon Cloud)
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing

## 📈 Performance Considerations

- **Connection Pooling**: SQLAlchemy pool (size: 10, overflow: 20)
- **Embedding Caching**: Stored in PostgreSQL for fast retrieval
- **Batch Processing**: Batch embedding generation for multiple documents
- **Async Routes**: Non-blocking FastAPI endpoints

## 🔒 Security

- JWT token expiration (60 minutes)
- Password hashing with bcrypt
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration
- Environment-based secrets

## 📝 License

This project is for educational and portfolio purposes.

## 👨‍💻 Author

Built as a demonstration of full-stack AI/ML engineering expertise.

---

**Questions?** Check `/docs` for interactive API documentation or review the inline code comments.

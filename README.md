# JobMarketIQ 🧠📊

**AI-powered Job Market & Salary Intelligence Platform**

JobMarketIQ is an end-to-end data science platform that analyzes job-market data to identify skill demand, salary trends, location opportunities, and personalized skill gaps. 

![Project Complete](https://img.shields.io/badge/Status-Complete-success)
![Python 3.13](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React+Vite-61DAFB)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E)

## 🎯 Features

1. **Skill Demand Analysis**: NLP-powered extraction of technical skills from job postings to highlight the most in-demand technologies across the Indian tech market.
2. **Salary Intelligence**: Machine Learning prediction model (RandomForest) to estimate salaries based on role, location, experience, and work mode. Achieved **R² = 0.98** and **MAE = 1.15 LPA**.
3. **Personalized Skill Gap Analyzer**: Compares a user's current tech stack against market requirements for a target role, highlighting missing high-value skills.
4. **Interactive Dashboard**: Modern, glassmorphism-styled React dashboard with Plotly charts visualizing geographic hotspots, remote work trends, and company hiring volumes.

## 🏗️ Architecture & Technology Stack

- **Data Processing**: Pandas, Python
- **NLP**: Regex-based token matching against a predefined skill dictionary
- **Database**: SQLite (SQLAlchemy ORM)
- **Machine Learning**: Scikit-learn (RandomForestRegressor)
- **Backend API**: FastAPI
- **Frontend**: React (Vite), Plotly.js, standard CSS (Dark theme + Glassmorphism)

## 📂 Project Structure

```
JobMarketIQ/
├── backend/            # FastAPI Application
│   ├── routers/        # API endpoints (analytics, jobs, salary, skills)
│   ├── main.py         # App entry point
│   └── schemas.py      # Pydantic models
├── data/               # Datasets
│   ├── processed/      # Cleaned CSVs used for database seeding
│   └── raw/            # Raw synthetic data
├── docs/               # Documentation
├── frontend/           # React + Vite Application
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Dashboard pages
│   │   ├── api.js      # API client wrappers
│   │   └── index.css   # Global design system
├── ml/                 # Machine Learning
│   ├── models/         # Trained model artifacts (.pkl)
│   ├── predict.py      # Inference logic
│   └── train.py        # Model training logic
├── scripts/            # Utilities
│   └── generate_dataset.py # Synthetic data generator
├── src/                # Core Data Pipeline
│   ├── analysis/       # Pandas-based analysis modules
│   ├── data/           # ETL and NLP skill extraction logic
│   └── database/       # SQLAlchemy models and SQLite connection
└── tests/              # Pytest unit tests
```

## 🚀 Getting Started

### 1. Backend Setup

```bash
# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the synthetic data generator
python scripts/generate_dataset.py

# Run the database seeder (also runs skill extraction)
python src/database/seed.py

# Train the ML model
python ml/train.py

# Start the FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to view the interactive dashboard. Visit `http://localhost:8000/docs` to view the FastAPI interactive API documentation.
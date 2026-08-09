"""
main.py
--------
FastAPI application entry point for JobMarketIQ.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import jobs, skills, salary, analytics

# ============================================================
# App configuration
# ============================================================

app = FastAPI(
    title="JobMarketIQ API",
    description="AI-powered Job Market & Salary Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================
# CORS — allow all origins for local dev (restrict in prod)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Routers
# ============================================================

app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(salary.router)
app.include_router(analytics.router)


# ============================================================
# Health check
# ============================================================

@app.get("/", tags=["health"])
def root():
    return {
        "service": "JobMarketIQ API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

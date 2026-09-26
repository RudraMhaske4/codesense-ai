from fastapi import FastAPI, HTTPException
from pathlib import Path
from backend.analyzer.repository_scanner import RepositoryScanner
from backend.analyzer.repository_metrics import RepositoryMetrics
app = FastAPI(
    title="CodeSense AI",
    description="AI-powered developer intelligence platform",
    version="0.2.0"
)
@app.get("/")
def home():
    return {
        "project": "CodeSense AI",
        "status": "running",
        "version": "0.2.0"
    }
@app.get("/health")
def health():
    return {"status": "healthy"}
@app.get("/analyze")
def analyze_repository():
    repository_path = Path("data/test_repository")
    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Test repository not found"
        )
    scanner = RepositoryScanner(repository_path)
    scan_results = scanner.scan()
    metrics = RepositoryMetrics(scan_results)
    summary = metrics.calculate()
    return {
        "repository": str(repository_path),
        "summary": summary,
        "files": scan_results
    }
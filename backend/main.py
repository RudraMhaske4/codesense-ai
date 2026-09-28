from pathlib import Path
from fastapi import FastAPI, HTTPException
from backend.analyzer.repository_scanner import RepositoryScanner
from backend.analyzer.repository_metrics import RepositoryMetrics
from backend.analyzer.risk_detector import RiskDetector
from backend.analyzer.quality_scorer import QualityScorer
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
@app.get("/risk-summary")
def risk_summary():
    repository_path = Path("data/test_repository")
    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Test repository not found"
        )
    scanner = RepositoryScanner(repository_path)
    scan_results = scanner.scan()
    detector = RiskDetector(scan_results)
    risks = detector.analyze()
    high_risks = [
        risk for risk in risks
        if risk["severity"] == "High"
    ]
    medium_risks = [
        risk for risk in risks
        if risk["severity"] == "Medium"
    ]
    return {
        "repository": str(repository_path),
        "total_risks": len(risks),
        "high_risks": len(high_risks),
        "medium_risks": len(medium_risks),
        "risk_details": risks
    }
@app.get("/quality-score")
def quality_score():
    repository_path = Path("data/test_repository")
    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Test repository not found"
        )
    scanner = RepositoryScanner(repository_path)
    scan_results = scanner.scan()
    detector = RiskDetector(scan_results)
    risks = detector.analyze()
    scorer = QualityScorer(risks)
    result = scorer.calculate()
    return {
        "repository": str(repository_path),
        **result
    }

@app.get("/repository-report")
def repository_report():
    repository_path = Path("data/test_repository")

    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Test repository not found"
        )
    scanner = RepositoryScanner(repository_path)
    scan_results = scanner.scan()
    metrics_calculator = RepositoryMetrics(scan_results)
    metrics = metrics_calculator.calculate()
    detector = RiskDetector(scan_results)
    risks = detector.analyze()
    scorer = QualityScorer(risks)
    quality = scorer.calculate()
    return {
        "repository": str(repository_path),
        "summary": {
            "files_analyzed": metrics["files_analyzed"],
            "total_lines_of_code": metrics["total_lines_of_code"],
            "total_functions": metrics["total_functions"],
            "total_classes": metrics["total_classes"]
        },
        "code_metrics": metrics,
        "risk_summary": {
            "total_risks": len(risks),
            "high_risks": quality["high_risks"],
            "medium_risks": quality["medium_risks"]
        },
        "quality": quality,
        "risk_details": risks
    }
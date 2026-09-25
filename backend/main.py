from fastapi import FastAPI 
app = FastAPI(
    title="CodeSense AI",
    description="AI-Powered Developer Intelligence Platform",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "project": "CodeSense AI",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
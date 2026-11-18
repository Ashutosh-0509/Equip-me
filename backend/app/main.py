from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api import contractor, provider, operator, officer, shared

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Unified API for BMC Heavy Logix: Contractor, Provider, Operator, and Officer domains."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contractor.router, prefix=settings.API_PREFIX)
app.include_router(provider.router, prefix=settings.API_PREFIX)
app.include_router(operator.router, prefix=settings.API_PREFIX)
app.include_router(officer.router, prefix=settings.API_PREFIX)
app.include_router(shared.router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "message": "BMC Heavy Logix Unified API is running",
        "docs_url": "/docs",
        "domains": ["contractor", "provider", "operator", "officer"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

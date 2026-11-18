import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api import contractor, provider, operator, officer, shared

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Unified API & Web Application for Equip-Me (BMC Heavy Logix): Contractor, Provider, Operator, and Officer domains."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Mount API routers under /api
app.include_router(contractor.router, prefix=settings.API_PREFIX)
app.include_router(provider.router, prefix=settings.API_PREFIX)
app.include_router(operator.router, prefix=settings.API_PREFIX)
app.include_router(officer.router, prefix=settings.API_PREFIX)
app.include_router(shared.router, prefix=settings.API_PREFIX)

# Direct health endpoint
@app.get("/api/health", tags=["Shared"])
def api_health():
    return {
        "status": "healthy",
        "service": "Equip-Me Unified Application",
        "version": settings.VERSION,
        "domains": ["contractor", "provider", "operator", "officer"],
    }

# 2. Frontend Production Build & Static File Serving with SPA Fallback
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    # Mount /assets if it exists
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    # Serve SPA or static files
    @app.get("/{full_path:path}")
    async def serve_spa_or_static(full_path: str, request: Request):
        # Allow API endpoints and docs to pass through
        if full_path.startswith("api") or full_path in ("docs", "redoc", "openapi.json"):
            return HTMLResponse(status_code=404, content="API route not found")

        # Static file check (e.g. favicon.ico, placeholder.svg, etc.)
        target_file = FRONTEND_DIST / full_path
        if full_path and target_file.is_file():
            return FileResponse(target_file)

        # SPA fallback for all client routes (/contractor, /provider, /operator, /officer, /login)
        index_file = FRONTEND_DIST / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)

        return HTMLResponse(
            "<h2>Equip-Me UI is loading...</h2>",
            status_code=200
        )
else:
    @app.get("/")
    def root():
        return {
            "message": "Equip-Me Unified API is running",
            "docs_url": "/docs",
            "domains": ["contractor", "provider", "operator", "officer"],
            "status": "Frontend build not detected. Run 'npm run build' inside frontend/ to serve the SPA."
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=True)

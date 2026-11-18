import os
import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn
from backend.app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Equip-Me Unified Application starting on http://{host}:{port}")
    print(f"📖 Swagger API Docs: http://{host}:{port}/docs")
    print(f"🖥️ Frontend UI: http://{host}:{port}/")
    uvicorn.run("main:app", host=host, port=port, reload=False)

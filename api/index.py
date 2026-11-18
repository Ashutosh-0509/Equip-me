import os
import sys
from pathlib import Path

# Ensure root repository directory is in Python path for Vercel Serverless
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app

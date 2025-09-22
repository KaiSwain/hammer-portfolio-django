"""
Settings package for Hammer Portfolio Django Backend

Auto-detects environment and loads appropriate settings:
- development: Local development with debug enabled
- production: Production deployment settings  
- testing: Test environment settings
"""

import os
from pathlib import Path

# Load .env file if it exists
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / '.env'

if env_file.exists():
    # Simple .env file parser
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Auto-detect which settings to use
environment = os.getenv('DJANGO_ENVIRONMENT', 'production')

if environment == 'development':
    from .development import *
    print(f"[SETTINGS] Loaded development settings")
elif environment == 'testing':
    from .testing import *
    print(f"[SETTINGS] Loaded testing settings")
else:
    from .production import *
    print(f"[SETTINGS] Loaded production settings")
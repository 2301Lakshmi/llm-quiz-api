import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required: set these in environment before starting
QUIZ_SECRET = "MONAHARINIR0802"
QUIZ_EMAIL = "22f1000912@ds.study.iitm.ac.in"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("ERROR: OPENAI_API_KEY is not set. Please add it to your .env file.")

# Timeouts (seconds)
TOTAL_WORK_TIMEOUT = 150  # keep < 180 (3min)
BROWSER_NAV_TIMEOUT = 90000  # ms for Playwright navigation
HTTP_TIMEOUT = 30  # seconds for http client
MAX_PAYLOAD_BYTES = 1 * 1024 * 1024  # 1MB

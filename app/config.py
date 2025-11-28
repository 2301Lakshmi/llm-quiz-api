# Required: set these in environment before starting
QUIZ_SECRET = "MONAHARINIR0802"
QUIZ_EMAIL = "22f1000912@ds.study.iitm.ac.in"
OPENAI_API_KEY = "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"  # optional, required if using OpenAI LLM

# Timeouts (seconds)
TOTAL_WORK_TIMEOUT = 150  # keep < 180 (3min)
BROWSER_NAV_TIMEOUT = 90000  # ms for Playwright navigation
HTTP_TIMEOUT = 30  # seconds for http client
MAX_PAYLOAD_BYTES = 1 * 1024 * 1024  # 1MB

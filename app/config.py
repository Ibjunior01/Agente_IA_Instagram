import os

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# SEGURANÇA DA API
# ============================================================

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError(
        "A variável de ambiente API_KEY não foi configurada."
    )


# ============================================================
# GOOGLE GEMINI
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "A variável de ambiente GEMINI_API_KEY não foi configurada."
    )


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

GEMINI_TIMEOUT_MS = int(
    os.getenv(
        "GEMINI_TIMEOUT_MS",
        "60000",
    )
)

GEMINI_TEMPERATURE = float(
    os.getenv(
        "GEMINI_TEMPERATURE",
        "0.75",
    )
)

GEMINI_MAX_OUTPUT_TOKENS = int(
    os.getenv(
        "GEMINI_MAX_OUTPUT_TOKENS",
        "600",
    )
)


# ============================================================
# VALIDAÇÃO DA API
# ============================================================

MAX_USER_ID_LENGTH = 128
MAX_MESSAGE_LENGTH = 4000


# ============================================================
# SERVIDOR
# ============================================================

PORT = int(
    os.getenv(
        "PORT",
        "5000",
    )
)
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

def project_root() -> Path:
    # Use the dir that contains .env if present; else fall back to repo root guess
    env_path = find_dotenv(".env", usecwd=True)
    return Path(env_path).parent if env_path else Path(__file__).resolve().parents[2]

def load_env_files() -> None:
    """
    Precedence (last wins):
      1) .env                         -> base defaults (do NOT override OS)
      2) OS environment               -> already set, remains (Bitbucket vars, exports, Makefile)
      3) .env.{ENVIRONMENT} (optional)-> developer-local overrides; DOES override OS + .env
    """
    root = project_root()

    # 1) Base .env (DO NOT override anything already in the OS)
    base = root / ".env"
    if base.exists():
        load_dotenv(dotenv_path=base, override=False)

    # ENVIRONMENT may come from OS (preferred) or from .env we just loaded
    env_name = (os.getenv("ENVIRONMENT") or "").strip()

    # 3) Developer-local overrides: .env.{ENVIRONMENT}, if present, WINS
    if env_name:
        # Support both ".env.prod" and "env.prod" naming, pick the first that exists
        for candidate in (root / f".env.{env_name}", root / f"env.{env_name}"):
            if candidate.exists():
                load_dotenv(dotenv_path=candidate, override=True)
                break

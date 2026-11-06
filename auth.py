"""
auth.py - YouTube Data API v3 Authentication Module
Cross-platform support for both Local Desktop and Headless Cloud VPS environments.
Handles Google OAuth 2.0 flow, token caching, and automatic token refresh.
"""

import os
import glob
import pickle
import logging
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger("YouTubeAutomation")

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload"
]

CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_PICKLE_FILE = "token.pickle"


def get_client_secret_path():
    """Finds the client secret json file if named differently."""
    if os.path.exists(CLIENT_SECRET_FILE):
        return CLIENT_SECRET_FILE
    matches = glob.glob("client_secret*.json")
    if matches:
        return matches[0]
    if os.path.exists("client_secrets.json"):
        return "client_secrets.json"
    return None


def get_authenticated_service(token_path=TOKEN_PICKLE_FILE):
    """
    Authenticates with YouTube Data API v3.
    VPS/CI Ready: If token.pickle exists or base64 token env var is set,
    uses refresh token silently in headless mode.
    """
    import base64
    creds = None

    # Fallback: Restore token.pickle from environment variable if missing or empty
    if (not os.path.exists(token_path) or os.path.getsize(token_path) == 0):
        b64_token = os.getenv("YOUTUBE_TOKEN_PICKLE_B64", "").strip()
        if b64_token:
            try:
                with open(token_path, "wb") as f:
                    f.write(base64.b64decode(b64_token))
                logger.info("Restored '%s' from YOUTUBE_TOKEN_PICKLE_B64 environment variable.", token_path)
            except Exception as e:
                logger.warning("Failed decoding YOUTUBE_TOKEN_PICKLE_B64: %s", e)

    # 1. Load cached credentials
    if os.path.exists(token_path) and os.path.getsize(token_path) > 100:
        try:
            with open(token_path, "rb") as token_file:
                creds = pickle.load(token_file)
            logger.info("Loaded credentials from '%s'.", token_path)
        except Exception as e:
            logger.warning("Could not read '%s': %s. Will re-authenticate.", token_path, e)
            creds = None

    # 2. Check validity and auto-refresh expired token
    if creds and creds.expired and creds.refresh_token:
        logger.info("Access token expired. Refreshing token silently...")
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_path, "wb") as token_file:
                pickle.dump(creds, token_file)
            logger.info("Access token successfully refreshed and saved.")
        except Exception as e:
            logger.error("Failed to auto-refresh token: %s", e)
            creds = None

    # 3. If credentials are still invalid, we need authorization
    if not creds or not creds.valid:
        secret_path = get_client_secret_path()
        if not secret_path:
            raise FileNotFoundError(
                f"Missing OAuth Client Secret JSON! Place 'client_secret.json' "
                f"or 'token.pickle' in: {os.path.abspath(os.curdir)}"
            )

        # Check if running in a headless VPS environment (no GUI browser)
        is_headless = os.name != "nt" and not os.environ.get("DISPLAY")

        if is_headless:
            print("\n" + "!" * 65)
            print("[HEADLESS VPS DETECTED]")
            print("Cannot open a web browser on this VPS directly.")
            print("EASY SOLUTION:")
            print(" 1. Run the script on your local PC once to generate 'token.pickle'.")
            print(" 2. Upload/copy 'token.pickle' to this VPS project folder.")
            print(" 3. Re-run on VPS. It will use 'token.pickle' automatically!")
            print("!" * 65 + "\n")
            raise SystemExit("Missing 'token.pickle' on headless server.")

        logger.info("Initiating OAuth2 browser login...")
        flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token_file:
            pickle.dump(creds, token_file)
        logger.info("New credentials saved to '%s'.", token_path)

    # 4. Build and return YouTube service
    return build("youtube", "v3", credentials=creds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    try:
        service = get_authenticated_service()
        print("[AUTH] Successfully connected to YouTube Data API!")
    except Exception as err:
        print(f"[AUTH ERROR] {err}")

import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# tokens
BOT_TOKEN = os.getenv("TOKEN_BOT")

base_url = os.getenv("BASE_URL")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

LANGS = ["en", "uz", "ru"]

# CHAT_ID = os.getenv("CHAT_ID")

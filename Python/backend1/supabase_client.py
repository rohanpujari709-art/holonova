from supabase import create_client, Client
from dotenv import load_dotenv
import os


# Get backend1 folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load .env from backend1/.env
load_dotenv(os.path.join(BASE_DIR, ".env"))


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


print("SUPABASE URL:", SUPABASE_URL)
print("KEY FOUND:", bool(SUPABASE_KEY))


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
from dotenv import load_dotenv 
import os 
load_dotenv()

DB_NAME = os.environ.get("DB_NAME") 
DB_USER = os.environ.get("DB_USER") 
DB_PASSWORD = os.environ.get("DB_PASSWORD")

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
CLIENT_ID = os.environ.get("CLIENT_ID")
LOGOUT_REDIRECT_URI = os.environ.get("LOGOUT_REDIRECT_URI")
SECRET_KEY = os.environ.get("SECRET_KEY")

BLACKLISTED_TOKENS = set()
import os
from dotenv import load_dotenv

load_dotenv()

# API
WP_API_URL: str = os.getenv('WP_API_URL', 'http://localhost:8000')
WP_API_USER: str = os.getenv('WP_API_USER', 'Firstname.Lastname')
WP_API_PASS: str = os.getenv('WP_API_PASS', '123-Test')

# DB
DB_HOST: str = os.getenv('DB_HOST', 'localhost')
DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
DB_NAME: str = os.getenv('DB_NAME', 'wordpress')
DB_USER: str = os.getenv('DB_USER', 'wordpress')
DB_PASS: str = os.getenv('DB_PASS', 'wordpress')

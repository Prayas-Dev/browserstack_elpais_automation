# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("KEY:", os.getenv("RAPIDAPI_KEY"))
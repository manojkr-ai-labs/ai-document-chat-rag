from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Read the model name
MODEL = os.getenv("MODEL")   

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
# BASE_URL = os.getenv("BASE_URL")
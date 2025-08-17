from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read MongoDB URI and DB Name from environment variables
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'job_ai_db')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Job AI backend running"}

# Example endpoint to add a user
@app.post("/user")
def add_user(user: dict):
    result = db.users.insert_one(user)
    return {"inserted_id": str(result.inserted_id)}

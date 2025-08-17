from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from model import User  # Import your model!
from job_models import Job
from notify import send_job_match

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'job_ai_db')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Job AI backend running"}

@app.post("/user")
def add_user(user: User):
    user_dict = user.dict()
    result = db.users.insert_one(user_dict)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/user/{name}")
def get_user(name: str):
    user = db.users.find_one({"name": name})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user
    return {"error": "User not found"}

@app.get("/users")
def list_users():
    users = [dict(u, _id=str(u['_id'])) for u in db.users.find()]
    return users

@app.post("/jobs")
def add_job(job: Job):
    job_dict = job.dict()
    result = db.jobs.insert_one(job_dict)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/jobs")
def list_jobs():
    jobs = [dict(j, _id=str(j["_id"])) for j in db.jobs.find()]
    return jobs

@app.get("/job/{job_id}")
def get_job(job_id: str):
    from bson import ObjectId
    job = db.jobs.find_one({"_id": ObjectId(job_id)})
    if job:
        job['_id'] = str(job['_id'])
        return job
    return {"error": "Job not found"}

@app.get("/match_jobs/{user_name}")
def match_jobs_for_user(user_name: str):
    user = db.users.find_one({"name": user_name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user_skills = set(user.get("skills", []))
    user_prefs = set(user.get("preferences", []))
    print("user_skills:"+ str(user_skills))
    print("user_prefs:"+ str(user_prefs))
    matched_jobs = []
    for job in db.jobs.find():
        job_skills = set(job.get("skills_required", []))
        job_location = job.get("location", "")
        score = len(user_skills & job_skills)
        print("job_skills:"+ str(job_skills))
        print("job_location:"+ str(job_location))
        print("score:"+ str(score))

        # Optional: quick preference filter
        if user_prefs and job_location not in user_prefs:
            continue
        if score > 0:
            job["_id"] = str(job["_id"])
            job["match_score"] = score
            matched_jobs.append(job)
        print("matched_jobs:"+ str(matched_jobs))
    # Sort by match_score, descending
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    send_job_match(user_name, matched_jobs)
    return matched_jobs

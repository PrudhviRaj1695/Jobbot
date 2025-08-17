import schedule
import time
from notify import send_job_match
from main import db  # re-use your DB connection

def run_daily_matches():
    users = db.users.find({"telegram_chat_id": {"$exists": True}})
    for user in users:
        user_name = user["name"]
        # You may want to import and use your match_jobs_for_user logic here
        user_skills = set(user.get("skills", []))
        user_prefs = set(user.get("preferences", []))
        matched_jobs = []
        for job in db.jobs.find():
            job_skills = set(job.get("skills_required", []))
            job_location = job.get("location", "")
            score = len(user_skills & job_skills)
            if user_prefs and job_location not in user_prefs:
                continue
            if score > 0:
                job['_id'] = str(job['_id'])
                job["match_score"] = score
                matched_jobs.append(job)
        matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        send_job_match(user_name, matched_jobs)

schedule.every().day.at("08:00").do(run_daily_matches)

print("Scheduler started, waiting for jobs...")
while True:
    schedule.run_pending()
    time.sleep(30)

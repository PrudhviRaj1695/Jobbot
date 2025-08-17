import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'job_ai_db')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(chat_id: str, text: str):
    # """Send a Telegram message via raw API (with debug logging)."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    # print("Telegram API response:", response.json())  # 👈 debug output
    return response.json()

def send_job_match(user_name: str, jobs: list):
    """Find user in DB and send job matches to their Telegram."""
    user = db.users.find_one({"name": user_name})
    if not user:
        print(f"User {user_name} not found in DB")
        return

    chat_id = user.get('telegram_chat_id')
    if not chat_id:
        print(f"No Telegram chat ID for {user_name}")
        return

    if not jobs:
        message = "No matched jobs found for you today."
        send_telegram_message(chat_id, message)  # use raw API
        return

    for job in jobs:
        print("Sending message in Telegram...")
        message = (
            f"🚀 New job match!\n"
            f"Title: {job['title']}\n"
            f"Company: {job['company']}\n"
            f"Location: {job.get('location', '')}\n"
            f"Skills: {', '.join(job.get('skills_required', []))}\n"
            f"Link: {job.get('link', '')}\n"
        )
        send_telegram_message(chat_id, message)  # use raw API

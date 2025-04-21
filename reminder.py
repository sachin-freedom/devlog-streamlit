# reminder_debug.py

import schedule
import time
from pymongo import MongoClient
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# 🧠 MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client["devlog"]
users = db["users"]
logs = db["logs"]

# 📧 Email Credentials
MY_EMAIL = "wisdomwithlife@gmail.com"
MY_PASSWORD = "axav hxzi xesz fnwx"

# 🔔 Email Reminder Function
def send_reminder_email(to_email, name):
    try:
        msg = MIMEText(f"Hi {name},\n\nDon't forget to submit your DevLog today before midnight!")
        msg["Subject"] = "🔔 Daily Log Reminder - DevLog"
        msg["From"] = MY_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(MY_EMAIL, MY_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

# 🔄 Check who hasn’t submitted today's log
def daily_log_check():
    today = datetime.now().strftime("%Y-%m-%d")
    devs = list(users.find({"role": "developer"}))
    print(f"🔍 Total Developers: {len(devs)} | Date: {today}")

    for dev in devs:
        username = dev.get("username")
        email = dev.get("email")

        log = logs.find_one({"username": username, "date": today})

        if not log:
            print(f"⛔ No log found for: {username}")
            if email:
                send_reminder_email(email, username)
            else:
                print(f"⚠️ No email for user: {username}")
        else:
            print(f"✅ Log already submitted by: {username}")

# ⏱️ Schedule for daily 10 PM
schedule.every().day.at("22:59").do(daily_log_check)

print("🚀 Scheduler started... (Ctrl+C to stop)")

# 🔧 Test immediately once
print("🧪 Running test log check now...")
daily_log_check()

# ⏳ Keep it running
while True:
    schedule.run_pending()
    time.sleep(60)


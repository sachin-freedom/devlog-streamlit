import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from db import users  # import users collection from your db connection file


# 📧 Email Credentials
MY_EMAIL = "wisdomwithlife@gmail.com"
MY_PASSWORD = "axav hxzi xesz fnwx"

def notify_manager(developer_name, tasks, mood, blockers):
    managers = users.find({"role": "manager"})
    
    for manager in managers:
        if "email" in manager:
            subject = f"📥 New Log Submitted by {developer_name}"
            body = f"""
Hi {manager['username']},

🧑‍💻 Developer {developer_name} just submitted their daily log.

📝 Tasks:
{tasks}

😊 Mood: {mood}
🚧 Blockers: {blockers if blockers else 'None'}

🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

You can now review and provide feedback in the dashboard.

- DevLog System
            """

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = MY_EMAIL
            msg["To"] = manager["email"]

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(MY_EMAIL, MY_PASSWORD)
                smtp.send_message(msg)
                print(f"✅ Notification sent to manager: {manager['email']}")

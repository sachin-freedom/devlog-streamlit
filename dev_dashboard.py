# dev_dashboard.py

import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from utils import notify_manager
from db import client, db, logs, users


# Mood options
mood_emojis = {
    "😄 Happy": "happy",
    "😐 Neutral": "neutral",
    "😔 Sad": "sad"
}

def dev_dashboard(user):
    st.subheader(f"👨‍💻 Welcome, {user['username']} (Developer)")

    # Daily Log Form
    with st.form("daily_log_form"):
        st.markdown("### ✍️ Submit Today's Log")
        task_details = st.text_area("Tasks Completed (Markdown Supported)")
        time_spent = st.number_input("Time Spent (in hours)", min_value=0.0, step=0.5)
        mood = st.radio("Your Mood Today", list(mood_emojis.keys()))
        blockers = st.text_area("Any Blockers? (Optional)")

        submitted = st.form_submit_button("Submit Log")
        if submitted:
            log = {
                "username": user["username"],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "task_details": task_details,
                "time_spent": time_spent,
                "mood": mood_emojis[mood],
                "blockers": blockers,
                "reviewed": False
            }
            logs.insert_one(log)
            # ✅ Notification bhejo manager ko
            notify_manager(
                developer_name = user["full_name"],
                tasks=task_details,
                mood=mood,
                blockers=blockers
            )
            st.success("✅ Log submitted successfully!")

    # View Previous Logs
    st.markdown("---")
    st.markdown("### 📅 Your Previous Logs")

    user_logs = list(logs.find({"username": user["username"]}).sort("date", -1))
    if user_logs:
        df = pd.DataFrame(user_logs)
        df = df[["date", "task_details", "time_spent", "mood", "blockers", "reviewed"]]
        st.dataframe(df)
    else:
        st.info("No logs found. Start by submitting one above.")

    # ✏️ Edit Previous Log
    st.markdown("---")
    st.markdown("### ✏️ Edit Previous Log")

    # Get log dates for the user
    log_dates = [log["date"] for log in user_logs]
    selected_date = st.selectbox("Select a date to edit log:", options=log_dates)

    if selected_date:
        selected_log = next((log for log in user_logs if log["date"] == selected_date), None)

        if selected_log:
            with st.form("edit_log_form"):
                task_details = st.text_area("Tasks Completed", value=selected_log["task_details"])
                time_spent = st.number_input("Time Spent (in hours)", min_value=0.0, step=0.5, value=selected_log["time_spent"])
                mood = st.radio("Your Mood", list(mood_emojis.keys()), 
                                index=list(mood_emojis.values()).index(selected_log["mood"]))
                blockers = st.text_area("Blockers", value=selected_log.get("blockers", ""))

                update_btn = st.form_submit_button("Update Log")
                if update_btn:
                    logs.update_one(
                        {"_id": selected_log["_id"]},
                        {"$set": {
                            "task_details": task_details,
                            "time_spent": time_spent,
                            "mood": mood_emojis[mood],
                            "blockers": blockers
                        }}
                    )
                    st.success("✅ Log updated successfully!")
                    st.rerun()
    from fpdf import FPDF
    from io import BytesIO

    # Weekly Export Section
    st.markdown("---")
    st.markdown("### 📊 Export Weekly Report")

    if st.button("📥 Export as CSV"):
        last_7_logs = logs.find({
            "username": user["username"],
            "date": {"$gte": (datetime.now() - pd.Timedelta(days=7)).strftime("%Y-%m-%d")}
        })
        df = pd.DataFrame(list(last_7_logs))
        df = df[["date", "task_details", "time_spent", "mood", "blockers"]]

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, file_name="weekly_devlog.csv", mime="text/csv")


    # Logout Button
    if st.button("Logout"):
        del st.session_state["user"]
        st.success("Logged out successfully!")
        st.rerun()

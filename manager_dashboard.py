# manager_dashboard.py

import streamlit as st
from pymongo import MongoClient
import pandas as pd
from db import client, db, logs, users


def manager_dashboard(user):
    st.subheader(f"👨‍💼 Welcome, {user['username']} (Manager)")
    st.markdown("### 📋 Team Logs")

    # Fetch developer usernames
    devs = [u["username"] for u in users.find({"role": "developer"})]

    # Filters
    selected_dev = st.selectbox("Select Developer", ["All"] + devs)
    selected_date = st.date_input("Filter by Date (optional)", None)

    query = {}
    if selected_dev != "All":
        query["username"] = selected_dev
    if selected_date:
        query["date"] = selected_date.strftime("%Y-%m-%d")

    results = list(logs.find(query).sort("date", -1))
    
    if results:
        for r in results:
            with st.expander(f"📅 {r['date']} | 👨‍💻 {r['username']}"):
                st.markdown(f"**Tasks Completed:**\n{r['task_details']}")
                st.markdown(f"**Time Spent:** {r['time_spent']} hours")
                st.markdown(f"**Mood:** {r['mood'].capitalize()}")
                st.markdown(f"**Blockers:** {r['blockers'] or 'None'}")
                st.markdown(f"**Reviewed:** {'✅ Yes' if r['reviewed'] else '❌ No'}")

                if not r['reviewed']:
                    if st.button(f"✅ Mark Reviewed - {r['_id']}", key=str(r['_id'])):
                        logs.update_one({"_id": r["_id"]}, {"$set": {"reviewed": True}})
                        st.success("Marked as reviewed. Refresh to see update.")
    else:
        st.info("No logs found for selected filters.")

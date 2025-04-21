# app.py
import streamlit as st
from auth import login_user
from dev_dashboard import dev_dashboard
from manager_dashboard import manager_dashboard

st.set_page_config(page_title="DevLog", layout="wide")
st.title("🧠 DevLog - Developer Productivity & Daily Log Tool")

# Role-based routing
user = login_user()
print("User session state:", user)  # Debugging line

if user:
    print("User session state:", user)  # Debugging line
    if user["role"] == "developer":
        dev_dashboard(user)
    elif user["role"] == "manager":
        manager_dashboard(user)

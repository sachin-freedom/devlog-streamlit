# auth.py

import streamlit as st
import bcrypt
import pymongo
from pymongo import MongoClient
from db import client, db, users


# Hashing functions
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Sign Up
def signup_user():
    st.subheader("👤 Create Account")
    username = st.text_input("Username")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["developer", "manager"])
    if st.button("Sign Up"):
        if users.find_one({"username": username}):
            st.warning("Username already exists.")
        else:
            hashed_pwd = hash_password(password)
            users.insert_one({"username": username,"full_name":full_name, "email": email, "password": hashed_pwd, "role": role})
            st.success("Account created! Please login.")

# Login & Logout Logic
def login_user():
    if "user" in st.session_state:
        st.sidebar.markdown(f"👋 Logged in as **{st.session_state['user']['username']}**")
        if st.sidebar.button("🚪 Logout"):
            del st.session_state["user"]
            st.rerun()
        return st.session_state["user"]

    menu = st.sidebar.selectbox("Login / Signup", ["Login", "Sign Up"])
    if menu == "Sign Up":
        signup_user()
        return None

    st.sidebar.subheader("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = users.find_one({"username": username})

        if user:
            print("User found:", user)  # Debugging line

        if user and verify_password(password, user["password"]):
            st.session_state["user"] = {
                "username": username,
                "role": user["role"],
                "full_name": user["full_name"]
            }
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    return st.session_state.get("user")


# # Login
# def login_user():
#     menu = st.sidebar.selectbox("Login / Signup", ["Login", "Sign Up"])
#     if menu == "Sign Up":
#         signup_user()
#         return None

#     st.sidebar.subheader("🔐 Login")
#     username = st.sidebar.text_input("Username")
#     password = st.sidebar.text_input("Password", type="password")
#     if st.sidebar.button("Login"):
#         user = users.find_one({"username": username})
        
#         if user:
#             print("User found:", user)  # Debugging line

#         if user and verify_password(password, user["password"]):
#             st.session_state["user"] = {"username": username, "role": user["role"], "full_name": user["full_name"]}
#             st.success(f"Welcome back, {username}!")
#             return st.session_state["user"]
#         else:
#             st.error("Invalid username or password.")
#     return st.session_state.get("user")

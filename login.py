import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Login - SEVORA", layout="wide")

user_file = "users.csv"
if not os.path.exists(user_file):
    pd.DataFrame(columns=["Name", "Contact", "Address"]).to_csv(user_file, index=False)

def user_exists(name):
    users = pd.read_csv(user_file)
    return name.strip().lower() in users["Name"].str.lower().values

def add_user(name, contact, address):
    new_user = pd.DataFrame([[name.strip(), contact.strip(), address.strip()]],
                            columns=["Name", "Contact", "Address"])
    new_user.to_csv(user_file, mode='a', index=False, header=False)

st.title("👤 Login or Sign Up")

name = st.text_input("Full Name (Login)")

if name:
    if user_exists(name):
        st.success(f"✅ Welcome back, {name}!")
        st.session_state.user = name
        st.switch_page("app.py")
    else:
        st.warning("🔐 No account found. Please sign up below.")
        full_name = st.text_input("Full Name (Signup)", key="signup_name")
        contact = st.text_input("📞 Contact", key="signup_contact")
        address = st.text_input("🏠 Address", key="signup_address")

        if st.button("Sign Up"):
            if not full_name or not contact or not address:
                st.error("❌ Fill in all fields.")
            elif not contact.isdigit():
                st.error("❌ Contact must be digits only.")
            else:
                add_user(full_name, contact, address)
                st.success(f"✅ Account created for {full_name}. Please login.")
                st.rerun()

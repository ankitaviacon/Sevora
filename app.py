import streamlit as st
import pandas as pd
import os
import random

# Streamlit config
st.set_page_config(page_title="SEVORA Fashion", layout="wide")

# Load external CSS
def load_local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_local_css("style.css")

# Inject navbar
st.markdown("""
    <div class="navbar">
        <h1>🛍️ SEVORA</h1>
        <div>
            <a href="#home">Home</a>
            <a href="#search">Search</a>
            <a href="#products">Products</a>
            <a href="#contact">Contact</a>
        </div>
    </div>
    <div class="content">
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("fashion_subset_1200.csv")
df['Product Description'] = df['Product Description'].fillna('')
df['Product Tags'] = df['Product Tags'].fillna('')
df['Product Image Url'] = df['Product Image Url'].fillna('https://via.placeholder.com/200x250.png?text=No+Image')
df['Product Rating'] = df['Product Rating'].fillna(0)
df['Product Category'] = df['Product Category'].fillna('Unknown')

# User management
user_file = "users.csv"
if not os.path.exists(user_file):
    pd.DataFrame(columns=["Name", "Contact", "Address"]).to_csv(user_file, index=False)

def user_exists(name):
    users = pd.read_csv(user_file)
    return name.strip().lower() in users["Name"].str.lower().values

def get_user(name):
    users = pd.read_csv(user_file)
    user_row = users[users["Name"].str.lower() == name.strip().lower()]
    return user_row.iloc[0] if not user_row.empty else None

def add_user(name, contact, address):
    new_user = pd.DataFrame([[name.strip(), contact.strip(), address.strip()]], columns=["Name", "Contact", "Address"])
    new_user.to_csv(user_file, mode='a', index=False, header=False)

# Sidebar login/signup
with st.sidebar:
    st.header("👤 Login or Sign Up")
    name = st.text_input("Full Name (Login)", key="login_name")

    if name:
        if user_exists(name):
            st.success(f"✅ Welcome back, {name}!")
            st.session_state.user = name
        else:
            st.warning("🔐 No account found. Please sign up below.")
            full_name = st.text_input("Full Name (Signup)", key="signup_full_name")
            contact = st.text_input("📞 Contact (Numbers Only)", key="signup_contact")
            address = st.text_input("🏠 Address", key="signup_address")

            if st.button("Sign Up"):
                if not full_name or not contact or not address:
                    st.error("❌ Please fill in all signup details.")
                elif not contact.isdigit():
                    st.error("❌ Contact number must contain digits only.")
                else:
                    add_user(full_name, contact, address)
                    st.success(f"✅ Account created for {full_name}!")
                    st.session_state.user = full_name
                    st.rerun()

# Title
st.title("🛍️ SEVORA — Your Fashion Companion")

# Search Bar
st.markdown("---")
query = st.text_input("🔎 Search for a product (e.g., 'jeans', 'shoes')")

if query:
    filtered_df = df[df['Product Name'].str.contains(query, case=False, na=False)].head(12)
    st.subheader(f"📦 Results for '{query}':")
else:
    filtered_df = df.sample(12)
    st.subheader("🔥 Trending Products:")

# Product Display Grid
num_cols = 4
for i in range(0, len(filtered_df), num_cols):
    row_data = filtered_df.iloc[i:i+num_cols]
    cols = st.columns(num_cols)
    for idx, (_, product) in enumerate(row_data.iterrows()):
        with cols[idx]:
            st.image(product['Product Image Url'], use_container_width=True)
            st.markdown(f"**🧥 {product['Product Name']}**")
            st.markdown(f"📂 *Category:* {product['Product Category']}")
            st.markdown(f"⭐ *Rating:* {product['Product Rating']}")
            st.markdown("---")

# Footer
st.markdown("""
<div class="footer">
    <strong>Need Help?</strong><br>
    <a href="#">Contact Us</a> |
    <a href="#">About</a> |
    <a href="#">Terms</a> |
    <a href="#">Privacy Policy</a><br><br>
    &copy; 2025 Try Before You Buy. All rights reserved.
</div>
""", unsafe_allow_html=True)

# app.py
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SEVORA — Try Before You Buy", layout="wide")


# Load custom CSS
def load_local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_local_css("style.css")

# Load user data
user_file = "users.csv"
if not os.path.exists(user_file):
    pd.DataFrame(columns=["Name", "Contact", "Address"]).to_csv(user_file, index=False)

def user_exists(name):
    users = pd.read_csv(user_file)
    return name.strip().lower() in users["Name"].str.lower().values

def add_user(name, contact, address):
    df = pd.DataFrame([[name.strip(), contact.strip(), address.strip()]], columns=["Name", "Contact", "Address"])
    df.to_csv(user_file, mode='a', header=False, index=False)

# Sidebar Login/Signup
with st.sidebar:
    st.header("🔐 Login / Sign Up")
    name = st.text_input("Your Name")
    if name:
        if user_exists(name):
            st.success(f"✅ Welcome back, {name}!")
            st.session_state.user = name
        else:
            st.info("👋 New here? Sign up below:")
            contact = st.text_input("📞 Contact")
            address = st.text_input("🏠 Address")
            if st.button("Sign Up"):
                if not contact or not address:
                    st.error("❌ Please fill in all details.")
                elif not contact.isdigit():
                    st.error("❌ Contact must be numbers only.")
                else:
                    add_user(name, contact, address)
                    st.success(f"✅ Account created for {name}!")
                    st.session_state.user = name
                    st.rerun()

# Load product data
df = pd.read_csv("fashion_subset_1200.csv")
df['Product Description'].fillna('', inplace=True)
df['Product Tags'].fillna('', inplace=True)
df['Product Image Url'].fillna('https://via.placeholder.com/200x250.png?text=No+Image', inplace=True)
df['Product Rating'].fillna(0, inplace=True)
df['Product Category'].fillna('Unknown', inplace=True)

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# UI
st.title("🛍️ Welcome to SEVORA — Try Before You Buy")

query = st.text_input("🔍 Search Products")
filtered_df = df[df["Product Name"].str.contains(query, case=False, na=False)].head(12) if query else df.sample(12)

st.subheader("🧾 Products Available:")

cols = st.columns(4)
for i, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[i % 4]:
        st.image(row["Product Image Url"], use_container_width=True)
        st.write(f"**{row['Product Name']}**")
        st.caption(f"📂 {row['Product Category']} | ⭐ {row['Product Rating']}")
        if st.button("Add to Cart", key=f"add_{i}"):
            if row.to_dict() not in st.session_state.cart:
                st.session_state.cart.append(row.to_dict())
                st.success("🛒 Added to cart")

# Optional: Show footer
st.markdown("""
<hr>
<center>
    <strong>Need Help?</strong><br>
    <a href="#">Contact Us</a> |
    <a href="#">About</a> |
    <a href="#">Terms</a> |
    <a href="#">Privacy Policy</a><br><br>
    &copy; 2025 SEVORA. All rights reserved.
</center>
""", unsafe_allow_html=True)

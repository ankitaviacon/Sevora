import streamlit as st

st.title("🛒 Your Cart")

if "cart" not in st.session_state or not st.session_state.cart:
    st.warning("Your cart is empty.")
else:
    for item in st.session_state.cart:
        with st.expander(item["Product Name"]):
            st.image(item["Product Image Url"], width=120)
            st.write(f"📂 Category: {item['Product Category']}")
            st.write(f"⭐ Rating: {item['Product Rating']}")
    st.page_link("pages/Booking.py", label="📅 Proceed to Booking")

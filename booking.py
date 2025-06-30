# pages/Booking.py

import streamlit as st
import datetime
from google_calendar import create_event

st.set_page_config(page_title="Trial Booking", layout="wide")
st.title("📅 Trial Booking for Your Cart Items")

# Ensure cart exists
if "cart" not in st.session_state or not st.session_state.cart:
    st.warning("🛒 Your cart is empty. Please add products before booking a trial.")
    st.stop()

now = datetime.datetime.now()
today = now.date()
min_booking_time = now + datetime.timedelta(minutes=40)

# Slot generator: returns list of (start, end) datetime.time pairs
def generate_slots(start_hour=10, end_hour=18):
    slots = []
    for hour in range(start_hour, end_hour):
        slots.append((datetime.time(hour, 0), datetime.time(hour, 30)))
        slots.append((datetime.time(hour, 30), datetime.time(hour + 1, 0)))
    return slots

# Booking for each product
for i, product in enumerate(st.session_state.cart):
    with st.expander(f"🧥 {product['Product Name']} — {product['Product Category']}"):
        st.image(product["Product Image Url"], width=200)

        selected_date = st.date_input(
            f"Select Date for {product['Product Name']}",
            min_value=today,
            key=f"date_{i}"
        )

        all_slots = generate_slots()
        valid_slots = []

        for start_time, end_time in all_slots:
            slot_start_dt = datetime.datetime.combine(selected_date, start_time)
            if slot_start_dt > min_booking_time:
                label = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                valid_slots.append((label, start_time, end_time))

        if not valid_slots:
            st.warning("❌ No valid slots available. Try a later date.")
            continue

        slot_labels = [slot[0] for slot in valid_slots]
        selected_label = st.selectbox(f"Available Time Slots for {product['Product Name']}", slot_labels, key=f"slot_{i}")

        selected_slot = next((slot for slot in valid_slots if slot[0] == selected_label), None)

        if st.button(f"✅ Book Trial for {product['Product Name']}", key=f"book_{i}"):
            start_dt = datetime.datetime.combine(selected_date, selected_slot[1])
            end_dt = datetime.datetime.combine(selected_date, selected_slot[2])
            if start_dt < min_booking_time:
                st.error("❌ Slot must be at least 40 minutes in the future.")
            else:
                # Optional: Create Google Calendar event
                create_event(product['Product Name'], start_dt.isoformat(), end_dt.isoformat())
                st.success(f"✅ Trial booked for **{product['Product Name']}** at **{selected_label}** on {selected_date.strftime('%d %b %Y')}")

# Optional: Book All button (optional logic)
if st.button("📅 Book All Trials"):
    any_booked = False
    for i, product in enumerate(st.session_state.cart):
        slot_key = f"slot_{i}"
        date_key = f"date_{i}"
        if slot_key in st.session_state and date_key in st.session_state:
            selected_label = st.session_state[slot_key]
            selected_date = st.session_state[date_key]
            slot_time = next((s for s in generate_slots() if f"{s[0].strftime('%H:%M')} - {s[1].strftime('%H:%M')}" == selected_label), None)
            if slot_time:
                start_dt = datetime.datetime.combine(selected_date, slot_time[0])
                end_dt = datetime.datetime.combine(selected_date, slot_time[1])
                if start_dt >= min_booking_time:
                    create_event(product['Product Name'], start_dt.isoformat(), end_dt.isoformat())
                    st.success(f"✅ Booked {product['Product Name']} at {selected_label} on {selected_date.strftime('%d %b %Y')}")
                    any_booked = True
    if not any_booked:
        st.warning("⚠️ No valid bookings made. Please check slot timings.")

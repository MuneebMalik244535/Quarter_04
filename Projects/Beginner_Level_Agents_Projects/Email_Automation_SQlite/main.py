import smtplib
from email.message import EmailMessage
import streamlit as st
import os
import sqlite3

# --- CREATE TABLE IF NOT EXISTS ---
def create_appointments_table():
    conn = sqlite3.connect("appointments.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            number TEXT,
            reason TEXT,
            date TEXT,
            time TEXT,
            slot TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# --- SAVE APPOINTMENT ---
def save_appointment(name, email, number, reason, date, time):
    slot = f"{date} {time}"
    try:
        conn = sqlite3.connect("appointments.db")
        c = conn.cursor()
        c.execute("INSERT INTO appointments (name, email, number, reason, date, time, slot) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  (name, email, str(number), reason, str(date), str(time), slot))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# --- VIEW ALL APPOINTMENTS ---
def get_all_appointments():
    conn = sqlite3.connect("appointments.db")
    c = conn.cursor()
    c.execute("SELECT name, email, number, reason, date, time FROM appointments ORDER BY date, time")
    data = c.fetchall()
    conn.close()
    return data

# --- EMAIL FUNCTION ---
def send_email(to_email: str, name: str, date: str, time: str , reason : str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Appointment Confirmation"
        msg["From"] = "aniqayan2@gmail.com"
        msg["To"] = to_email
        msg.set_content(
            f"Hello {name},\n\nI am Hafiz Muneeb, your assistant. Your appointment has been scheduled for:\n\n"
            f"📅 Date: {date}\n⏰ Time: {time}\n📌 Reason: {reason}\n\nThanks!\nWe will be waiting for you."
        )
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("aniqayan2@gmail.com", "ueik kfpw zwrb dhev")
            smtp.send_message(msg)
            st.success(f"📧 Email sent to {to_email}.")
    except Exception as e:
        st.error(f"❌ Email error: {e}")

# --- CREATE TABLE ON APP START ---
create_appointments_table()

# --- STREAMLIT UI ---
st.title("📅 Email Automation Tool For Appointment")
st.header("📝 Book Your Appointment — a confirmation email will be sent to your Gmail")

menu = st.sidebar.radio("Select Option", ["📤 Book Appointment", "📋 View All Bookings"])

if menu == "📤 Book Appointment":
    name = st.text_input("Enter your Name:")
    email = st.text_input("Enter your Email:")
    number = st.number_input("Enter your Phone Number", step=1, format="%d")
    reason = st.text_area("Enter Appointment Reason:")
    date = st.date_input("Choose Appointment Date")
    time = st.time_input("Choose Appointment Time")

    if st.button("✅ Book Appointment"):
        if save_appointment(name, email, number, reason, date, time):
            send_email(email, name, str(date), str(time), reason)
            st.success("🎉 Appointment has been scheduled successfully.")
        else:
            st.error("⛔ This slot is already booked. Please choose another one.")

elif menu == "📋 View All Bookings":
    st.subheader("📃 All Scheduled Appointments")
    appointments = get_all_appointments()
    if appointments:
        st.table(
            [{"Name": a[0], "Email": a[1], "Phone": a[2], "Reason": a[3], "Date": a[4], "Time": a[5]} for a in appointments]
        )
    else:
        st.info("📭 No appointments found.")

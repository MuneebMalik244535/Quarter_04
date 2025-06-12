import smtplib
from email.message import EmailMessage
import streamlit as st
import os
def send_email(to_email: str, name: str, date: str, time: str , reason : str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Appointment Confirmation"
        msg["From"] = "aniqayan2@gmail.com"
        msg["To"] = to_email
        msg.set_content(f"Hello {name},\n I am Hafiz Muneeb Assistant Your appointment has been Schedule for {reason} on {date} at {time}.\n\nThanks. \n We will be waiting for you \n")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("aniqayan2@gmail.com", "ueik kfpw zwrb dhev")
            smtp.send_message(msg)
            st.success(f"📧 Email sent to {to_email}.")
    except Exception as e:
        st.error(f"❌ Email error: {e}")

st.title("Email Automation Tool For Appoinment")
st.header("Book Your Appoinment so that The Verify Message will be sent to you gmail Account")
name = st.text_input("Enter your Name Here :  ")
email = st.text_input("Enter Your Email Here : ")
number = st.number_input("Enter Your Phone Number")
reason = st.text_area("Enter Appoinment Reason : ")
date = st.date_input("Choose appointment date")
time = st.time_input("Choose appointment time")
try : 
    if st.button("Book Appoinment"):
        slot = f"{date} {time}"
        if not os.path.exists("Booking_data.txt") or slot not in open("Booking_data.txt" , "r" , encoding="utf-8").read():
            with open("Booking_data.txt" , "a" , encoding = "utf-8" ) as file : 
                file.write(f"User name : {name} \n Email : {email} \n Slots : {slot} \n Reason of Appoinment : {reason} \n---\n")
            send_email(email , name , str(date) , str(time) , reason)
            st.success("Congratulations Appoinment Has Been Scheduled")    
except Exception as e : 
    st.error(f"Email Error {e}")           
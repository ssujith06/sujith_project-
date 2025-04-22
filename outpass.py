import streamlit as st
from datetime import datetime, date, time
import pandas as pd
import os
from textblob import TextBlob

def analyze_reason(reason):
    acceptable_reasons = ['shopping', 'barber', 'haircut', 'salon', 'eat', 'food',
                         'dinner', 'lunch', 'market', 'pharmacy', 'stationery']
    analysis = TextBlob(reason)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    is_acceptable = any(keyword in reason.lower() for keyword in acceptable_reasons)
    if is_acceptable:
        return "Auto-Approved", 1.0, 0.1
    return "Pending Review", polarity, subjectivity

def has_applied_today(reg_no):
    today = date.today().strftime("%Y-%m-%d")
    if os.path.exists("outpass_data.csv"):
        df = pd.read_csv("outpass_data.csv")
        filtered = df[(df['Register Number'] == reg_no) & (df['Date'] == today)]
        return not filtered.empty
    return False

def has_returned_today(reg_no):
    today = date.today().strftime("%Y-%m-%d")
    if os.path.exists("outpass_data.csv"):
        df = pd.read_csv("outpass_data.csv")
        filtered = df[(df['Register Number'] == reg_no) & (df['Date'] == today)]
        if not filtered.empty:
            latest = filtered.iloc[-1]
            if pd.notna(latest['Actual Return']) and latest['Actual Return'] != "Not Returned Yet":
                return latest['Actual Return']
    return None

def update_return_time(reg_no):
    today = date.today().strftime("%Y-%m-%d")
    if os.path.exists("outpass_data.csv"):
        df = pd.read_csv("outpass_data.csv")
        # Find all records for this reg_no today that haven't been returned
        idx = df[(df['Register Number'] == reg_no) & 
                (df['Date'] == today) & 
                ((df['Actual Return'].isna()) | 
                 (df['Actual Return'] == "Not Returned Yet"))].index
        
        if not idx.empty:
            return_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.at[idx[-1], 'Actual Return'] = return_time
            df.to_csv("outpass_data.csv", index=False)
            
            # Update session state
            st.session_state['has_returned'] = True
            return return_time
    return None

def outpass_page():
    st.markdown("## 🏃‍♂️ Outpass Request")

    # Check if user has already returned today
    if 'has_returned' in st.session_state and st.session_state.get('has_returned', False):
        st.warning("🚫 You've already used and returned from your outpass today.")
        if st.button("Back to Chatbot"):
            st.session_state['current_page'] = 'chat'
            st.rerun()
        return

    name = st.text_input("👤 Student Name", value=st.session_state.get("username", ""))
    reg_no = st.text_input("🆔 Register Number")

    if not name or not reg_no:
        return

    returned_time = has_returned_today(reg_no)
    if returned_time:
        st.session_state['has_returned'] = True  # Mark as returned
        st.success(f"🎉 You already returned to hostel at {returned_time}")
        if st.button("Back to Chatbot"):
            st.session_state['current_page'] = 'chat'
            st.rerun()
        return

    if has_applied_today(reg_no):
        st.warning("😅 Whoa there, Outpass Ninja! 🥷 You already used your one-shot today.")
        if st.button("Back to Chatbot"):
            st.session_state['current_page'] = 'chat'
            st.rerun()
        return

    st.info("🚀 You can apply for an outpass now!")

    reason = st.text_area("📜 Reason for Outpass", placeholder="Example: Going to the market 💼")
    departure_time = st.time_input("⏰ Departure Time", value=datetime.now().time())
    return_time = st.time_input("🕒 Expected Return Time (before 9PM)", value=time(19, 0))

    if return_time >= time(21, 0):
        st.error("⛔ Return time must be before 9:00 PM")
        return

    if st.button("📩 Submit Outpass Request"):
        if not all([name, reg_no, reason]):
            st.warning("❌ All fields are required!")
            return

        status, polarity, subjectivity = analyze_reason(reason)
        data = {
            "Name": name,
            "Register Number": reg_no,
            "Reason": reason,
            "Date": date.today().strftime("%Y-%m-%d"),
            "Departure Time": departure_time.strftime("%H:%M"),
            "Expected Return": return_time.strftime("%H:%M"),
            "Actual Return": "Not Returned Yet",
            "Status": "Auto-Approved" if status == "Auto-Approved" else "Pending",
            "Submitted At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "AI Analysis": status,
            "Sentiment Score": polarity,
            "Subjectivity Score": subjectivity
        }

        try:
            # Initialize CSV with headers if it doesn't exist
            if not os.path.exists("outpass_data.csv"):
                df = pd.DataFrame(columns=data.keys())
                df.to_csv("outpass_data.csv", index=False)
            
            df = pd.DataFrame([data])
            if os.path.exists("outpass_data.csv"):
                old = pd.read_csv("outpass_data.csv")
                df = pd.concat([old, df])
            df.to_csv("outpass_data.csv", index=False)
            
            st.session_state['show_receipt'] = True
            st.session_state['current_page'] = 'chat'
            st.session_state['last_outpass'] = data  # Store for receipt
            st.rerun()
        except Exception as e:
            st.error(f"🚨 Could not save: {str(e)}")

    # Only show return button if they have an active outpass
    if has_applied_today(reg_no) and not has_returned_today(reg_no):
        if st.button("🏠 I'm back to hostel!"):
            returned = update_return_time(reg_no)
            if returned:
                st.success(f"🎉 Return time updated to {returned}")
                st.session_state['has_returned'] = True
                st.rerun()
            else:
                st.error("😵 Couldn't update your return time. Did you apply for an outpass today?")
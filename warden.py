import streamlit as st
import pandas as pd
import os
from credentials import ADMIN_USERNAME, ADMIN_PASSWORD
from datetime import datetime, time

def warden_login():
    st.title("🧑‍🏫 Admin Login (Warden)")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["warden_logged_in"] = True
            st.success("✅ Logged in as Warden")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

def display_outpass_data():
    st.subheader("📋 Student Outpass Requests")

    try:
        if os.path.exists("outpass_data.csv"):
            df = pd.read_csv("outpass_data.csv")
            df = df[df['Name'].astype(str).str.lower() != 'name']

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"])
                today = pd.to_datetime(datetime.now().date())

                # Calculate daily request count for each student
                daily_counts = df[df["Date"] == today].groupby("Register Number")["Reason"].nunique().reset_index()
                daily_counts.columns = ["Register Number", "Outpasses Today"]

                st.subheader("📅 Today's Outpass Summary")
                st.dataframe(daily_counts)

                df = df.merge(daily_counts, on="Register Number", how="left")

                # Highlight approval time restriction
                now = datetime.now().time()
                if now >= time(18, 0):
                    st.warning("⚠️ Approvals after 6PM are not allowed.")

                editable_status = st.data_editor(
                    df,
                    column_config={
                        "Status": st.column_config.SelectboxColumn(
                            "Status",
                            help="Change approval status",
                            width="medium",
                            options=["Pending", "Approved", "Rejected", "Needs More Info"],
                            required=True,
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    num_rows="dynamic"
                )

                if st.button("Save Changes"):
                    if now >= time(18, 0):
                        st.error("🚫 Cannot approve outpasses after 6PM.")
                        return
                    editable_status.to_csv("outpass_data.csv", index=False)
                    st.success("Status updates saved!")

                csv = editable_status.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name='outpass_data.csv',
                    mime='text/csv',
                )

                st.subheader("📊 Approval Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pending", len(editable_status[editable_status['Status'] == "Pending"]))
                with col2:
                    st.metric("Approved", len(editable_status[editable_status['Status'] == "Approved"]))
                with col3:
                    st.metric("Rejected", len(editable_status[editable_status['Status'] == "Rejected"]))

                st.subheader("🤖 AI Insights")
                if "AI Analysis" in editable_status.columns:
                    st.bar_chart(editable_status["AI Analysis"].value_counts())
            else:
                st.info("No outpass submissions found.")
        else:
            st.info("No outpass submissions found.")
    except Exception as e:
        st.error(f"Error loading outpass data: {str(e)}")
        st.info("Please try again or check the data file.")

def warden_page():
    if "warden_logged_in" not in st.session_state or not st.session_state["warden_logged_in"]:
        warden_login()
    else:
        if st.button("Logout"):
            st.session_state["warden_logged_in"] = False
            st.rerun()
        display_outpass_data()
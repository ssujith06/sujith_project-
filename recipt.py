import streamlit as st
import pandas as pd
import os
from outpass import update_return_time

def show_receipt():
    st.title("📄 Outpass Receipt")

    try:
        if os.path.exists("outpass_data.csv"):
            df = pd.read_csv("outpass_data.csv")
            if df.empty:
                st.warning("No outpass data found.")
                return

            # Get the last outpass for the current user
            if 'username' in st.session_state:
                last = df[df['Name'] == st.session_state['username']].iloc[-1]
            else:
                last = df.iloc[-1]

            # Store in session state for easy access
            st.session_state['last_outpass'] = last.to_dict()

            # Display all fields properly formatted
            st.markdown(f"**Name:** {last['Name']}")
            st.markdown(f"**Register Number:** {last['Register Number']}")
            st.markdown(f"**Reason:** {last['Reason']}")
            st.markdown(f"**Date:** {last['Date']}")
            st.markdown(f"**Departure Time:** {last['Departure Time']}")
            st.markdown(f"**Expected Return Time:** {last['Expected Return']}")
            
            # Handle return time properly
            actual_return = last['Actual Return']
            if pd.isna(actual_return) or str(actual_return) == "Not Returned Yet":
                st.markdown("**Actual Return Time:** Not returned yet")
                
                # Add "Back to Hostel" button only if not returned yet
                if st.button("🏠 I'm back to hostel!", key="return_to_hostel"):
                    returned = update_return_time(last['Register Number'])
                    if returned:
                        st.success(f"🎉 Return time updated to {returned}")
                        st.session_state['has_returned'] = True  # Mark as returned
                        st.rerun()
                    else:
                        st.error("😵 Couldn't update your return time. Please try again!")
            else:
                st.markdown(f"**Actual Return Time:** {actual_return}")
                st.session_state['has_returned'] = True  # Mark as returned
            
            st.markdown(f"**Status:** {last['Status']}")
            
            # Only show these if they exist in the data
            if 'AI Analysis' in last:
                st.markdown(f"**AI Analysis:** {last['AI Analysis']}")
            if 'Sentiment Score' in last:
                st.markdown(f"**Sentiment Score:** {last['Sentiment Score']:.2f}")
            if 'Subjectivity Score' in last:
                st.markdown(f"**Subjectivity Score:** {last['Subjectivity Score']:.2f}")

    except Exception as e:
        st.error(f"Error reading outpass data: {e}")
        st.info("Please contact support if this persists.")
        return

    st.success("Your outpass has been submitted successfully!")
    st.info("You'll be notified when the warden reviews your application.")

    if st.button("Back to Menu", key="receipt_back"):
        st.session_state['show_receipt'] = False
        st.session_state['current_page'] = "chat"
        st.rerun()
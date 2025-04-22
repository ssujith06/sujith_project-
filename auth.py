import streamlit as st

# Sample login credentials
sample_users = {
    "sujith": "pass123",
    "arulsakthi": "arul123",
    "ashwinkumar": "ashwin123"
}

def login():
    # Fun animated header
    st.markdown("""
        <div style='text-align:center; margin-top: -20px;'>
            <h1 style='color:#58a6ff; animation: floatText 4s ease-in-out infinite;'>🔐 Welcome, Hero of the Hostel! 🏡</h1>
            <p style='font-size:18px; color:#ffa657; animation: swing 2s infinite ease-in-out;'>Please enter your secret credentials... 🕵️‍♂️</p>
        </div>
        <style>
            @keyframes floatText {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-5px); }
                100% { transform: translateY(0px); }
            }

            @keyframes swing {
                0% { transform: rotate(0deg); }
                50% { transform: rotate(3deg); }
                100% { transform: rotate(-3deg); }
            }

            .hanging-thought {
                font-size: 14px;
                color: #c9d1d9;
                text-align: center;
                margin-top: 10px;
                padding: 5px 10px;
                background: #21262d;
                display: inline-block;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                animation: floatText 6s ease-in-out infinite;
            }
        </style>
    """, unsafe_allow_html=True)

    # Funny thought bubbles
    st.markdown("<div class='hanging-thought'>💡 Pro Tip: Passwords are like underwear. Keep them secret. 🩲</div>", unsafe_allow_html=True)
    st.markdown("<div class='hanging-thought'>🚪 Outpass = Freedom + Approval!</div>", unsafe_allow_html=True)

    # Input fields
    st.write("##")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    # Login button
    if st.button("🚀 Let Me In!"):
        if username in sample_users and sample_users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"🎉 Welcome back, `{username}`! Your escape is being processed... 🏃‍♂️")
            st.rerun()
        else:
            st.error("😵 Wrong credentials! Are you an imposter? Try again... 🕵️‍♀️")

def main():
    login()

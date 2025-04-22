# app.py
import streamlit as st
from outpass import outpass_page
from warden import warden_page
from chatbot import chatbot
from recipt import show_receipt
from auth import login

def main():
    # Sidebar title
    st.sidebar.title("Navigation")

    # Inject dark-theme friendly CSS
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                font-family: 'Segoe UI', sans-serif;
                background-color: #0d1117;
                color: #c9d1d9;
            }

            .css-18e3th9 {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            h1, h2, h3, .stText, .stRadio label, .stSelectbox label {
                color: #f0f6fc !important;
            }

            .stRadio > div {
                background-color: #161b22;
                padding: 1rem;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                color: #c9d1d9;
            }

            .stButton>button {
                background: linear-gradient(to right, #00c6ff, #0072ff);
                color: white;
                padding: 0.7em 1.5em;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.3s ease;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }

            .stButton>button:hover {
                background: linear-gradient(to right, #0072ff, #00c6ff);
                transform: translateY(-1px) scale(1.03);
            }

            .stTextInput > div > input,
            .stSelectbox > div,
            .stTextArea > div > textarea,
            .stNumberInput > div,
            .stDateInput > div {
                background-color: #21262d;
                color: #f0f6fc;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 10px;
            }

            .stSidebar {
                background: #161b22;
            }

            .stSidebar .css-1d391kg {
                color: white;
            }

            .stSelectbox label, .stTextInput label, .stTextArea label {
                color: #f0f6fc;
            }

            /* Center alignment for role selection */
            .stRadio, .stButton {
                display: flex;
                justify-content: center;
            }

            .css-1d391kg {
                color: #f0f6fc;
            }
            
            .funny-quote {
                background: #161b22;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #00c6ff;
                font-style: italic;
            }
        </style>
    """, unsafe_allow_html=True)

    # Session state init
    if 'show_receipt' not in st.session_state:
        st.session_state['show_receipt'] = False

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'user_type' not in st.session_state:
        st.session_state['user_type'] = None

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'home'

    if 'has_returned' not in st.session_state:
        st.session_state['has_returned'] = False

    # Role selection screen
    if st.session_state['user_type'] is None:
        st.markdown("<h1 style='text-align: center;'>🎓 <span style='color:#00c6ff'>AI Outpass System</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px; color: gray;'>Smart campus access management solution</p>", unsafe_allow_html=True)
        st.write("##")
        st.markdown("<h3 style='text-align: center;'>Select Your Role</h3>", unsafe_allow_html=True)
        choice = st.radio("", ["Student", "Warden"], horizontal=False)
        if st.button("Continue", key="role_continue"):
            st.session_state['user_type'] = choice
            st.rerun()
        return

    # Chat redirection from receipt
    if st.session_state['current_page'] == 'chat':
        chatbot()
        return

    # Student flow
    if st.session_state['user_type'] == "Student":
        if not st.session_state['logged_in']:
            login()
        else:
            if st.session_state['show_receipt']:
                show_receipt()
            else:
                st.markdown("<h2 style='text-align: center;'>Welcome back, " + st.session_state.get('username', 'Student') + "! 👋</h2>", unsafe_allow_html=True)
                
                # Funny quotes
                quotes = [
                    "Remember: An outpass a day keeps the warden away! 😜",
                    "Pro tip: Running late? Just say you were debugging life! 🐛",
                    "Hostel rule #1: What happens in the mess, stays in the mess! 🍛",
                    "Your attendance may be low, but your spirits are high! 🚀",
                    "They say college is the best time of your life... who's 'they'? 🤔"
                ]
                
                st.markdown(f"""
                    <div class="funny-quote">
                        {random.choice(quotes)}
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("##")
                st.markdown("<h3 style='text-align: center;'>What would you like to do?</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚀 Apply for Outpass", use_container_width=True):
                        st.session_state['current_page'] = 'outpass'
                        st.rerun()
                with col2:
                    if st.button("🤖 Chat with BuddyBot", use_container_width=True):
                        st.session_state['current_page'] = 'chat'
                        st.rerun()
                
                if st.session_state.get('current_page') == 'outpass':
                    outpass_page()

    # Warden flow
    elif st.session_state['user_type'] == "Warden":
        warden_page()

if __name__ == "__main__":
    import random
    main()
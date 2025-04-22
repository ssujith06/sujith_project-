# chatbot_bert.py
import streamlit as st
import random
from collections import defaultdict
from transformers import pipeline

# Load BERT emotion classifier
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

# BERT-emotion-based response dictionary
responses = {
    "sadness": [
        "I'm really sorry you're feeling down. Want to talk about it? 🫂",
        "You're not alone — I’m here for you. 💙",
        "Tough days don’t last. You’ve got this! 💪"
    ],
    "joy": [
        "Yay! Your joy just made my day 😄",
        "Keep smiling, it suits you! ✨",
        "Let’s celebrate! 🎉"
    ],
    "anger": [
        "Take a deep breath... you deserve peace. 🧘‍♀️",
        "Anger is valid — let’s channel it into strength 💥",
        "Want to vent? I’m all ears."
    ],
    "fear": [
        "It's okay to be scared sometimes. I’m with you 🤝",
        "Breathe in... Breathe out... You are safe. 🌬️",
        "You’re stronger than your fears."
    ],
    "love": [
        "Sending all the love right back to you 💌",
        "You’ve got a heart of gold 💛",
        "Keep spreading love — the world needs it 💖"
    ],
    "surprise": [
        "Whoa! That’s unexpected! 😲",
        "Wow! Tell me more! 🤩",
        "Surprises can be fun, right?"
    ],
    "default": [
        "Hmm, I didn’t get that fully — but I’m still here to listen!",
        "Tell me more about how you're feeling. 💭"
    ]
}

# Get emotion label using BERT
def detect_emotion_bert(message):
    try:
        prediction = emotion_classifier(message)
        label = prediction[0]['label'].lower()
        return label if label in responses else "default"
    except Exception:
        return "default"

# Streamlit chatbot app
def chatbot():
    st.title("🧠 BuddyBot: Emotion-Aware AI (Powered by BERT 🤖)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "used_responses" not in st.session_state:
        st.session_state.used_responses = defaultdict(list)

    if "available_responses" not in st.session_state:
        st.session_state.available_responses = {
            intent: random.sample(responses[intent], len(responses[intent]))
            for intent in responses
        }

    for msg in st.session_state.chat_history:
        sender = "👤 You" if msg["role"] == "user" else "🤖 BuddyBot"
        st.markdown(f"**{sender}:** {msg['content']}")

    user_input = st.text_input("How are you feeling?", key="chat_input")

    if st.button("Send", key="send_button") and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        intent = detect_emotion_bert(user_input)

        available = st.session_state.available_responses[intent]
        used = st.session_state.used_responses[intent]

        if len(used) >= len(available):
            st.session_state.available_responses[intent] = random.sample(responses[intent], len(responses[intent]))
            st.session_state.used_responses[intent] = []
            available = st.session_state.available_responses[intent]
            used = st.session_state.used_responses[intent]

        for response in available:
            if response not in used:
                selected = response
                used.append(response)
                break

        st.session_state.chat_history.append({"role": "bot", "content": selected})
        st.rerun()

    if st.button("Back to Receipt", key="chat_back_to_receipt"):
        st.session_state['current_page'] = 'receipt'
        st.session_state['show_receipt'] = True
        st.rerun()

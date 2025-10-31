import streamlit as st
import google.generativeai as genai
from datetime import datetime

# -------------------- CONFIGURATION --------------------
genai.configure(api_key="AIzaSyCYxIylA_VW4NHYQTb4uuZ-6963QPP78Fw")  # replace with your actual Gemini API key
model = genai.GenerativeModel("models/gemini-2.5-flash")

st.set_page_config(
    page_title="Aanya’s Cyberbot",
    page_icon="🤖",
    layout="centered",
)

# -------------------- INITIAL SETUP --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# -------------------- SIDEBAR --------------------
st.sidebar.title("💬 Chat History")
if st.session_state.chat_history:
    for i, chat in enumerate(st.session_state.chat_history):
        if st.sidebar.button(f"Chat {i+1} - {chat['timestamp']}"):
            st.session_state.current_chat = chat["messages"]
else:
    st.sidebar.write("No previous chats yet.")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.chat_history = []
    st.session_state.feedback = {}
    st.rerun()

# -------------------- MAIN CHAT UI --------------------
st.title("🤖 InfoGenius - Your favourite CyberBot")

user_input = st.chat_input("Type your message here...")

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []


for msg in st.session_state.current_chat:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            if msg.get("id") in st.session_state.feedback:
                feedback = st.session_state.feedback[msg["id"]]
                st.write(f"✅ Feedback recorded: {feedback}")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍", key=f"up_{msg['id']}"):
                        st.session_state.feedback[msg["id"]] = "positive"
                        st.success("Thanks for your feedback! 👍")
                        st.rerun()
                with col2:
                    if st.button("👎", key=f"down_{msg['id']}"):
                        st.session_state.feedback[msg["id"]] = "negative"
                        st.warning("Feedback recorded 👎")
                        st.rerun()

# -------------------- RESPONSE HANDLING --------------------
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.current_chat.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()
            except Exception as e:
                bot_reply = f"⚠️ Error generating response: {e}"

        st.markdown(bot_reply)
        msg_id = str(datetime.now().timestamp())
        st.session_state.current_chat.append({"role": "assistant", "content": bot_reply, "id": msg_id})

    # Save chat snapshot
    if len(st.session_state.current_chat) > 1:
        if not st.session_state.chat_history or st.session_state.current_chat not in [
            c["messages"] for c in st.session_state.chat_history
        ]:
            st.session_state.chat_history.append({
                "timestamp": datetime.now().strftime("%H:%M"),
                "messages": st.session_state.current_chat.copy()
            })

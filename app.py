import streamlit as st
import feedparser

from ai_engine import ai_process
from voice import listen, speak, stop_speaking
import musicLibrary

st.set_page_config(page_title="MAYA – AI Voice Assistant", layout="centered")

st.title("🎙️ MAYA – AI Voice Assistant")
st.write("Click the button and talk to Maya")

STOP_WORDS = [
    "stop speaking",
    "stop",
    "shut up",
    "be quiet",
    "silence",
    "enough"
]

if "chat" not in st.session_state:
    st.session_state.chat = []

if "open_url" not in st.session_state:
    st.session_state.open_url = None

for sender, message in st.session_state.chat:
    if sender == "You":
        st.markdown(f"**👤 You:** {message}")
    else:
        st.markdown(f"**🤖 Maya:** {message}")


if st.session_state.open_url:
    st.markdown("### 🔗 Action")
    st.link_button("👉 Open link", st.session_state.open_url)

    st.session_state.open_url = None

if st.button("🎤 Talk to Maya"):
    try:
        with st.spinner("🎧 Listening..."):
            user_command = listen()

        if not user_command:
            st.warning("I didn't catch that. Please try again.")
            st.stop()

        user_lower = user_command.lower()

        if any(word in user_lower for word in STOP_WORDS):
            stop_speaking()
            reply = "Okay, I'll stop."
            st.session_state.chat.append(("Maya", reply))
            st.stop()

        st.session_state.chat.append(("You", user_command))

    except:
        st.error("Couldn't understand. Please try again.")
        st.stop()

if st.session_state.chat:
    last_sender, last_msg = st.session_state.chat[-1]

    if last_sender == "You":
        user_lower = last_msg.lower()

        with st.spinner("🤖 Maya is thinking..."):

            if any(word in user_lower for word in STOP_WORDS):
                stop_speaking()
                reply = "Okay, I'll stop."

            elif "open google" in user_lower:
                reply = "Opening Google"
                st.session_state.open_url = "https://google.com"

            elif "open youtube" in user_lower:
                reply = "Opening YouTube"
                st.session_state.open_url = "https://youtube.com"

            elif user_lower.startswith("play"):
                song = user_lower.replace("play", "").strip().lower()
                link = musicLibrary.music.get(song)

                if link:
                    reply = f"Playing {song}"
                    st.session_state.open_url = link
                else:
                    reply = "Sorry, I couldn't find that song."

            elif "news" in user_lower:
                feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
                if feed.entries:
                    top_headlines = feed.entries[:5]
                    reply = "Here are the top news headlines:\n"
                    for i, entry in enumerate(top_headlines, start=1):
                        reply += f"{i}. {entry.title}\n"
                else:
                    reply = "Sorry, I couldn't fetch the news right now."

            else:
                reply = ai_process(last_msg)

            st.session_state.chat.append(("Maya", reply))

        if reply and not any(word in user_lower for word in STOP_WORDS):
            with st.spinner("🔊 Maya is speaking..."):
                speak(reply)

        st.rerun()
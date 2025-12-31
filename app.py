import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# --- CONFIG ---
st.set_page_config(page_title="AI Voyager Pro", page_icon="🌎", layout="wide")

# API Keys (Hackathon keys - Ensure these are active)
genai.configure(api_key="AIzaSyBUDl5O85bqjHEIGMwdFxQwoglC50FTdTg")
ELEVEN_API_KEY = "sk_f54676b97602a893d08e4cb6e36ecdc13d21f8ef8a12606c"
client = ElevenLabs(api_key=ELEVEN_API_KEY)

# --- UI DESIGN (VIDEO BG & GLASSMORPHISM) ---
st.markdown("""
    <style>
    #bgVideo {
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        object-fit: cover;
        filter: brightness(0.45);
    }
    .main-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(18px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 45px;
        margin: 4% auto;
        max-width: 800px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    h1, h3, p, label { color: white !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white !important; border: none; padding: 12px 30px;
        border-radius: 50px; font-weight: bold; font-size: 20px;
        width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    </style>
    <video autoplay muted loop playsinline id="bgVideo">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-beautiful-landscape-of-mountains-and-a-river-during-sunset-3127-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

# --- APP UI ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.title("🌎 AI Global Voyager")
st.markdown("#### *Your Personal AI Guide in Your Own Language*")

user_input = st.text_input("📍 Destination:", placeholder="Enter a city or place...")
lang_choice = st.radio("Language:", ("Hindi", "English"), horizontal=True)

if st.button("Unveil the Journey ✨"):
    if user_input:
        with st.spinner("AI is traveling for you..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Give 4 captivating sentences about {user_input} in {lang_choice}. Focus on history and famous food."
                response = model.generate_content(prompt)
                details = response.text
                
                st.markdown("---")
                st.info(details)
                
                audio = client.text_to_speech.convert(
                    text=details, voice_id="21m00Tcm4TlvDq8ikWAM",
                    model_id="eleven_multilingual_v2"
                )
                st.audio(b"".join(audio), format="audio/mp3", autoplay=True)
                st.balloons()
            except:
                st.error("API Limit reached. Please try again in a moment.")
    else:
        st.warning("Please enter a destination!")

st.markdown('</div>', unsafe_allow_html=True)

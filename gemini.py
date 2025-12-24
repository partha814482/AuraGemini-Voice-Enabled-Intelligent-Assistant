import streamlit as st
import google.genai as genai
import base64
import pyttsx3
import threading

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Gemini RAG App",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# BACKGROUND IMAGE
# -------------------------------
def set_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Glass effect for inputs */
        .stTextInput, .stTextArea, .stButton button {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🔴 YOUR IMAGE PATH
set_background(
    r"C:\Users\HP\OneDrive\Documents\data science\Promt Engennering\02 prompet.jpg"
)

# -------------------------------
# TEXT TO SPEECH (AI ASSISTANT)
# -------------------------------
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)   # speed
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    threading.Thread(target=speak_text, args=(text,), daemon=True).start()

# -------------------------------
# APP UI
# -------------------------------
st.title("🤖 Prompt Engineering using Gemini")
st.caption("Ask a question and the AI assistant will answer and read it aloud")

api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # Dummy retriever (can replace with FAISS later)
    def retriever_info(query):
        return (
            "India has a mixed economy where the service sector contributes "
            "more than half of GDP, followed by industry and agriculture."
        )

    def rag_query(query):
        context = retriever_info(query)

        prompt = f"""
User Question:
{query}

Retrieved Context:
{context}

Answer clearly and concisely.
"""

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
            config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )
        return response.text

    query = st.text_area("💬 Ask your question:", "Explain India's economy")

    if st.button("🔍 Generate Response"):
        if query.strip():
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = rag_query(query)

                    st.success("✅ Response Generated")
                    st.markdown(f"### 🧠 Answer:\n{answer}")

                    # 🔊 AI Assistant speaks the answer
                    speak_async(answer)

                    st.info("🔊 AI Assistant is reading the answer aloud")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a question.")

else:
    st.info("Please enter your Gemini API key to start.")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini + AI Voice | Author: Parthasarathi Behera")

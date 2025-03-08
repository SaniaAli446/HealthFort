import streamlit as st
import google.generativeai as genai
import base64

# Configure API Key
GENAI_API_KEY = "AIzaSyDGfK8y5mdOoYRJ1Ncm3lSfbKHmYBQ0Ro4"
genai.configure(api_key=GENAI_API_KEY)

# Set page title and layout
st.set_page_config(page_title="Mental Health Support", layout="wide")

# Load Background Image
def get_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image = "background.png"  
bin_str = get_base64(background_image)

st.markdown(f"""
    <style>
        body {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp {{
            background-color: transparent;
        }}
        .navbar {{
            display: flex;
            justify-content: center;
            padding: 15px;
            background-color: #1a1a2e;
        }}
        .navbar button {{
            padding: 14px 20px;
            text-decoration: none;
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
            margin: 0 15px;
            background: none;
            border: none;
            cursor: pointer;
        }}
        .navbar button:hover {{
            background-color: #16213e;
            border-radius: 5px;
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Navigation Bar
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.page = "Home"
with col2:
    if st.button("Chatbot"):
        st.session_state.page = "Chatbot"
with col3:
    if st.button("Upload Reports"):
        st.session_state.page = "Upload Reports"

# Home Page
if st.session_state.page == "Home":
    st.title("Welcome to the Mental Health Support Platform")
    st.write("""
    This platform is designed to provide mental health support through AI-powered conversations
    and secure report uploads. Our chatbot offers empathetic responses and well-being tasks 
    to help you feel better. Stay positive and take care of your mental health!
    """)

# Chatbot Page
elif st.session_state.page == "Chatbot":
    st.title("Mental Health Chatbot")

    # Initialize conversation history
    st.session_state.setdefault('conversation_history', [])

    def generate_response(user_input):
        st.session_state['conversation_history'].append({"role": "user", "content": user_input})
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        prompt = f"""
        User's concern: {user_input}
        
        1. Respond with a helpful and empathetic reply.
        2. Suggest a well-being task the user can do immediately.
        
        Format:
        **AI Response:** <your response>
        **Well-being Task:** <your suggested task>
        """
        response = model.generate_content(prompt)
        ai_response = response.text if response else "I'm here to support you. Take a deep breath."
        st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
        return ai_response

    # Display past conversations
    for msg in st.session_state['conversation_history']:
        role = "You" if msg['role'] == "user" else "AI"
        st.markdown(f"**{role}:** {msg['content']}")

    # User input
    user_message = st.text_input("How can I help you today?")
    if user_message:
        with st.spinner("Thinking..."):
            ai_response = generate_response(user_message)
            st.markdown(ai_response)

    # Buttons for additional features
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Give me a positive Affirmation"):
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content("Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed.")
            affirmation = response.text if response else "Stay strong and positive!"
            st.markdown(f"**Affirmation:** {affirmation}")

    with col2:
        if st.button("Give me a guided meditation"):
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content("Provide a 5-minute guided meditation script to help someone relax and reduce stress.")
            meditation_guide = response.text if response else "Take a deep breath, relax, and focus on your breathing."
            st.markdown(f"**Guided Meditation:** {meditation_guide}")

# Report Upload Page
elif st.session_state.page == "Upload Reports":
    st.title("Upload Medical Reports")
    st.write("This feature is still under development. Stay tuned for updates!")
    st.file_uploader("Upload your report (Coming Soon)", type=["pdf", "jpg", "png", "txt"])

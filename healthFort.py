import streamlit as st
import google.generativeai as genai
import base64

# Set page title
st.set_page_config(page_title="Mental Health Chatbot")

# Configure API Key
GENAI_API_KEY = "AIzaSyDGfK8y5mdOoYRJ1Ncm3lSfbKHmYBQ0Ro4"
genai.configure(api_key=GENAI_API_KEY)

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
    </style>
    """, unsafe_allow_html=True)

# Initialize conversation history
st.session_state.setdefault('conversation_history', [])

# Function to generate AI response + Task
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    
    # AI prompt to generate a response AND a well-being task
    prompt = f"""
    User's concern: {user_input}

    1. First, respond with a helpful and empathetic reply based on the user's concern.
    2. Then, suggest a **small well-being task** that the user can do to improve their mood or mental health.
    3. The task should be practical, simple, and something the user can do immediately.

    Format your response as:
    **AI Response:** <your response>
    **Well-being Task:** <your suggested task>
    """

    response = model.generate_content(prompt)
    
    if response:
        ai_response = response.text
    else:
        ai_response = "**AI Response:** Sorry, I couldn't generate a response.\n**Well-being Task:** Try taking a deep breath and relaxing."

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    
    return ai_response

# Function to generate a positive affirmation
def generate_affirmation():
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = model.generate_content(prompt)
    return response.text if response else "Stay strong and positive!"

# Function to generate a guided meditation script
def generate_meditation_guide():
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = model.generate_content(prompt)
    return response.text if response else "Take a deep breath, relax, and focus on your breathing."

# Streamlit UI
st.title("Mental Health Support Agent")

# Display past conversation history
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
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")

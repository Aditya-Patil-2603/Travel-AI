import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv


# Load API key from .env
load_dotenv()


# Configure the page
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide"
)


# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")


# Check API key
if not api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()


# Groq client
client = Groq(
    api_key=api_key
)


# Title and description
st.title("✈️ AI Travel Assistant")

st.caption(
    "Your AI-powered travel companion for destinations, "
    "attractions, food, hotels, and travel tips."
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
st.sidebar.title("🌍 Travel Settings")


# Destination input
destination = st.sidebar.text_input(
    "Enter your destination",
    placeholder="e.g. Goa, Paris, Dubai"
)


# Message count
st.sidebar.metric(
    "Conversation Messages",
    len(st.session_state.messages)
)


# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Chat input
user_input = st.chat_input(
    "Ask me anything about your trip..."
)


# Process user input
if user_input:

    # Check destination
    if not destination.strip():

        st.warning(
            "Please enter a travel destination in the sidebar first."
        )

        st.stop()


    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)


    # System prompt
    system_prompt = f"""
You are an intelligent AI Travel Assistant.

The user's selected destination is: {destination}

Help the user with:

- Tourist attractions
- Places to visit
- Hotels and accommodation
- Local food
- Restaurants
- Travel tips
- Transportation
- Suggested itineraries
- Things to do
- Budget-friendly recommendations
- Safety and general travel advice

Give useful, clear, and personalized answers.

Always consider the selected destination when answering.
"""


    # Prepare conversation
    conversation = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # Add previous conversation
    conversation.extend(
        st.session_state.messages
    )


    # Get AI response
    try:

        with st.chat_message("assistant"):

            with st.spinner("Planning your trip..."):

                response = client.chat.completions.create(

                    model="llama-3.3-70b-versatile",

                    messages=conversation,

                    temperature=0.7,

                    max_tokens=1024
                )


                assistant_response = (
                    response.choices[0]
                    .message.content
                )


                st.markdown(
                    assistant_response
                )


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# Download conversation
if st.session_state.messages:

    conversation_text = (
        "AI Travel Assistant\n"
    )

    conversation_text += (
        f"Destination: {destination}\n"
    )

    conversation_text += (
        "=" * 50 + "\n\n"
    )


    # Add messages to download file
    for message in st.session_state.messages:

        role = message["role"].capitalize()

        conversation_text += (
            f"{role}:\n"
        )

        conversation_text += (
            message["content"]
        )

        conversation_text += "\n\n"


    # Download button
    st.sidebar.download_button(

        label="📥 Download Conversation",

        data=conversation_text,

        file_name="travel_conversation.txt",

        mime="text/plain"
    )
import streamlit as st
import requests
import uuid

# Streamlit app title
st.title("Document Q&A System")

# Check if session_id exists in session state, otherwise create one
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Use the session_id from session state
session_id = st.session_state.session_id

# Display the session ID for debugging
st.write(f"Session ID: {session_id}")

# Get OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Handle file upload
if uploaded_file and api_key:
    st.success("File uploaded successfully!")
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Upload to Backend"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"openai_key": api_key, "session_id": session_id}
        response = requests.post("http://backend:8000/upload", files=files, data=data)
        if response.status_code == 200:
            st.success("File successfully uploaded to backend!")
        else:
            st.error(f"Failed to upload file: {response.text}")

# Ask questions
question = st.text_input("Ask a question about the document:")
if question:
    if st.button("Get Answer"):
        response = requests.post("http://backend:8000/ask", json={"session_id": session_id, "question": question})
        if response.status_code == 200:
            st.write("**Answer:**", response.json().get("answer"))
        else:
            st.error(f"Failed to get an answer: {response.text}")

# Cleanup session
if st.button("End Session"):
    response = requests.post("http://backend:8000/cleanup", data={"session_id": session_id})
    if response.status_code == 200:
        st.success("Session cleaned up successfully!")
    else:
        st.error(f"Failed to clean up session: {response.text}")

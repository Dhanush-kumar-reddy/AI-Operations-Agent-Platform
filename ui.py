import streamlit as st
import requests

st.title("AI Operations Agent")

user_input = st.text_input("Enter your request")

if st.button("Run Agent"):
    if user_input:
        response = requests.post(
            "http://127.0.0.1:8000/run",
            params={"input_text": user_input}
        )

        st.json(response.json())
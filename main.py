# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
from dotenv import load_dotenv
import requests
import streamlit as st
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "f814e7e4-5f66-41a5-9f94-ad0b6a5c24a4"
FLOW_ID = "7393c6ea-45f1-49e2-9a0b-584fec84cf91"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
        }

        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
        
        # Added timeout parameter (30 seconds)
        response = requests.post(api_url, json=payload, headers=headers, timeout=(60, 120))
        


        return response.json()


def main():
    st.title("Langflow Chatbot")
    
    user_input = st.text_area("Message:", placeholder="Enter your message here...")

    if st.button("Run Flow"):
        if not user_input.strip():
            st.error("Please enter a message.")
            return
        
        try:
            with st.spinner("Running flow..."):
                response = run_flow(user_input)

            response = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.markdown(response)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()  

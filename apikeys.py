import streamlit as st

def get_api_keys():
    """Retrieves API keys from Streamlit Secrets.

    Returns:
        tuple: A tuple containing the retrieved API keys.
    """

    # Configure API keys from Streamlit Secrets
    groq_key = st.secrets["GROQ_API_KEY"]
    deepgram_key = st.secrets["DEEPGRAM_API_KEY"]
    openai_key = st.secrets["OPENAI_API_KEY"]
    aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
    aws_region = "sa-east-1"  # Defina a região da AWS que você está usando (São Paulo)

    return groq_key, deepgram_key, openai_key, aws_access_key_id, aws_secret_access_key, aws_region

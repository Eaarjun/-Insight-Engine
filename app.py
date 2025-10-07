import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load the env variables
load_dotenv()
headers = {
    "Authorization": f"Bearer {os.environ['HF_API_KEY']}",
}
print("Loaded API key:", os.getenv("HF_API_KEY"))

# API Inference points
API_URL_SUMMARY = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
API_URL_NER = "https://router.huggingface.co/hf-inference/models/dslim/bert-base-NER"



def query_api(api_url, payload):

    response = requests.post(api_url, headers=headers, json= payload)
    
    response.raise_for_status()
    return response.json


# Streamlit Interface
st.set_page_config(layout="wide", page_title="Polaris MVP")


st.title("Polaris")
st.markdown("Paste a block of text below, and the AI will generate a concise summary and extract key entities like names, organizations, and locations.")


col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Text")
    # Input field
    input_text = st.text_area("Enter text here", height=300, label_visibility="hidden")

# Analyse Button
if st.button("Analyse Text", use_container_width= True):
    if not input_text:
        st.warning("Please paste some text to analyze")
    else:
        with col2:
            st.subheader("Analysis Results")
            with st.spinner("The AI is thinking..."):
                try:
                    summary_payload = {"inputs": input_text}
                    summary_result = query_api(API_URL_SUMMARY, summary_payload)

                    st.info("Summary")
                    st.write(summary_result[0]["summary_text"])

                    # all the named entity recognition API
                    ner_payload = {"inputs": input_text}
                    ner_result = query_api(API_URL_NER, ner_payload)

                    st.info("Extracted Entities")     

                    for entity in ner_result:
                        st.markdown(f"**{entity['entity_group']}**: {entity['word']}")
                        
                except requests.exceptions.HTTPError as err:
                    st.error(f"An API error occurred: {err}. This might be due to model loading times on Hugging Face. Please try again in a moment.")
                except:
                    st.error("Something went wrong, please try again")
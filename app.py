
from dotenv import load_dotenv
load_dotenv() #loads all environment variables
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#model instantiate
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
            
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    



st.set_page_config(page_title="Multilanguage invoice extractor")
st.header("Gemini invoice reader application")
input=st.text_input("input prompt:", key="input")
uploaded_file=st.file_uploader("Choose an image...:", type=['jpg','png','pdf','jpeg'])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit = st.button("Tell me about the asked prompt from the invoice")


input_prompt="""You are an expert in undertstanding invoices. We will upload 
an image as an invoice and you will have to answer the input
 questions based on the uploaded invoice image."""


if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is:")
    st.write(response)
    
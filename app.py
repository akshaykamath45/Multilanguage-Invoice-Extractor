from dotenv import load_dotenv

load_dotenv() # loading all the environment variables from .env file

import streamlit as st # for frontend
import os  
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini pro vision
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    # input : what I want the assistant to do
    # prompt : what is the message I want to send
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    # will take the uploaded file
    # convert that into bytes
    # will give all the image format in byte
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
        raise FileNotFoundError("No File Uploaded")
    
# initializing streamlit
st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Multilanguage Invoice Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice ...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)
    
    
submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices.We will upload a image as an invoice and you will have to answer any questions based on the uploaded invoice image 
"""

# if submit button is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    # displaying the response
    st.subheader("The Response is ")
    st.write(response)
    

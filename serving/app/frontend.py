import streamlit as st
from fastapi import FastAPI
import uvicorn
import whisper

def main():
    st.title("Model test")


    # model = whisper.load_model("base")

    # uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg","png"])

    # if uploaded_file:
    #     st.image(image, caption='Uploaded Image')
    #     st.write("Classifying...")

    #     st.write(f'label is ')
    files ='text'
    response = requests.post("http://localhost:9000/order", files=files)
    st.write(f'label is {response}')

main()
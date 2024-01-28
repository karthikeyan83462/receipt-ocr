import streamlit as st
import re
import os
import json
import cv2
import pandas as pd
import pytesseract
import numpy as np
from pytesseract import Output

# Import functions from utils.py
from utils import *

# Main function
def main():
    # Set up styles and colors
    st.markdown(
        """
        <style>
            /* Add some custom CSS for a more attractive appearance */
            .title {
                color: #ff6347; /* Red color for title */
                text-align: center; /* Center align the title */
                font-size: 36px; /* Larger font size for title */
                margin-bottom: 20px; /* Add some margin below the title */
            }
            .subtitle {
                color: #4682b4; /* Blue color for subtitles */
                font-size: 24px; /* Font size for subtitles */
                margin-top: 20px; /* Add some margin above the subtitle */
            }
            .image-container {
                text-align: center; /* Center align the image */
            }
            .item {
                color: #228b22; /* Green color for items */
            }
            .cost {
                color: #9932cc; /* Purple color for costs */
                font-weight: bold; /* Bold font for costs */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Define constants and parameters
    remove_list = {"vat", "etc"}
    keywords = {"vat", "VAT Exempt Sales", "qty", "order total", "offer", "online offer", "tips", "discount", "atm",
                "total", "promo", "vat", "change", "recyclable", "tax", "sub total", "gratuity", "cgst", "sgst",
                "subtotal", "cash", "change (cash)"}
    excluded_words = {"ph", "Phone No", "food"}

    # Streamlit app title
    st.markdown("<h1 class='title'>Receipt Analysis App</h1>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display file details
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.sidebar.write(file_details)

        # Read the uploaded image and extract text
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        extracted_text = pytesseract.image_to_string(image, config=r'--oem 3 --psm 6')

        # OCR extraction
        merchant_info = extract_merchant_info(extracted_text, excluded_words)
        merchant_info_filtered = {key: value for key, value in merchant_info.items() if value != "Null"}
        items, item_cost = extract_items_and_costs(extracted_text, keywords, remove_list)
        additional_val, val_cost = extract_values(extracted_text, keywords, remove_list)

        # Display chosen image
        st.subheader("Chosen Image:")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Display extracted information
        st.subheader("Merchant info:")
        for key, value in merchant_info_filtered.items():
            st.text(f"    {key}: {value}")

        # Display items and costs
        st.subheader("Items and Costs:")
        if len(items) == len(item_cost):
            for i in range(len(items)):
                st.markdown(f"<p class='item'>{items[i]}</p>: <span class='cost'>{item_cost[i]}</span>", unsafe_allow_html=True)
        else:
            st.error("Error: Lengths of items and costs lists do not match.")

        # Display additional values
        st.subheader("Additional Values:")
        for i in range(len(additional_val)):
            st.write(f"    {additional_val[i]}: {val_cost[i]}")

        # Display extracted text
        st.subheader("Extracted Text:")
        st.write(extracted_text)

if __name__ == "__main__":
    main()

import streamlit as st
import re
import os
import json
import cv2
import pytesseract
import numpy as np
from pytesseract import Output

# Import functions from utils.py
from utils import *

# Main function
def main():
    remove_list = {"vat", "etc"}
    keywords = {"vat", "VAT Exempt Sales", "qty", "order total", "offer", "online offer", "tips", "discount", "atm",
                "total", "promo", "vat", "change", "recyclable", "tax", "sub total", "gratuity", "cgst", "sgst",
                "subtotal", "cash", "change (cash)"}
    excluded_words = {"ph", "Phone No", "food"}

    st.title("Receipt Analysis App")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.sidebar.write(file_details)

        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        extracted_text = pytesseract.image_to_string(image, config=r'--oem 3 --psm 6')

        # OCR extraction
        merchant_info = extract_merchant_info(extracted_text, excluded_words)  # Pass extracted_text as an argument
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

        # Display extracted items and costs
        st.subheader("Items and Costs:")
        for i in range(len(items)):
            st.write(f"    {items[i]}: {item_cost[i]}")

        # Display additional values
        st.subheader("Additional Values:")
        for i in range(len(additional_val)):
            st.write(f"    {additional_val[i]}: {val_cost[i]}")

        st.subheader("Extracted Text:")
        st.write(extracted_text)

if __name__ == "__main__":
    main()

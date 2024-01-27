import streamlit as st
import re
import os
import json
import cv2
import pytesseract
import numpy as np
from pytesseract import Output

# Functions
def clean_special_characters(name, excluded_words=None):
    if excluded_words is None:
        excluded_words = set()
    return re.sub(r'[^a-zA-Z\s]', '', name).replace('\n', ' ').replace(''.join(excluded_words), '').strip()

def clean_n_s(name):
    name = name.replace("\n","")
    name = name.replace(" ","")
    return name

def extract_items_and_costs(text,keywords,remove_list):
    item_cost = []
    items = []
    for line in text.splitlines():
        if re.search(r"[0-9]*\.[0-9]|[0-9]*\,[0-9]", line):
            regex_line = line
            if not any(exclude in regex_line.lower() for exclude in keywords):
                new_item = regex_line
                for subToRemove in remove_list:
                    new_item = new_item.replace(subToRemove, "").replace(subToRemove.upper(), "")
                new_item_list = ' '.join(ele for ele in new_item.split() if len(ele) != 2)
                cleaned_item = clean_special_characters(new_item_list)
                items.append(cleaned_item)
                cost = re.findall('\d*\.?\d+|\d*\,?\d+|', line.replace(",", "."))
                item_cost.extend(possibleCost for possibleCost in cost if "." in possibleCost)
    return items, item_cost

def extract_values(text, keywords,remove_list):
    val_cost = []
    vals = []
    for line in text.splitlines():
        if re.search(r"[0-9]*\.[0-9]|[0-9]*\,[0-9]", line):
            regex_line = line
            if any(exclude in regex_line.lower() for exclude in keywords):
                new_val = regex_line
                for subToRemove in remove_list:
                    new_val = new_val.replace(subToRemove, "").replace(subToRemove.upper(), "")
                new_val_list = ' '.join(ele for ele in new_val.split() if len(ele) != 2)
                cleaned_val = clean_special_characters(new_val_list)
                vals.append(cleaned_val)
                cost = re.findall('\d*\.?\d+|\d*\,?\d+|', line.replace(",", "."))
                val_cost.extend(possibleCost for possibleCost in cost if "." in possibleCost)
    return vals, val_cost

def extract_merchant_info(text,excluded_words):
    merchant_name_match = re.search(r'^\s*(.+?)(?:\d|^\s*$)', text, re.MULTILINE | re.DOTALL)
    phone_number_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text, re.IGNORECASE)
    website_match = re.search(r'www\.(.*?)\.com', text)
    server_name_match = re.search(r'Server\s*:\s*(\w+ \w+)', text, re.IGNORECASE)
    cashier_name_match = re.search(r'Cashier\s*:\s*(\w+ \w+)', text, re.IGNORECASE)
    waiter_name_match = re.search(r'W\.No:\s*([a-zA-Z\s]+)', text, re.IGNORECASE)
    user_name_match = re.search(r'User\s*:\s*(\w+)', text)
    sales_rep_name_match = re.search(r'Sales\s+Rep\s+(\w+)', text)
    date_time_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APM]{2})?)|(\d{1,2}-[a-zA-Z]+-\d{4}\s+\d{1,2}:\d{2}:\d{2}[APM]{0,1})|(\d{1,2}/\d{1,2}/\d{2,4})', text)
    table_number_match = re.search(r'\b(?:Table|TABLE|Tbl|TBL)\s*[:#]?\s*([a-zA-Z0-9]+)', text, re.IGNORECASE)
    order_number_match = re.search(r'\b(?:Order|ORDER|ORCheck|CHECK|Chk|CHK)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)', text, re.IGNORECASE)
    ticket_number_match = re.search(r'\b(?:Ticket|TICKET|Ticket #)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)', text, re.IGNORECASE)
    ref_number_match = re.search(r'\b(?:REF|ref)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)', text, re.IGNORECASE)
    station_number_match = re.search(r'\b(?:Station|STATION)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)', text, re.IGNORECASE)

    #order_number_match = re.search(r'\b(?:Order|ORDER|Check|CHECK|Chk|CHK|Order #)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)\s', text, re.IGNORECASE)
    guest_match = re.search(r'\b(?:Guests|GUESTS|Persons|PERSONS|Guest|GUEST)\s*[:#]?\s*([a-zA-Z0-9]+\s*[a-zA-Z0-9]*)\s', text, re.IGNORECASE)
    dine_in_match = re.search(r'\bDine In\b', text, re.IGNORECASE)
    
    
    
    merchant_name = merchant_name_match.group(1).strip() if merchant_name_match else "Null"
    cleaned_merchant_name = clean_special_characters(merchant_name, excluded_words)
    email_match = clean_n_s(email_match.group(0).strip() if email_match else "Null")
    website = website_match.group(1).strip() if website_match else "Null"
    website = clean_n_s(f"www.{website}.com" if website != "Null" else "Null")
    server_name = server_name_match.group(1).strip() if server_name_match else "Null"
    user_name = user_name_match.group(1).strip() if user_name_match else "Null"
    sales_rep_name = sales_rep_name_match.group(1).strip() if sales_rep_name_match else "Null"
    waiter_name = waiter_name_match.group(1).strip() if waiter_name_match else "Null"
    cashier_name = cashier_name_match.group(1).strip() if cashier_name_match else "Null"
    merchant_address = re.search(f'{re.escape(merchant_name)}(.*?)(?:{re.escape(phone_number_match.group()) if phone_number_match else ""}|$)', text, re.DOTALL)
    merchant_address = merchant_address.group(1).replace('\n', ' ').strip() if merchant_address else "Null"
    merchant_address = merchant_address[:60]

    for word in excluded_words:
        merchant_address = re.sub(rf'\b{word}\b', '', merchant_address, flags=re.IGNORECASE).strip()

    date_time = date_time_match.group(0) if date_time_match else "Null"
    table_number = table_number_match.group(1).strip() if table_number_match else "Null"
    order = re.findall(r'\d+', order_number_match.group(1) if order_number_match else "Null")
    order_number = order[0] if order else "Null"
    
    ref = re.findall(r'\d+', ref_number_match.group(1) if ref_number_match else "Null")
    ref_number = ref[0] if ref else "Null"
    
    ticket = re.findall(r'\d+', ticket_number_match.group(1) if ticket_number_match else "Null")
    ticket_number = ticket[0] if ticket else "Null"

    station = re.findall(r'\d+', station_number_match.group(1) if station_number_match else "Null")
    station_number = station[0] if station else "Null"
    
    guest = re.findall(r'\d+', guest_match.group(1) if guest_match else "Null")
    guest_number = guest[0] if guest else "Null"
    
    dine_in = bool(dine_in_match)

    return {
        "Date and Time": date_time,
        "Merchant Name": cleaned_merchant_name,
        "Merchant Address": merchant_address,
        "Phone Number": phone_number_match.group() if phone_number_match else "Null",
        "Email": email_match,
        "Website" : website,
        "Order Number": order_number,
        "Referance Number": ref_number,
        "Table Number": table_number,
        "Guests": guest_number,
        "Ticket Number": ticket_number,
        "Station Number": station_number,
        "Server Name": server_name,
        "Cashier Name": cashier_name,
        "Waiter Name": waiter_name,
        "User Name" : user_name,
        "sales rep name": sales_rep_name,
        "Dine In": dine_in
    }



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
        st.subheader("Items and Costs")
        for i in range(len(items)):
            st.write(f"    {items[i]}: {item_cost[i]}")

        # Display additional values
        st.subheader("Additional Values")
        for i in range(len(additional_val)):
            st.write(f"    {additional_val[i]}: {val_cost[i]}")

        st.subheader("Extracted Text:")
        st.write(extracted_text)
if __name__ == "__main__":
    main()



# Receipt OCR App

Receipt OCR App is a Streamlit web application that performs Optical Character Recognition (OCR) on receipt images to extract text and analyze receipt information.

## Features

- Upload receipt images (JPEG, PNG) for OCR processing.
- Extract text from uploaded receipt images using Tesseract OCR.
- Analyze extracted text to extract merchant information, item details, and additional values.
- Display extracted information in a user-friendly format.
- Save all image information from a directory to a JSON file.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/receipt-ocr.git
```

2. Navigate to the project directory:

```bash
cd receipt-ocr
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Access the app in your browser at the provided URL.

## Usage

1. Upload a receipt image using the file uploader.
2. Wait for the OCR processing to complete.
3. View the extracted information in the app interface.
4. Optionally, save all image information from a directory to a JSON file by providing the directory path.

## Requirements

- Python 3.x
- Tesseract OCR
- Streamlit
- OpenCV
- Pytesseract

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README to better fit your project's specific features and requirements!

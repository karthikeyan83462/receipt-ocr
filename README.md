---

# Receipt OCR

Receipt OCR is a Streamlit web application that performs optical character recognition (OCR) on receipt images to extract relevant information such as merchant details, items purchased, costs, and additional values.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/karthikeyan83462/receipt-ocr.git
   ```

2. Navigate to the project directory:

   ```bash
   cd receipt-ocr
   ```

3. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure that the following packages are installed on your system:

   - tesseract-ocr
   - freeglut3-dev
   - libgtk2.0-dev

   You can install them using your package manager:

   ```bash
   sudo apt-get install tesseract-ocr freeglut3-dev libgtk2.0-dev
   ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run main.py
   ```

2. Upload an image of the receipt using the file uploader widget.

3. The app will perform OCR on the uploaded image and display the extracted information.

## Live Demo

You can access the live demo of this application at [Receipt OCR Web App](https://receipt-ocr.streamlit.app/).

## License

This project is licensed under the MIT License.

---

"""
Optical Character Recognition (OCR) Module.

This module provides functionality to extract text from images using the
Tesseract OCR engine via the pytesseract library. It reads the Tesseract
executable path from the application settings.
"""
import pytesseract
from PIL import Image
import logging
from sims_gba_ai.config.settings import TESSERACT_CMD_PATH # Import the setting

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Tesseract command path from settings if provided
if TESSERACT_CMD_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH
    logging.info(f"Using Tesseract executable at: {TESSERACT_CMD_PATH}")
# Removed old example line

def extract_text_from_image(image: Image.Image) -> str:
    """
    Extracts text from a given PIL Image object using pytesseract.

    Args:
        image: A PIL Image object.

    Returns:
        The extracted text as a string, or an empty string if OCR fails.
    """
    try:
        # Ensure image is in a format Tesseract can handle well, like RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        text = pytesseract.image_to_string(image)
        logging.info("OCR successful.")
        # Optional: Clean up common OCR noise if needed
        # text = text.strip().replace('\n', ' ')
        return text
    except pytesseract.TesseractNotFoundError:
        logging.error("Tesseract is not installed or not in your PATH. Please install Tesseract.")
        # Depending on requirements, you might want to raise the error or handle it differently
        raise
    except Exception as e:
        logging.error(f"An error occurred during OCR: {e}")
        return "" # Return empty string on other errors

# Example usage (if you want to test this file directly)
# if __name__ == '__main__':
#     try:
#         img_path = 'path/to/your/test_image.png' # Replace with a valid image path
#         img = Image.open(img_path)
#         extracted_text = extract_text_from_image(img)
#         print("Extracted Text:")
#         print(extracted_text)
#     except FileNotFoundError:
#         print(f"Error: Test image not found at {img_path}")
#     except pytesseract.TesseractNotFoundError:
#         print("Error: Tesseract not found. Please ensure it's installed and in PATH.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
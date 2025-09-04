import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
import os
from backend.utils.logger import logger

def extract_text_from_file(file_path: str) -> str:
    logger.info(f"Starting OCR for {file_path}")
    try:
        if file_path.endswith(".pdf"):
            pages = convert_from_path(file_path)
            text = "\n".join([pytesseract.image_to_string(page) for page in pages])
        elif file_path.endswith((".jpg", ".png")):
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file type")
        logger.info(f"OCR completed for {file_path}")
        return text
    except Exception as e:
        logger.error(f"OCR failed for {file_path}: {str(e)}")
        return ""






def parse_fields(text: str) -> dict:
    logger.info("Parsing fields from text")
    try:
        vendor = re.search(r"(?:From|Vendor|Store|Biller):?\s*(.+)", text, re.IGNORECASE)
        date = re.search(r"\b(?:Date|Billing Date):?\s*([\d/.\-]+)", text, re.IGNORECASE)
        amount = re.search(r"\b(?:Total|Amount|Paid|Total ₹|Total Amount):?\s*\$?([\d,.]+)", text, re.IGNORECASE)

        result = {
            "vendor": vendor.group(1).strip() if vendor else "Unknown",
            "date": date.group(1).strip() if date else "Unknown",
            "amount": amount.group(1).strip() if amount else "0.00",
            "category": "Misc"  # Can later map based on known vendor list
        }

        logger.info(f"Parsed data: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to parse fields: {str(e)}")
        return {"vendor": "Unknown", "date": "Unknown", "amount": "0.00", "category": "Misc"}



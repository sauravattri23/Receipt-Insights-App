# Receipt Insights App

A full-stack Streamlit-based application for uploading, parsing, storing, and analyzing receipts or bills using OCR, regex, and algorithmic logic. Built as part of the **Python Intern Assignment: R1 – Full Stack**.

---

## Features

### Upload & Parse
- Upload `.jpg`, `.png`, `.pdf`, or `.txt` receipts
- Extract:
  - Vendor / Biller
  - Date of transaction
  - Amount
  - Category (optional)

### Algorithms
- **Search** by keyword, amount range, or date pattern
- **Sort** by amount, vendor, date, or category
- **Aggregate** statistics:
  - Total, Mean, Median, Mode of expenses
  - Vendor frequency
  - Monthly expenditure trends

### Dashboard
- Tabular view of uploaded receipts
- Pie & bar charts of vendor data
- Line graph for time-series analysis

---

## Project Structure
```bash
receipt_insights_app/
├── backend/
│ ├── ingestion/ # File validation & saving
│ ├── parsing/ # OCR & regex parsing
│ ├── db/ # SQLite schema & inserts
│ ├── algorithms/ # Search, sort, aggregate logic
│ └── utils/ # Logging, validation
├── data/ # Uploaded files, DB
├── logs/ # app.log
├── frontend/
│ └── app.py # Streamlit frontend
└── main.py
└── requirements.txt

```
#### One thing need to download tesseract-ocr [https://github.com/UB-Mannheim/tesseract/wiki] And add path in system variable
##  Setup Instructions

1. **Clone the repository**

```bash
git clone 
cd receipt-insights-app
python main.py

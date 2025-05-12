# Credit Card Transaction Analyzer

A web application that allows users to upload their credit card transaction data in CSV format and view insightful analytics and visualizations.

## Features

- Drag-and-drop CSV file upload
- Interactive data visualization
- Key metrics including:
  - Total spend
  - Maximum transaction amount
  - Average transaction amount
  - Daily spending trends
  - Monthly spending trends
  - Top merchants by spend

## CSV File Format

The application expects a CSV file with the following columns:
- `Date`: Transaction date (format: DD/MM/YY or DD/MM/YYYY)
- `Description`: Merchant name or transaction description
- `Amount`: Transaction amount (positive for purchases, negative for credits)

Example CSV format:
```csv
Date,Description,Amount
01/01/24,GROCERY STORE,50.00
02/01/24,COFFEE SHOP,25.50
03/01/24,REFUND,-30.00
```

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Security Note

This application processes your transaction data locally and does not store any files permanently. All uploaded files are deleted after processing.

## Technologies Used

- Backend: Python (Flask)
- Frontend: HTML, JavaScript, TailwindCSS
- Data Processing: Pandas
- Visualizations: Chart.js 
from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def date_to_str(date_obj):
    """Convert date object to string in DD/MM/YY format"""
    if isinstance(date_obj, pd.Timestamp):
        return date_obj.strftime('%d/%m/%y')
    return str(date_obj)

def analyze_transactions(df):
    # Calculate merchant totals and sort in descending order
    merchant_totals = df.groupby('Description')['Amount'].sum()
    # Sort by amount in descending order and take top 5
    top_merchants = merchant_totals.sort_values(ascending=False).head(5)
    # Convert to OrderedDict to maintain sort order
    top_merchants_dict = OrderedDict((str(k), float(v)) for k, v in top_merchants.items())
    
    # Calculate daily spending using absolute values
    daily_spend = df.groupby(df['Date'].dt.date)['Amount'].apply(lambda x: abs(x.sum())).to_dict()
    
    # Basic analysis of transactions
    analysis = {
        'total_transactions': len(df),
        'total_spend': float(df['Amount'].sum()),
        'max_spend': float(df['Amount'].max()),
        'avg_transaction': float(df['Amount'].mean()),
        'monthly_spend': {date_to_str(k): float(v) for k, v in df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum().items()},
        'top_merchants': top_merchants_dict,
        'daily_spend': {date_to_str(k): float(v) for k, v in daily_spend.items()},
        'daily_spend_details': {
            'spend': {date_to_str(k): float(v) for k, v in df[df['Amount'] > 0].groupby(df['Date'].dt.date)['Amount'].sum().items()},
            'credits': {date_to_str(k): float(abs(v)) for k, v in df[df['Amount'] < 0].groupby(df['Date'].dt.date)['Amount'].sum().items()}
        }
    }
    return analysis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read CSV file with expected columns
            df = pd.read_csv(filepath, usecols=['Date', 'Description', 'Amount'])
            
            # Validate required columns
            required_columns = ['Date', 'Description', 'Amount']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV file must contain Date, Description, and Amount columns")
            
            # Convert date column to datetime with DD/MM/YY format
            try:
                df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
            except ValueError:
                # Try alternative format in case of 4-digit year
                df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
            
            # Perform analysis
            analysis = analyze_transactions(df)
            
            # Clean up
            os.remove(filepath)
            
            return jsonify(analysis)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 400
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True) 
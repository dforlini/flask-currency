import logging
from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')

app= Flask(__name__)

load_dotenv()

API_URL = "http://api.exchangerate.host/convert"
API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        from_currency = request.form.get('from_currency').upper()
        to_currency = request.form.get('to_currency').upper()
        amount = request.form.get('amount')
        
        logging.debug(f"Attempting to convert {amount} from {from_currency} to {to_currency}")
        
        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            logging.warning(f"Invalid amount entered: {amount}")
            return render_template('error.html', message="Invalid amount")
        
        params = {
            'access_key': API_KEY,
            'from': from_currency,
            'to': to_currency,
            'amount': amount
        }
        response = requests.get(API_URL, params=params)
        logging.debug(f"API request sent. Params: {params}")
        
        if response.status_code !=200 or 'error' in response.json():
            logging.error(f"API request failed. Status code: {response.status_code}, Response: {response.text}")
            return render_template('error.html', message="Error with currency conversion")
        
        response_data = response.json()
        if 'result' not in response_data:
            logging.error(f"Converstion result missing in API response. Response data: {response_data} ")
            return render_template('error.html', message="Invalid currency code or API error")
        
        conversion_result = round(response_data['result'], 2)
        logging.info(f"Conversion successful: {amount} {from_currency} to {conversion_result} {to_currency}")
        return render_template('result.html', conversion_result=conversion_result, to_currency=to_currency)
    
    return render_template('index.html')

   

if __name__ == '__main__':
    app.run(debug=True)
        
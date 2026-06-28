import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URL of the internal inventory service container over the Docker bridge network
INVENTORY_URL = os.environ.get("INVENTORY_SERVICE_URL", "http://inventory-service:5001")

@app.route('/', methods=['GET'])
def home():
    try:
        # Communicate with the internal inventory backend API via HTTP GET
        response = requests.get(f"{INVENTORY_URL}/api/stock").json()
        
        # Render a clean HTML interface for the customer browser
        html_content = f"""
        <html>
            <head><title>E-Commerce Portal</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h1>Welcome to the Tech Marketplace!</h1>
                <p style="font-size: 18px;">Available Stock: <strong>{response['stock']} units</strong> of {response['product']}</p>
                <form action="/purchase" method="POST">
                    <input type="submit" value="Buy 1 Laptop" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background-color: #28a745; color: white; border: none; border-radius: 5px;">
                </form>
            </body>
        </html>
        """
        return html_content
    except Exception as e:
        return f"<h1>Error 500</h1><p>Frontend cannot reach Inventory Service! Details: {str(e)}</p>", 500

@app.route('/purchase', methods=['POST'])
def purchase():
    try:
        # Trigger an inventory reduction by sending a POST request to the backend API
        response = requests.post(f"{INVENTORY_URL}/api/buy").json()
        if response.get("status") == "success":
            return f"""
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h2 style="color: green;">Purchase Successful!</h2>
                <p>Remaining Stock: {response['remaining_stock']}</p>
                <a href="/">Go Back to Store</a>
            </body>
            """
        return f"<h2>Order Failed!</h2><p>{response.get('message')}</p><a href='/'>Go Back</a>"
    except Exception as e:
        return jsonify({"error": "Checkout connection failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

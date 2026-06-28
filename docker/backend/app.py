import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Connects to the Redis container using environment variables
redis_host = os.environ.get("REDIS_HOST", "redis-db")
cache = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Pre-populate warehouse inventory metrics if the registry key is missing
if not cache.exists("laptop_stock"):
    cache.set("laptop_stock", 45)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    # Fetch real-time numbers from the data storage layer
    stock = cache.get("laptop_stock")
    return jsonify({"product": "Developer Laptop", "stock": int(stock)})

@app.route('/api/buy', methods=['POST'])
def buy_product():
    stock = int(cache.get("laptop_stock"))
    if stock > 0:
        # Atomically decrement data count to handle rapid clicks safely
        new_stock = cache.decr("laptop_stock")
        return jsonify({"status": "success", "remaining_stock": new_stock})
    return jsonify({"status": "error", "message": "Out of Stock in Warehouse!"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

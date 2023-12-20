from flask import Flask, request, jsonify
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["etherscan"]
collection = db["monitored_addresses"]


@app.route('/add_address', methods=['POST'])
def add_address():
    try:
        data = request.json
        address = data.get('address')

        if address is None:
            return jsonify({"error": "Address is required"}), 400

        # Check if the address is already in the database
        if collection.find_one({"to": address}):
            return jsonify({"error": "Address already exists"}), 400

        # Add the address to the database
        collection.insert_one({"to": address})

        return jsonify({"message": "Address added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port = 5000)

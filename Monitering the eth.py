import requests
import json
import pymongo
import time
import os
from dotenv import load_dotenv
import smtplib
import schedule
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["etherscan"]
collection = db["monitored_addresses"]

url = "https://api-sepolia.etherscan.io/api"

def get_transactions(address):
    payload = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "tag": "latest",
        "startblock": 0,
        "endblock": 99999999,
        "offset": 1,
        "page": 1,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=payload)
    return response.json()

def check_for_new_transactions(address):
    transactions = get_transactions(address)
    if transactions["status"] == "1":
        for transaction in transactions["result"]:
            if collection.find_one({"hash": transaction["hash"]}) is None:
                collection.insert_one(transaction)

                # Send email notification
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(email, email_password)
                    subject = "New transaction found"
                    body = f"New transaction found: {transaction['hash']}"
                    msg = f"Subject: {subject}\n\n{body}"
                    smtp.sendmail(email, email, msg)

                print("New transaction found: " + transaction["hash"])

        # Update the latest transaction in the database
        latest_transaction = transactions["result"][0] if transactions["result"] else None
        if latest_transaction:
            collection.update_one({"to": address}, {"$set": {"latest_transaction": latest_transaction}})
    else:
        print("Error: " + transactions["message"])

def main():

        for address in collection.distinct("to"):
                check_for_new_transactions(address)


if __name__ == "__main__":
    schedule.every(30).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
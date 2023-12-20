from flask import Flask,request
import requests
import json
from datetime import datetime,timedelta

app = Flask(__name__)
url = "https://graphql.bitquery.io"

test_suspicious = ["0x8CE13C17B9C9caE9193538DC2a64ca7be07E2C00","0xcd531ae9efcce479654c4926dec5f6209531ca7b"]



@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/api', methods=['POST'])
def api():
    data_recive = request.json
    attributes= data_recive["attribute"]
    filters = data_recive["filters"]
    refresh = data_recive["refresh"]
    if filters == "date-amount":
        try:
            date_before= attributes["date"]["before"]
            date_after = attributes["date"]["after"]
            amount = attributes["amount"]
            print("hiiiii")
            payload = json.dumps({
   "query": "query($amount: Float , $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {bitcoin(network: bitcoin) {transactions(date: {after: $date_after, before: $date_before}outputValue: {gt:$amount}) {hash}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","amount" : '+amount+'}'})
            headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}

            response = requests.request("POST", url, headers=headers, data=payload)
            print(payload)
            print(response.text)
            print(response.status_code)
            return response.text
        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send


    
            







@app.route('/api2', methods=['POST'])
def api2():
    data_recive = request.json
    attributes= data_recive["attribute"]
    filters = data_recive["filters"]
    refresh = data_recive["refresh"]


    if filters == "date-amount":
        try:
            date_before= attributes["date"]["before"]
            date_after = attributes["date"]["after"]
            amount = attributes["amount"]
            print("hiiiii")
            payload = json.dumps({
   "query": "query($amount: Float , $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}amount: {gt:$amount}) {hash}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","amount" : '+amount+'}'})
            headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}
            print(222222222222222222222222222)
            response = requests.request("POST", url, headers=headers, data=payload)
            print(payload)
            print(response.text)
            print(response.status_code)
            return json.loads(response.text)
        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send


    if filters == "last-30-day-out-amount":
        try:
            acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
            today_date = datetime.today()
            thirty_days_ago = today_date - timedelta(days=30)
            thirty_days_ago_formatted = thirty_days_ago.strftime('%Y-%m-%d')
            today_date__formatted = datetime.today().strftime('%Y-%m-%d')
            date_after  = thirty_days_ago_formatted
            date_before = today_date__formatted
            print("hiiiii")
            
            payload = json.dumps({
   "query": "query($address: [String!], $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}txSender: {in: $address}) {amount}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","address" : '+acc_add+'}'})
            headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}

            response = requests.request("POST", url, headers=headers, data=payload)
            print(payload)
            print(response.text)
            print(response.status_code)
            return json.loads(response.text)
        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send




    if filters == "last-30-day-in-amount":
        try:
            acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
            today_date = datetime.today()
            thirty_days_ago = today_date - timedelta(days=30)
            thirty_days_ago_formatted = thirty_days_ago.strftime('%Y-%m-%d')
            today_date__formatted = datetime.today().strftime('%Y-%m-%d')
            date_after  = thirty_days_ago_formatted
            date_before = today_date__formatted
            print("hiiiii")
            
            payload = json.dumps({
   "query": "query($address: [String!], $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}txTo: {in: $address}) {amount}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","address" : '+acc_add+'}'})
            headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}

            response = requests.request("POST", url, headers=headers, data=payload)
            print(payload)
            print(response.text)
            print(response.status_code)
            return json.loads(response.text)
        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send


    if filters=="last-50-transaction":
        try:
            acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
            payload = json.dumps({
   "query": "query($address:[String!]){\n  ethereum(network: ethereum) {\n    transactions(\n      txSender: {in:$address}\n      options: {limit: 50}\n    ) {\n      hash\n    }\n  }\n}\n",
   "variables": "{\"address\" : "+acc_add+"}"
})
            haders = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}

            response = requests.request("POST", url, headers=haders, data=payload)
            print(payload)
            print(response.text)
            print(response.status_code)
            return json.loads(response.text)

        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send

    
    if filters == "transaction-detail":
        try:
            hash = attributes["hash"]
            payload = json.dumps({
   "query": "query ($hash:String) {\n  ethereum(network: ethereum) {\n    transactions(txHash: {is: $hash}) {\n      amount\n      date {\n        date\n      }\n      sender {\n        address\n      }\n      to {\n        address\n      }\n    }\n  }\n}\n",
   "variables": "{\"hash\": \""+hash+"\"}"
})
            headers = {
   'Content-Type': 'application/json',
   'X-API-KEY': ''
}


            response = requests.request("POST", url, headers=headers, data=payload) 
            print(payload)
            print(response.text)
            print(response.status_code)
            return json.loads(response.text)

        except Exception as e:
            data_send = {"error":"Please send the proper Attribute."}
            print(e)
            return data_send

# @app.route('/api2/date-amount/<data_before>/<data_after>/<amount>', methods=['GET'])
# def date_amount(data_after,data_before,amount):
#     try:
#         print("hiiiii")
#         payload = json.dumps({
#    "query": "query($amount: Float , $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}amount: {gt:$amount}) {hash}}}","variables": '{"date_after":"'+data_after+'","date_before":"'+data_before+'","amount" : '+amount+'}'})
#         headers = {
#    'Content-Type': 'application/json',
#    'X-API-KEY': ''
# }

#         response = requests.request("POST", url, headers=headers, data=payload)
#         print(payload)
#         print(response.text)
#         print(response.status_code)
#         return response.text
#     except Exception as e:
#         data_send = {"error":"Please send the proper Attribute."}
#         print(e)
#         return data_send

# @app.route('/api2/last-30-day-out-amount', methods=['GET'])
# def last_30_day_out_amount():
#     try:
#         acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
#         today_date = datetime.today()
#         thirty_days_ago = today_date - timedelta(days=30)
#         thirty_days_ago_formatted = thirty_days_ago.strftime('%Y-%m-%d')
#         today_date__formatted = datetime.today().strftime('%Y-%m-%d')
#         date_after  = thirty_days_ago_formatted
#         date_before = today_date__formatted
#         print("hiiiii")
        
#         payload = json.dumps({
#    "query": "query($address: [String!], $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}txSender: {in: $address}) {amount}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","address" : '+acc_add+'}'})
#         headers = {
#    'Content-Type': 'application/json',
#    'X-API-KEY': ''
# }

#         response = requests.request("POST", url, headers=headers, data=payload)
#         print(payload)
#         print(response.text)
#         print(response.status_code)
#         return response.text
#     except Exception as e:
#         data_send = {"error":"Please send the proper Attribute."}
#         print(e)
#         return data_send

# @app.route('/api2/last-30-day-in-amount', methods=['GET'])

# def last_30_day_in_amount():
#     try:
#         acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
#         today_date = datetime.today()
#         thirty_days_ago = today_date - timedelta(days=30)
#         thirty_days_ago_formatted = thirty_days_ago.strftime('%Y-%m-%d')
#         today_date__formatted = datetime.today().strftime('%Y-%m-%d')
#         date_after  = thirty_days_ago_formatted
#         date_before = today_date__formatted
#         print("hiiiii")
        
#         payload = json.dumps({
#    "query": "query($address: [String!], $date_after:ISO8601DateTime, $date_before:ISO8601DateTime) {ethereum(network: ethereum) {transactions(date: {after: $date_after, before: $date_before}txTo: {in: $address}) {amount}}}","variables": '{"date_after":"'+date_after+'","date_before":"'+date_before+'","address" : '+acc_add+'}'})
#         headers = {
#    'Content-Type': 'application/json',
#    'X-API-KEY': ''
# }

#         response = requests.request("POST", url, headers=headers, data=payload)
#         print(payload)
#         print(response.text)
#         print(response.status_code)
#         return response.text
#     except Exception as e:
#         data_send = {"error":"Please send the proper Attribute."}
#         print(e)
#         return data_send

# @app.route('/api2/last-50-transaction', methods=['GET'])
# def last_50_transaction():
#     try:
#         acc_add=  '[' + ', '.join(f'"{item}"' for item in test_suspicious) + ']'
#         payload = json.dumps({
#    "query": "query($address:[String!]){\n  ethereum(network: ethereum) {\n    transactions(\n      txSender: {in:$address}\n      options: {limit: 50}\n    ) {\n      hash\n    }\n  }\n}\n",
#    "variables": "{\"address\" : "+acc_add+"}"
# })
#         haders = {
#    'Content-Type': 'application/json',
#    'X-API-KEY': ''
# }

#         response = requests.request("POST", url, headers=haders, data=payload)
#         print(payload)
#         print(response.text)
#         print(response.status_code)
#         return response.text

#     except Exception as e:
#         data_send = {"error":"Please send the proper Attribute."}
#         print(e)
#         return data_send

# @app.route('/api2/transaction-detail/<hash>', methods=['GET'])
# def transaction_detail(hash):
#     try:
#         payload = json.dumps({
#    "query": "query ($hash:String) {\n  ethereum(network: ethereum) {\n    transactions(txHash: {is: $hash}) {\n      amount\n      date {\n        date\n      }\n      sender {\n        address\n      }\n      to {\n        address\n      }\n    }\n  }\n}\n",
#    "variables": "{\"hash\": \""+hash+"\"}"
# })
#         headers = {
#    'Content-Type': 'application/json',
#    'X-API-KEY': ''
# }


#         response = requests.request("POST", url, headers=headers, data=payload) 
#         print(payload)
#         print(response.text)
#         print(response.status_code)
#         return response.text

#     except Exception as e:
#         data_send = {"error":"Please send the proper Attribute."}
#         print(e)
#         return data_send

app.run(debug=True)

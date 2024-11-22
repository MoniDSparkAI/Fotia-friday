 
from flask import Flask, jsonify, request
import pymysql
import requests
from flask_cors import CORS
 
app = Flask(__name__)
 
# Enable CORS for all routes
CORS(app)
 
# Alchemy API Key and Base URL
alchemy_api_key = "rbcArvD4It1EDhUyGgi4G69U_39LRn0Q"  # Replace with your Alchemy API Key
alchemy_base_url = "https://polygon-mainnet.g.alchemy.com/v2"
 
# Database configuration for MySQL
db_config = {
    "host": "141.136.42.65",
    "user": "root",
    "password": "Test@2024",
    "database": "fotia_wallet",  # Correct database name
}
 
# Fetch wallet address for a user from the 'wallets' table
def get_wallet_address(user_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT wallet_address FROM wallets WHERE user_id = %s"  # Correct table name 'wallets'
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        connection.close()
 
# Fetch transaction history using Alchemy API for a given wallet address
def get_transaction_history(wallet_address):
    if not wallet_address:
        return {"error": "Invalid wallet address"}
 
    try:
        # API request to Alchemy to get the transaction history
        url = f"{alchemy_base_url}/{alchemy_api_key}"
        payload = {
            "jsonrpc": "2.0",
            "method": "alchemy_getAssetTransfers",
            "params": [{
                "fromBlock": "0x0",  # Start from the genesis block
                "toBlock": "latest",
                "fromAddress": wallet_address,  # Transactions sent from the wallet
                "category": ["external", "internal", "erc20", "erc721", "erc1155"],  # Fetch all categories
                "withMetadata": True,  # Include detailed metadata
                "excludeZeroValue": False  # Include transactions with zero value
            }],
            "id": 1
        }
 
        # Make the request to Alchemy's API
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
 
        # Check if the request was successful
        if response.status_code == 200:
            transactions = response.json()
            if "result" in transactions and "transfers" in transactions["result"]:
                wallet_transactions = []
                for tx in transactions["result"]["transfers"]:
                    # Format and collect transaction data
                    wallet_transactions.append({
                        "hash": tx.get("hash", "N/A"),
                        "from": tx.get("from", "N/A"),
                        "to": tx.get("to", "N/A"),
                        "value": tx.get("value", "N/A"),  # Value in native token or token units
                        "asset": tx.get("asset", "N/A"),  # Token or currency name
                        "timestamp": tx.get("metadata", {}).get("blockTimestamp", "N/A"),
                        "block_number": tx.get("blockNum", "N/A"),
                        "category": tx.get("category", "N/A")  # Transaction category
                    })
                return wallet_transactions
            else:
                return {"error": "No transactions found or error occurred."}
        else:
            return {"error": f"Failed to fetch data from Alchemy API: {response.status_code}"}
 
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
 
# Endpoint to get transactions for a user based on user ID
@app.route('/get-transactions', methods=['POST'])
def get_transactions():
    data = request.json
    user_id = data.get("user_id")
   
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
 
    wallet_address = get_wallet_address(user_id)
    if not wallet_address:
        return jsonify({"error": "Wallet address not found"}), 404
 
    transactions = get_transaction_history(wallet_address)
    return jsonify(transactions)
 
if __name__ == "__main__":
    app.run(debug=True, port=5008)
 

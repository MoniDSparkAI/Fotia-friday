# from flask import Flask, jsonify, request
# from web3 import Web3
# import pymysql
# import datetime
# import json

# app = Flask(__name__)

# # Replace with your Alchemy Polygon RPC URL
# alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
# web3 = Web3(Web3.HTTPProvider(alchemy_rpc_url))

# # USDT contract configuration on Polygon
# usdt_contract_address = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
# usdt_abi = json.loads('''[ 
#     {
#         "constant": true,
#         "inputs": [
#             {
#                 "name": "account",
#                 "type": "address"
#             }
#         ],
#         "name": "balanceOf",
#         "outputs": [
#             {
#                 "name": "",
#                 "type": "uint256"
#             }
#         ],
#         "payable": false,
#         "stateMutability": "view",
#         "type": "function"
#     },
#     {
#         "constant": false,
#         "inputs": [
#             {
#                 "name": "to",
#                 "type": "address"
#             },
#             {
#                 "name": "value",
#                 "type": "uint256"
#             }
#         ],
#         "name": "transfer",
#         "outputs": [
#             {
#                 "name": "",
#                 "type": "bool"
#             }
#         ],
#         "payable": false,
#         "stateMutability": "nonpayable",
#         "type": "function"
#     }
# ]''')

# # Initialize USDT contract
# usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_abi)

# # MySQL database connection
# def db_connection():
#     return pymysql.connect(
#         host="141.136.42.65",
#         user="root",
#         password="Test@2024",
#         database="send_usdt",
#         cursorclass=pymysql.cursors.DictCursor,
#     )

# @app.route('/send', methods=['POST'])
# def send_usdt():
#     data = request.json
#     user_id = data.get('user_id')
#     from_address = data.get('from_address')
#     private_key = data.get('private_key')
#     to_address = data.get('to_address')
#     amount = data.get('amount')

#     if not all([user_id, from_address, private_key, to_address, amount]):
#         return jsonify({"error": "Missing required fields"}), 400

#     if not (web3.is_address(from_address) and web3.is_address(to_address)):
#         return jsonify({"error": "Invalid from or to address"}), 400

#     amount_in_wei = int(float(amount) * 10**6)

#     try:
#         balance = usdt_contract.functions.balanceOf(from_address).call()
#         if balance < amount_in_wei:
#             return jsonify({"error": "Insufficient USDT balance"}), 400

#         gas_price = web3.to_wei('55', 'gwei')
#         nonce = web3.eth.get_transaction_count(from_address)
#         txn = usdt_contract.functions.transfer(to_address, amount_in_wei).build_transaction({
#             'chainId': 137,
#             'gas': 60000,
#             'gasPrice': gas_price,
#             'nonce': nonce
#         })

#         signed_txn = web3.eth.account.sign_transaction(txn, private_key)
#         txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

#         # Wait for the transaction to be mined
#         txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

#         # Determine the transaction status based on receipt
#         txn_status = "pending"
#         if txn_receipt.status == 1:
#             txn_status = "success"
#         elif txn_receipt.status == 0:
#             txn_status = "failure"

#         with db_connection() as connection:
#             with connection.cursor() as cursor:
#                 sql = """
#                     INSERT INTO send_token (
#                         user_id, from_address, to_address, amount, txn_hash,
#                         block_number, gas_used, status, created_at
#                     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(sql, (
#                     user_id, from_address, to_address, amount,
#                     txn_hash.hex(), txn_receipt.blockNumber,
#                     txn_receipt.gasUsed, txn_status,
#                     datetime.datetime.now()
#                 ))
#                 connection.commit()

#         return jsonify({
#             "txn_hash": txn_hash.hex(),
#             "block_number": txn_receipt.blockNumber,
#             "status": txn_status
#         }), 200

#     except Exception as e:
#         return jsonify({"error": f"Transaction failed: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5006)

from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from web3 import Web3
import pymysql
import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your updated Alchemy Polygon RPC URL
alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/rbcArvD4It1EDhUyGgi4G69U_39LRn0Q"
web3 = Web3(Web3.HTTPProvider(alchemy_rpc_url))

# Check connection
if not web3.is_connected():
    raise ConnectionError("Failed to connect to the Polygon network")

# USDT contract configuration on Polygon
usdt_contract_address = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
usdt_abi = json.loads('''[
    {
        "constant": true,
        "inputs": [
            {
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]''')

# Initialize USDT contract
usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_abi)

# MySQL database connection
def db_connection():
    return pymysql.connect(
        host="141.136.42.65",
        user="root",
        password="Test@2024",
        database="send_usdt",
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.route('/send', methods=['POST'])
def send_usdt():
    data = request.json
    user_id = data.get('user_id')
    from_address = data.get('from_address')
    private_key = data.get('private_key')
    to_address = data.get('to_address')
    amount = data.get('amount')

    if not all([user_id, from_address, private_key, to_address, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    if not (web3.is_address(from_address) and web3.is_address(to_address)):
        return jsonify({"error": "Invalid from or to address"}), 400

    try:
        # Convert amount to smallest unit (USDT has 6 decimals)
        amount_in_wei = int(float(amount) * 10**6)

        # Fetch the current nonce
        nonce = web3.eth.get_transaction_count(from_address, "pending")

        # Check USDT balance
        balance = usdt_contract.functions.balanceOf(from_address).call()
        if balance < amount_in_wei:
            return jsonify({"error": "Insufficient USDT balance"}), 400

        # Gas price and transaction configuration
        gas_price = web3.eth.gas_price
        txn = usdt_contract.functions.transfer(to_address, amount_in_wei).build_transaction({
            'chainId': 137,
            'gas': 100000,  # Updated to handle sufficient gas
            'gasPrice': gas_price,
            'nonce': nonce
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash, timeout=180)

        # Transaction status
        txn_status = "success" if txn_receipt.status == 1 else "failure"

        # Store transaction details in the database
        with db_connection() as connection:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO send_token (
                        user_id, from_address, to_address, amount, txn_hash,
                        block_number, gas_used, status, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    user_id, from_address, to_address, amount,
                    txn_hash.hex(), txn_receipt.blockNumber,
                    txn_receipt.gasUsed, txn_status,
                    datetime.datetime.now()
                ))
                connection.commit()

        return jsonify({
            "txn_hash": txn_hash.hex(),
            "block_number": txn_receipt.blockNumber,
            "status": txn_status
        }), 200

    except Exception as e:
        return jsonify({"error": f"Transaction failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5006)

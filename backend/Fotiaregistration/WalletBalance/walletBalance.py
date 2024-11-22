
from flask import Flask, request, jsonify
from web3 import Web3
import json
import mysql.connector
import logging
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow all origins by default

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Alchemy Polygon RPC URL
alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
web3 = Web3(Web3.HTTPProvider(alchemy_rpc_url))

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
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]''')

# Initialize USDT contract
usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_abi)

# Database connection configuration
db_config = {
    'host': '141.136.42.65',
    'user': 'root',
    'password': 'Test@2024',
    'database': 'fotia_wallet'
}


def get_wallet_address_from_db(user_id):
    try:
        logging.info(f"Fetching wallet address for user_id: {user_id}")
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT wallet_address FROM wallets WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()

                # Ensure cursor is fully read to avoid 'Unread result found' error
                cursor.fetchall()  # Ensures no remaining unprocessed results

                if result:
                    logging.info(f"Found wallet address: {result['wallet_address']} for user_id: {user_id}")
                else:
                    logging.warning(f"No wallet address found for user_id: {user_id}")
                return result['wallet_address'] if result else None
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        raise Exception(f"Database error: {err}")


@app.route('/get_wallet_address/<user_id>', methods=['GET'])
def get_wallet_address(user_id):
    try:
        wallet_address = get_wallet_address_from_db(user_id)
        if not wallet_address:
            return jsonify({"error": "Wallet not found for the given user ID"}), 404
        return jsonify({"wallet_address": wallet_address}), 200
    except Exception as e:
        logging.error(f"Error while fetching wallet address: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    try:
        wallet_address = get_wallet_address_from_db(user_id)
        if not wallet_address:
            return jsonify({"error": "Wallet not found for the given user ID"}), 404

        if not web3.is_address(wallet_address):
            return jsonify({"error": "Invalid wallet address"}), 400

        # Fetch USDT balance
        balance_usdt = usdt_contract.functions.balanceOf(wallet_address).call()
        decimals = usdt_contract.functions.decimals().call()
        balance_in_usdt = balance_usdt / (10 ** decimals)

        # Fetch MATIC balance
        balance_matic = web3.eth.get_balance(wallet_address)
        balance_in_matic = web3.from_wei(balance_matic, 'ether')

        logging.info(f"Balances for user_id {user_id} - USDT: {balance_in_usdt}, MATIC: {balance_in_matic}")

        return jsonify({
            "usdt_balance": balance_in_usdt,
            "matic_balance": balance_in_matic
        }), 200

    except Exception as e:
        logging.error(f"Error while fetching balances: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5005)

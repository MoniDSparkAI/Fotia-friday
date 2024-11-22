# import qrcode
# from flask import Flask, jsonify, request, send_file
# from flask_cors import CORS
# from io import BytesIO
# import pymysql
# import requests
# import datetime
# import logging
 
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
 
# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
 
# # Database connection details for fotia_transaction
# db_config = {
#     'host': '141.136.42.65',
#     'user': 'root',
#     'password': 'Test@2024',
#     'database': 'fotia_transaction'
# }
 
# # Fortio's new USDT wallet address
# fortio_usdt_address = '0x4E97447B035c13FfEEAB8D28d1F8D11B9Eb48636'.lower()  # Normalize to lowercase
 
# # Alchemy API URL
# alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
 
 
# @app.route('/generate_qr_code', methods=['GET'])
# def generate_qr_code():
#     """Generate a QR code for the Fortio wallet address."""
#     wallet_address = fortio_usdt_address
 
#     # Generate QR code
#     img = qrcode.make(wallet_address)
#     buffer = BytesIO()
#     img.save(buffer, 'PNG')
#     buffer.seek(0)
#     return send_file(buffer, mimetype='image/png')
 
 
# def extract_recipient_from_logs(logs, expected_address):
#     """
#     Extract and verify the recipient address from transaction logs.
 
#     Args:
#         logs (list): Transaction logs from the receipt.
#         expected_address (str): Address to validate against.
 
#     Returns:
#         bool: True if recipient matches the expected address, False otherwise.
#     """
#     for log in logs:
#         # Only process logs with the Transfer topic (ERC-20 Transfer event)
#         if log.get('topics') and log['topics'][0] == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
#             if len(log['topics']) > 2:
#                 recipient = '0x' + log['topics'][2][26:].lower()  # Extract recipient address
#                 logging.debug(f"Found recipient address: {recipient}")
#                 if recipient == expected_address:
#                     return True
#     return False
 
 
# def check_transaction_details(tx_hash, expected_address):
#     """
#     Verify transaction details using Alchemy API.
 
#     Args:
#         tx_hash (str): Transaction hash to verify.
#         expected_address (str): Address to validate against.
 
#     Returns:
#         str: 'Success', 'Failure', 'Pending', or 'Invalid Address'.
#     """
#     try:
#         # Fetch transaction details
#         payload = {
#             "jsonrpc": "2.0",
#             "method": "eth_getTransactionReceipt",
#             "params": [tx_hash],
#             "id": 1
#         }
#         logging.debug("Sending request to Alchemy for transaction receipt...")
#         response = requests.post(alchemy_rpc_url, json=payload)
#         receipt_data = response.json()
 
#         if 'result' not in receipt_data or receipt_data['result'] is None:
#             return 'Pending'  # Transaction not yet confirmed
 
#         transaction_receipt = receipt_data['result']
#         logging.debug(f"Transaction Receipt: {transaction_receipt}")
 
#         # Check if the transaction was successful
#         if transaction_receipt['status'] != '0x1':
#             return 'Failure'
 
#         # Extract and verify the recipient address from logs
#         if not extract_recipient_from_logs(transaction_receipt['logs'], expected_address):
#             return 'Invalid Address'
 
#         return 'Success'
#     except Exception as e:
#         logging.error(f"Error in check_transaction_details: {e}")
#         return f'error: {str(e)}'
 
 
# @app.route('/confirm_transaction', methods=['POST'])
# def confirm_transaction():
#     """Store transaction details in the MySQL database if verified as successful."""
#     try:
#         # Parse the request JSON
#         data = request.json
#         user_id = data.get('user_id')
#         from_address = data.get('from_address')
#         to_address = data.get('to_address').lower()  # Normalize to lowercase for validation
#         amount = data.get('amount')
#         gas_fee = data.get('gas_fee')
#         tx_hash = data.get('tx_hash')
 
#         # Validate required fields
#         if not all([user_id, from_address, to_address, amount, gas_fee, tx_hash]):
#             return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
 
#         # Validate the to_address
#         if to_address != fortio_usdt_address:
#             return jsonify({'status': 'error', 'message': 'Invalid to_address. Must match the Fortio wallet address.'}), 400
 
#         # Check if the user_id exists in the users table
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id FROM fotia_database.users WHERE id = %s", (user_id,))
#             user = cursor.fetchone()
#             if not user:
#                 return jsonify({'status': 'error', 'message': 'User ID not found in the database.'}), 404
 
#         # Verify transaction using Alchemy API
#         tx_status = check_transaction_details(tx_hash, fortio_usdt_address)
 
#         if tx_status == 'Success':
#             try:
#                 # Insert successful transaction into the database
#                 with connection.cursor() as cursor:
#                     sql = """
#                         INSERT INTO transaction (user_id, from_address, to_address, amount, gas_fee, tx_hash, status, date)
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                     """
#                     cursor.execute(sql, (
#                         user_id, from_address, to_address, amount, gas_fee, tx_hash, tx_status, datetime.datetime.now()
#                     ))
#                     connection.commit()
#                 return jsonify({'status': 'success', 'message': 'Transaction recorded successfully'}), 200
#             except Exception as e:
#                 logging.error(f"Database Error: {e}")
#                 return jsonify({'status': 'error', 'message': str(e)}), 500
#             finally:
#                 connection.close()
#         elif tx_status == 'Failure':
#             return jsonify({'status': 'failure', 'message': 'Transaction failed. Please retry.'}), 400
#         elif tx_status == 'Pending':
#             return jsonify({'status': 'pending', 'message': 'Transaction is pending. Please wait and try again later.'}), 202
#         elif tx_status == 'Invalid Address':
#             return jsonify({'status': 'error', 'message': 'Transaction not made to the expected address.'}), 400
#         elif 'error' in tx_status:
#             return jsonify({'status': 'error', 'message': tx_status}), 500
#         else:
#             return jsonify({'status': 'error', 'message': 'Unexpected transaction status.'}), 500
 
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500
 
 
# if __name__ == '__main__':
#     app.run(debug=True, port=5007)



























from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pymysql
import requests
import datetime
import logging
import qrcode
from io import BytesIO
 
app = Flask(__name__)
CORS(app)
 
# Configure logging
logging.basicConfig(level=logging.DEBUG)
 
# Database connection details
db_config = {
    'host': '141.136.42.65',
    'user': 'root',
    'password': 'Test@2024',
    'database': 'fotia_transaction'
}
 
# Fortio's USDT wallet address
fortio_usdt_address = '0x4e97447b035c13ffeeab8d28d1f8d11b9eb48636'  # Lowercase for consistency
 
# Alchemy API URL
alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
 
# Extract addresses, value, and gas fee from transaction logs
def extract_details_from_logs(logs, expected_address):
    from_address = None
    to_address = None
    value = None
    is_correct_recipient = False
 
    for log in logs:
        if log.get('topics') and log['topics'][0] == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
            if len(log['topics']) > 2:
                to_address = '0x' + log['topics'][2][26:].lower()
                from_address = '0x' + log['topics'][1][26:].lower()
 
                if to_address == expected_address:
                    is_correct_recipient = True
                    value = int(log['data'], 16) / (10 ** 6)  # Assuming the value is in smallest USDT units (6 decimals for USDT on Polygon)
 
    return from_address, to_address, value, is_correct_recipient
 
# Check transaction details
def check_transaction_details(tx_hash, expected_address):
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1
        }
        response = requests.post(alchemy_rpc_url, json=payload)
        receipt_data = response.json()
 
        if 'result' not in receipt_data or receipt_data['result'] is None:
            return 'Pending', None, None, None, None
 
        transaction_receipt = receipt_data['result']
 
        if transaction_receipt['status'] != '0x1':
            return 'Failed', None, None, None, None
 
        from_address, to_address, value, is_correct_recipient = extract_details_from_logs(transaction_receipt['logs'], expected_address)
        gas_fee = int(transaction_receipt['gasUsed'], 16) * int(transaction_receipt['effectiveGasPrice'], 16) / (10 ** 18)
 
        if not is_correct_recipient:
            return 'Invalid Address', from_address, to_address, value, gas_fee
 
        return 'Success', from_address, to_address, value, gas_fee
    except Exception as e:
        logging.error(f"Error in check_transaction_details: {e}")
        return f'error: {str(e)}', None, None, None, None
 
@app.route('/confirm_transaction', methods=['POST'])
def confirm_transaction():
    try:
        data = request.json
        user_id = data.get('user_id')
        tx_hash = data.get('tx_hash')
 
        if not user_id or not tx_hash:
            return jsonify({'status': 'error', 'message': 'User ID and transaction hash are required.'}), 400
 
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM fotia_database.users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'status': 'error', 'message': 'User ID not found in the database.'}), 404
 
        tx_status, from_address, to_address, value, gas_fee = check_transaction_details(tx_hash, fortio_usdt_address)
 
        if tx_status == 'Success':
            try:
                with connection.cursor() as cursor:
                    # Insert the transaction into the database with correct amount
                    sql = """
                        INSERT INTO transaction (user_id, tx_hash, from_address, to_address, amount, gas_fee, status, date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    # Ensure the correct value (amount) is passed in the database query as a float
                    cursor.execute(sql, (user_id, tx_hash, from_address, to_address, round(value, 6), gas_fee, tx_status, datetime.datetime.now()))
                    connection.commit()
                return jsonify({'status': 'success', 'message': f'Transaction successfully recorded. Amount received: {round(value, 6)} USDT.'}), 200
 
            finally:
                connection.close()
 
        elif tx_status == 'Failed':
            return jsonify({'status': 'failed', 'message': 'Transaction failed.'}), 400
 
        elif tx_status == 'Pending':
            return jsonify({'status': 'pending', 'message': 'The transaction was not made to the correct Fortio wallet address.'}), 202
 
        elif tx_status == 'Invalid Address':
            return jsonify({'status': 'error', 'message': 'The transaction was not made to the correct Fortio wallet address.'}), 400
 
        elif 'error' in tx_status:
            return jsonify({'status': 'error', 'message': tx_status}), 500
 
        else:
            return jsonify({'status': 'error', 'message': 'Unexpected transaction status.'}), 500
 
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500
 
@app.route('/generate_qr_code', methods=['GET'])
def generate_qr_code():
    """Generate a QR code for the Fortio wallet address."""
    wallet_address = fortio_usdt_address
 
    # Generate QR code
    img = qrcode.make(wallet_address)
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')
 
if __name__ == '__main__':
    app.run(debug=True, port=5007)
 
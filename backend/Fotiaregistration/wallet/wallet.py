# from flask import Flask, jsonify, request
# from web3 import Web3
# import pymysql
# from flask_cors import CORS
# import logging
# from flask_mail import Mail, Message
 
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
 
# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
 
# # Flask-Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
 
# mail = Mail(app)
 
# # Replace with your Alchemy Polygon RPC URL
# alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
# web3 = Web3(Web3.HTTPProvider(alchemy_rpc_url))
 
# # Check connection
# if not web3.is_connected():
#     logging.error("Failed to connect to the Polygon network")
#     raise ConnectionError("Failed to connect to the Polygon network")
# else:
#     logging.info("Connected to the Polygon network")
 
# # Database configurations
# fotia_database_config = {
#     'host': '141.136.42.65',
#     'user': 'root',
#     'password': 'Test@2024',
#     'database': 'fotia_database',
#     'port': 3306
# }
 
# fotia_wallet_config = {
#     'host': '141.136.42.65',
#     'user': 'root',
#     'password': 'Test@2024',
#     'database': 'fotia_wallet',
#     'port': 3306
# }
 
# @app.route('/create_wallet', methods=['POST'])
# def create_wallet():
#     try:
#         # Parse the request
#         data = request.get_json()
#         user_id = data.get('user_id')
       
#         # Validate user_id
#         if not user_id:
#             logging.error("User ID is missing in the request")
#             return jsonify({"error": "User ID is required"}), 400
 
#         # Generate a new wallet
#         account = web3.eth.account.create()
#         private_key = account._private_key.hex()
#         address = account.address
#         logging.info(f"Generated wallet - Address: {address}, Private Key: {private_key}")
 
#         # Connect to `fotia_database` to verify user ID and fetch email
#         fotia_db_connection = pymysql.connect(**fotia_database_config)
#         user_email = None
#         try:
#             with fotia_db_connection.cursor() as cursor:
#                 # Fetch email based on user_id
#                 cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
#                 user = cursor.fetchone()
#                 if not user:
#                     logging.error(f"Invalid user ID: {user_id}")
#                     return jsonify({"error": "Invalid user ID"}), 404
#                 user_email = user[0]  # Assuming email is the first column
#         finally:
#             fotia_db_connection.close()
 
#         # Connect to `fotia_wallet` to store wallet details
#         fotia_wallet_connection = pymysql.connect(**fotia_wallet_config)
#         try:
#             with fotia_wallet_connection.cursor() as cursor:
#                 # Insert wallet details into the wallets table
#                 sql = """
#                     INSERT INTO wallets (user_id, wallet_address, private_key, created_at)
#                     VALUES (%s, %s, %s, NOW())
#                 """
#                 cursor.execute(sql, (user_id, address, private_key))
#                 fotia_wallet_connection.commit()
#                 logging.info("Wallet details saved to the fotia_wallet database")
#         finally:
#             fotia_wallet_connection.close()
 
#         # Send email with wallet details
#         try:
#             msg = Message(
#                 'Wallet Created Successfully',  # Subject
#                 recipients=[user_email],        # Add the recipient's email here
#                 sender='noreply@fotia.cloud'  # Set the sender email
#             )
 
#             # Add the email body content
#             msg.body = f"Your new wallet address is: {address}\nYour private key is: {private_key}"
 
#             # Send the email
#             mail.send(msg)
#             logging.info("Email sent successfully.")
#         except Exception as e:
#             logging.error(f"Failed to send email: {str(e)}")
 
#         return jsonify({
#             "message": "Wallet created successfully, and email sent to the user.",
#             "address": address,
#             "private_key": private_key
#         }), 200
 
#     except pymysql.MySQLError as db_err:
#         logging.exception("Database error occurred")
#         return jsonify({"error": f"Database error: {str(db_err)}"}), 500
#     except Exception as e:
#         logging.exception("An unexpected error occurred")
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
 
 
# if __name__ == '__main__':
#     # Run Flask app with debugging enabled and avoid reloading issues
#     app.run(debug=True, port=5004, use_reloader=False)
 
 
 
 
 
from flask import Flask, jsonify, request
from web3 import Web3
import pymysql
from flask_cors import CORS
import logging
from flask_mail import Mail, Message
 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
 
# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
 
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'datasparkaisolutions@gmail.com'
app.config['MAIL_PASSWORD'] = 'mrgnqanvdwzlkcae'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
 
mail = Mail(app)
 
# Replace with your Alchemy Polygon RPC URL
alchemy_rpc_url = "https://polygon-mainnet.g.alchemy.com/v2/LXpg0b04ojjCWq9k26OPl9iQTIpLnpEf"
web3 = Web3(Web3.HTTPProvider(alchemy_rpc_url))
 
# Check connection
if not web3.is_connected():
    logging.error("Failed to connect to the Polygon network")
    raise ConnectionError("Failed to connect to the Polygon network")
else:
    logging.info("Connected to the Polygon network")
 
# Database configurations
fotia_database_config = {
    'host': '141.136.42.65',
    'user': 'root',
    'password': 'Test@2024',
    'database': 'fotia_database',
    'port': 3306
}
 
fotia_wallet_config = {
    'host': '141.136.42.65',
    'user': 'root',
    'password': 'Test@2024',
    'database': 'fotia_wallet',
    'port': 3306
}
 
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        # Parse the request
        data = request.get_json()
        user_id = data.get('user_id')
       
        # Validate user_id
        if not user_id:
            logging.error("User ID is missing in the request")
            return jsonify({"error": "User ID is required"}), 400
        
        # Connect to `fotia_wallet` to check if wallet already exists
        fotia_wallet_connection = pymysql.connect(**fotia_wallet_config)
        wallet_details = None
        try:
            with fotia_wallet_connection.cursor() as cursor:
                # Check if wallet exists for the user
                cursor.execute("SELECT wallet_address, private_key FROM wallets WHERE user_id = %s", (user_id,))
                wallet_details = cursor.fetchone()
        finally:
            fotia_wallet_connection.close()
        
        # If wallet exists, return the wallet details
        if wallet_details:
            logging.info(f"Wallet already exists for user {user_id}")
            return jsonify({
                "message": "Wallet already created.",
                "address": wallet_details[0],
                "private_key": wallet_details[1]
            }), 200

        # Generate a new wallet if none exists
        account = web3.eth.account.create()
        private_key = account._private_key.hex()
        address = account.address
        logging.info(f"Generated wallet - Address: {address}, Private Key: {private_key}")
 
        # Connect to `fotia_database` to verify user ID and fetch email
        fotia_db_connection = pymysql.connect(**fotia_database_config)
        user_email = None
        try:
            with fotia_db_connection.cursor() as cursor:
                # Fetch email based on user_id
                cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                if not user:
                    logging.error(f"Invalid user ID: {user_id}")
                    return jsonify({"error": "Invalid user ID"}), 404
                user_email = user[0]  # Assuming email is the first column
        finally:
            fotia_db_connection.close()
 
        # Store wallet details in the database
        fotia_wallet_connection = pymysql.connect(**fotia_wallet_config)
        try:
            with fotia_wallet_connection.cursor() as cursor:
                # Insert wallet details into the wallets table
                sql = """
                    INSERT INTO wallets (user_id, wallet_address, private_key, created_at)
                    VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(sql, (user_id, address, private_key))
                fotia_wallet_connection.commit()
                logging.info("Wallet details saved to the fotia_wallet database")
        finally:
            fotia_wallet_connection.close()
 
        # Send email with wallet details
        try:
            msg = Message(
                'Wallet Created Successfully',  # Subject
                recipients=[user_email],        # Add the recipient's email here
                sender='noreply@fotia.cloud'  # Set the sender email
            )
 
            # Add the email body content
            msg.body = f"Your new wallet address is: {address}\nYour private key is: {private_key}"
 
            # Send the email
            mail.send(msg)
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
 
        return jsonify({
            "message": "Wallet created successfully, and email sent to the user.",
            "address": address,
            "private_key": private_key
        }), 200
 
    except pymysql.MySQLError as db_err:
        logging.exception("Database error occurred")
        return jsonify({"error": f"Database error: {str(db_err)}"}), 500
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
 
 
if __name__ == '__main__':
    # Run Flask app with debugging enabled and avoid reloading issues
    app.run(debug=True, port=5004, use_reloader=False)

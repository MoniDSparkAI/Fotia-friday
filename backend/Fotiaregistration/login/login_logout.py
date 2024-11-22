# from flask import Flask, request, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_cors import CORS
# import MySQLdb
# import logging

# app = Flask(__name__)
# CORS(app)

# # Logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
# logger = logging.getLogger(__name__)
# handler = logging.FileHandler('app.log')
# handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
# logger.addHandler(handler)

# # MySQL configurations
# dcfg = {
#     "mysql": {
#         "host": "141.136.42.65",
#         "user": "root",
#         "password": "Test@2024",
#         "db": "fotia_database",
#         "port": 3306
#     }
# }

# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = MySQLdb.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             passwd=dcfg["mysql"]["password"],
#             db=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established")
#         return db_connection
#     except MySQLdb.Error as e:
#         logger.error(f"Database connection failed: {e}")
#         return None

# # Check if the database connection is working
# @app.route('/db-check', methods=['GET'])
# def db_check():
#     logger.info("Received request for database connection check")
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         logger.error("Database connection failed")
#         return jsonify({"message": "Database connection failed"}), 500

#     try:
#         cursor = db_connection.cursor()
#         cursor.execute("SELECT 1")
#         cursor.close()
#         logger.info("Database connection successful")
#         return jsonify({"message": "Database connection successful"}), 200
#     except MySQLdb.Error as e:
#         logger.error(f"Database query failed: {e}")
#         return jsonify({"message": "Database query failed"}), 500
#     finally:
#         db_connection.close()

# # Login a user and create or update a session
# @app.route('/login', methods=['POST'])
# def login():
#     logger.info("Received login request")
#     data = request.get_json()
#     identifier = data.get('identifier')  # Email or phone number
#     password = data.get('password')

#     if not identifier or not password:
#         logger.warning("Login failed: Missing identifier or password")
#         return jsonify({"message": "Missing identifier or password"}), 400

#     db_connection = mysqlconnect()
#     if db_connection is None:
#         logger.error("Database connection failed during login")
#         return jsonify({"message": "Database connection failed"}), 500

#     try:
#         cursor = db_connection.cursor()

#         # Check if the user exists by email or phone number
#         logger.info("Checking if user exists in database")
#         cursor.execute("SELECT id, email, username, password, phone_number, referral_code, is_first_login FROM users WHERE email = %s OR phone_number = %s", (identifier, identifier))
#         user = cursor.fetchone()

#         if user is None:
#             logger.warning("Login failed: User not found")
#             return jsonify({"message": "User not found"}), 404

#         # Check the password
#         if not check_password_hash(user[3], password):  # Assuming password is the 4th field
#             logger.warning("Login failed: Invalid password")
#             return jsonify({"message": "Invalid password"}), 401

#         # Check if it's the first login
#         is_first_login = user[6]  # Assuming `is_first_login` is the 7th field

#         if is_first_login:
#             # Update `is_first_login` to `False`
#             logger.info("Updating is_first_login flag for user")
#             cursor.execute("UPDATE users SET is_first_login = 0 WHERE id = %s", (user[0],))
#             db_connection.commit()

#         # Create or update a session for the user
#         logger.info("Creating or updating session for user")
#         cursor.execute("""
#             INSERT INTO user_sessions (user_id, login_time, logout_time) 
#             SELECT %s, NOW(), NULL
#             FROM DUAL
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM user_sessions WHERE user_id = %s AND logout_time IS NULL
#             )
#         """, (user[0], user[0]))
#         db_connection.commit()

#         logger.info(f"Login successful for user ID {user[0]}")
#         return jsonify({
#             "message": "Login successful",
#             "user": {
#                 "username": user[2],
#                 "email": user[1],
#                 "phone_number": user[4],
#                 "user_id": user[0],
#                 "referral_code": user[5],
#                 "is_first_login": is_first_login  # Return the first login status
#             }
#         }), 200

#     except MySQLdb.Error as e:
#         logger.error(f"Login failed: {e}")
#         return jsonify({"message": "Login failed"}), 500
#     finally:
#         db_connection.close()
        
# # Logout a user and update logout time
# @app.route('/logout', methods=['POST'])
# def logout():
#     logger.info("Received logout request")
#     data = request.get_json()
#     user_id = data.get('user_id')  # Ensure user_id is being passed in JSON request

#     if not user_id:
#         logger.warning("Logout failed: Missing user_id")
#         return jsonify({"message": "Missing user_id"}), 400

#     db_connection = mysqlconnect()
#     if db_connection is None:
#         logger.error("Database connection failed during logout")
#         return jsonify({"message": "Database connection failed"}), 500

#     try:
#         cursor = db_connection.cursor()

#         # Check if there's an active session (logout_time is NULL)
#         logger.info(f"Checking active session for user ID {user_id}")
#         cursor.execute("SELECT user_id FROM user_sessions WHERE user_id = %s AND logout_time IS NULL", (user_id,))
#         session = cursor.fetchone()

#         if session is None:
#             logger.warning("Logout failed: No active session found for user")
#             return jsonify({"message": "No active session found for the user"}), 404

#         # Update logout time
#         logger.info("Updating logout time for user")
#         cursor.execute("UPDATE user_sessions SET logout_time = NOW() WHERE user_id = %s AND logout_time IS NULL", (user_id,))
#         db_connection.commit()

#         logger.info(f"Logout successful for user ID {user_id}")
#         return jsonify({"message": "Logout successful"}), 200
#     except MySQLdb.Error as e:
#         logger.error(f"Logout failed: {e}")
#         return jsonify({"message": "Logout failed"}), 500
#     finally:
#         db_connection.close()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5002, debug=True)
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import MySQLdb
import logging
 
app = Flask(__name__)
CORS(app)
 
# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
 
# MySQL configurations
dcfg = {
    "mysql": {
        "host": "141.136.42.65",
        "user": "root",
        "password": "Test@2024",
        "db": "fotia_database",
        "port": 3306
    }
}
 
# Database connection function
def mysqlconnect():
    try:
        db_connection = MySQLdb.connect(
            host=dcfg["mysql"]["host"],
            user=dcfg["mysql"]["user"],
            passwd=dcfg["mysql"]["password"],
            db=dcfg["mysql"]["db"],
            port=dcfg["mysql"]["port"]
        )
        logger.info("Database connection established")
        return db_connection
    except MySQLdb.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None
 
# Check if the database connection is working
@app.route('/db-check', methods=['GET'])
def db_check():
    logger.info("Received request for database connection check")
    db_connection = mysqlconnect()
    if db_connection is None:
        logger.error("Database connection failed")
        return jsonify({"message": "Database connection failed"}), 500
 
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        logger.info("Database connection successful")
        return jsonify({"message": "Database connection successful"}), 200
    except MySQLdb.Error as e:
        logger.error(f"Database query failed: {e}")
        return jsonify({"message": "Database query failed"}), 500
    finally:
        db_connection.close()
 
# Login a user and create or update a session
@app.route('/login', methods=['POST'])
def login():
    logger.info("Received login request")
    data = request.get_json()
    identifier = data.get('identifier')  # Email or phone number
    password = data.get('password')
 
    if not identifier or not password:
        logger.warning("Login failed: Missing identifier or password")
        return jsonify({"message": "Missing identifier or password"}), 400
 
    db_connection = mysqlconnect()
    if db_connection is None:
        logger.error("Database connection failed during login")
        return jsonify({"message": "Database connection failed"}), 500
 
    try:
        cursor = db_connection.cursor()
 
        # Check if the user exists by email or phone number
        logger.info("Checking if user exists in database")
        cursor.execute("SELECT id, email, username, password, phone_number, referral_code, is_first_login, wallet_created, payment_completed FROM users WHERE email = %s OR phone_number = %s", (identifier, identifier))
        user = cursor.fetchone()
 
        if user is None:
            logger.warning("Login failed: User not found")
            return jsonify({"message": "User not found"}), 404
 
        # Check the password
        if not check_password_hash(user[3], password):  # Assuming password is the 4th field
            logger.warning("Login failed: Invalid password")
            return jsonify({"message": "Invalid password"}), 401
 
        # Check if it's the first login
        is_first_login = user[6]  # Assuming `is_first_login` is the 7th field
        wallet_created = user[7]  # Assuming `wallet_created` is the 8th field
        payment_completed = user[8]  # Assuming `payment_completed` is the 9th field
 
        if is_first_login:
            # Update `is_first_login` to `False`
            logger.info("Updating is_first_login flag for user")
            cursor.execute("UPDATE users SET is_first_login = 0 WHERE id = %s", (user[0],))
            db_connection.commit()
 
        # Create or update a session for the user
        logger.info("Creating or updating session for user")
        cursor.execute("""
            INSERT INTO user_sessions (user_id, login_time, logout_time)
            SELECT %s, NOW(), NULL
            FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1 FROM user_sessions WHERE user_id = %s AND logout_time IS NULL
            )
        """, (user[0], user[0]))
        db_connection.commit()
 
        logger.info(f"Login successful for user ID {user[0]}")
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user[2],
                "email": user[1],
                "phone_number": user[4],
                "user_id": user[0],
                "referral_code": user[5],
                "is_first_login": is_first_login,
                "wallet_created": wallet_created,
                "payment_completed": payment_completed  # Include these flags in the response
            }
        }), 200
 
    except MySQLdb.Error as e:
        logger.error(f"Login failed: {e}")
        return jsonify({"message": "Login failed"}), 500
    finally:
        db_connection.close()
 
       
# Logout a user and update logout time
@app.route('/logout', methods=['POST'])
def logout():
    logger.info("Received logout request")
    data = request.get_json()
    user_id = data.get('user_id')  # Ensure user_id is being passed in JSON request
 
    if not user_id:
        logger.warning("Logout failed: Missing user_id")
        return jsonify({"message": "Missing user_id"}), 400
 
    db_connection = mysqlconnect()
    if db_connection is None:
        logger.error("Database connection failed during logout")
        return jsonify({"message": "Database connection failed"}), 500
 
    try:
        cursor = db_connection.cursor()
 
        # Check if there's an active session (logout_time is NULL)
        logger.info(f"Checking active session for user ID {user_id}")
        cursor.execute("SELECT user_id FROM user_sessions WHERE user_id = %s AND logout_time IS NULL", (user_id,))
        session = cursor.fetchone()
 
        if session is None:
            logger.warning("Logout failed: No active session found for user")
            return jsonify({"message": "No active session found for the user"}), 404
 
        # Update logout time
        logger.info("Updating logout time for user")
        cursor.execute("UPDATE user_sessions SET logout_time = NOW() WHERE user_id = %s AND logout_time IS NULL", (user_id,))
        db_connection.commit()
 
        logger.info(f"Logout successful for user ID {user_id}")
        return jsonify({"message": "Logout successful"}), 200
    except MySQLdb.Error as e:
        logger.error(f"Logout failed: {e}")
        return jsonify({"message": "Logout failed"}), 500
    finally:
        db_connection.close()
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
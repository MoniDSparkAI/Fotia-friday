# import logging
# from flask import Flask, request, jsonify, url_for, redirect
# from werkzeug.security import generate_password_hash
# from flask_cors import CORS
# from flask_mail import Mail, Message
# import mysql.connector
# from itsdangerous import URLSafeTimedSerializer
# import random
# import string
# import phonenumbers

# # Flask App Setup
# app = Flask(__name__)
# CORS(app)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

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

# # Email configurations
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

# mail = Mail(app)

# # Token serializer for email verification
# serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])

# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = mysql.connector.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             password=dcfg["mysql"]["password"],
#             database=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established successfully.")
#         return db_connection
#     except mysql.connector.Error as e:
#         logger.error("Database connection failed: %s", e)
#         return None

# # Generate a referral code
# def generate_referral_code():
#     referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     logger.debug("Generated referral code: %s", referral_code)
#     return referral_code

# # Check if phone number is valid
# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)  # Parse phone number
#         is_valid = phonenumbers.is_valid_number(parsed_number)  # Check if valid
#         logger.debug("Phone number %s valid: %s", phone_number, is_valid)
#         return is_valid
#     except phonenumbers.phonenumberutil.NumberParseException:
#         logger.warning("Invalid phone number format: %s", phone_number)
#         return False

# # Generate a token for email verification
# def generate_verification_token(email):
#     token = serializer.dumps(email, salt='email-verify')
#     logger.debug("Generated email verification token for email: %s", email)
#     return token

# # Verify the token
# def confirm_verification_token(token, expiration=3600):
#     try:
#         email = serializer.loads(token, salt='email-verify', max_age=expiration)
#         logger.debug("Email verification token confirmed for email: %s", email)
#         return email
#     except:
#         logger.warning("Invalid or expired token")
#         return False

# # Send verification email with enhanced styles
# def send_verification_email(email, token):
#     verify_url = url_for('verify_email', token=token, _external=True)
#     msg = Message('Verify Your Email',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .button {{
#                 display: inline-block;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 padding: 10px 20px;
#                 border-radius: 5px;
#                 font-size: 16px;
#                 margin-top: 20px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Thank you for registering!</h1>
#             <p>Click the link below to verify your email address:</p>
#             <a href="{verify_url}" class="button">Verify Email</a>
#             <div class="footer">
#                 <p>If you did not register for an account, please ignore this email.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Verification email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send verification email to %s: %s", email, e)

# # Send registration success email with referral code and more styling
# def send_success_email(email, referral_code=None):
#     msg = Message('Registration Successful',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .referral-code {{
#                 font-size: 18px;
#                 color: #555;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Registration Successful!</h1>
#             <p>Your account is now verified.</p>
#             {f'<p class="referral-code">Your referral code is: {referral_code}</p>' if referral_code else ""}
#             <div class="footer">
#                 <p>Thank you for choosing Fotia.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Registration success email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send registration success email to %s: %s", email, e)


# # Register a new user
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     phone_number = data.get('phone_number')
#     referral_code = data.get('referral_code')

#     logger.info("Registration request received for email: %s", email)

#     if not email or not username or not password or not phone_number:
#         logger.warning("Missing required fields.")
#         return jsonify({"message": "Missing required fields"}), 400

#     if not is_valid_phone_number(phone_number):
#         logger.warning("Invalid phone number format.")
#         return jsonify({"message": "Invalid phone number format"}), 400

#     hashed_password = generate_password_hash(password)
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500

#     try:
#         cursor = db_connection.cursor()
#         cursor.execute("SELECT * FROM users WHERE email = %s OR phone_number = %s", (email, phone_number))
#         user = cursor.fetchone()

#         if user:
#             return jsonify({"message": "Email or phone number already exists"}), 400

#         referred_by = None
#         if referral_code:
#             cursor.execute("SELECT * FROM users WHERE referral_code = %s", (referral_code,))
#             referrer = cursor.fetchone()
#             if referrer:
#                 referred_by = referral_code
#             else:
#                 return jsonify({"message": "Invalid referral code"}), 400

#         user_referral_code = generate_referral_code()
#         cursor.execute(
#             "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (email, username, hashed_password, phone_number, user_referral_code, referred_by, 'unverified')
#         )
#         db_connection.commit()
#         token = generate_verification_token(email)
#         send_verification_email(email, token)
#         return jsonify({"message": "Please verify your email"}), 201
#     finally:
#         db_connection.close()

# # Verify the user's email
# @app.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     email = confirm_verification_token(token)
#     if not email:
#         return jsonify({"message": "Invalid or expired token"}), 400

#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500

#     try:
#         cursor = db_connection.cursor()
#         cursor.execute("UPDATE users SET status = %s WHERE email = %s", ('verified', email))
#         db_connection.commit()
#         send_success_email(email)
#         return redirect("http://localhost:5173/Login")
#     finally:
#         db_connection.close()

# if __name__ == '__main__':
#     app.run(debug=True, port=5001, host="0.0.0.0")
# import logging
# from flask import Flask, request, jsonify, url_for, redirect
# from werkzeug.security import generate_password_hash
# from flask_cors import CORS
# from flask_mail import Mail, Message
# import mysql.connector
# from itsdangerous import URLSafeTimedSerializer
# import random
# import string
# import phonenumbers
 
# # Flask App Setup
# app = Flask(__name__)
# CORS(app)
 
# # Set up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
 
# # MySQL configurations
# dcfg = {
#     "mysql": {
#         "host": "localhost",
#         "user": "root",
#         "password": "D@qwertyuiop",
#         "db": "fotia_database",
#         "port": 3307
#     }
# }
 
# # Email configurations
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
 
# mail = Mail(app)
 
# # Token serializer for email verification
# serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])
 
# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = mysql.connector.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             password=dcfg["mysql"]["password"],
#             database=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established successfully.")
#         return db_connection
#     except mysql.connector.Error as e:
#         logger.error("Database connection failed: %s", e)
#         return None
 
# # Generate a referral code
# def generate_referral_code():
#     referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     logger.debug("Generated referral code: %s", referral_code)
#     return referral_code
 
# # Check if phone number is valid
# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         is_valid = phonenumbers.is_valid_number(parsed_number)
#         logger.debug("Phone number %s valid: %s", phone_number, is_valid)
#         return is_valid
#     except phonenumbers.phonenumberutil.NumberParseException:
#         logger.warning("Invalid phone number format: %s", phone_number)
#         return False
 
# # Generate a token for email verification
# def generate_verification_token(email):
#     token = serializer.dumps(email, salt='email-verify')
#     logger.debug("Generated email verification token for email: %s", email)
#     return token
 
# # Verify the token
# def confirm_verification_token(token, expiration=3600):
#     try:
#         email = serializer.loads(token, salt='email-verify', max_age=expiration)
#         logger.debug("Email verification token confirmed for email: %s", email)
#         return email
#     except:
#         logger.warning("Invalid or expired token")
#         return False
 
# # Send verification email
# def send_verification_email(email, token):
#     verify_url = url_for('verify_email', token=token, _external=True)
#     msg = Message('Verify Your Email',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#         <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .button {{
#                 display: inline-block;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 padding: 10px 20px;
#                 border-radius: 5px;
#                 font-size: 16px;
#                 margin-top: 20px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Thank you for registering!</h1>
#             <p>Click the link below to verify your email address:</p>
#             <a href="{verify_url}" class="button">Verify Email</a>
#             <div class="footer">
#                 <p>If you did not register for an account, please ignore this email.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Verification email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send verification email to %s: %s", email, e)
 
 
# def send_success_email(email):
#     msg = Message('Account Successfully Verified',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = """
#        <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .referral-code {{
#                 font-size: 18px;
#                 color: #555;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Registration Successful!</h1>
#             <p>Your account is now verified.</p>
#             <div class="footer">
#                 <p>Thank you for choosing Fotia.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Success email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send success email to %s: %s", email, e)
 
 
# # Store user data temporarily in a list
# temp_user_data = []
 
# # Register a new user
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     phone_number = data.get('phone_number')
#     referral_code = data.get('referral_code')
 
#     logger.info("Registration request received for email: %s", email)
 
#     if not email or not username or not password or not phone_number:
#         logger.warning("Missing required fields.")
#         return jsonify({"message": "Missing required fields"}), 400
 
#     if not is_valid_phone_number(phone_number):
#         logger.warning("Invalid phone number format.")
#         return jsonify({"message": "Invalid phone number format"}), 400
 
#     hashed_password = generate_password_hash(password)
 
#     # Save user data in the temporary list
#     user_referral_code = generate_referral_code()
#     temp_user_data.append({
#         "email": email,
#         "username": username,
#         "password": hashed_password,
#         "phone_number": phone_number,
#         "referral_code": user_referral_code,
#         "referred_by": referral_code
#     })
 
#     token = generate_verification_token(email)
#     send_verification_email(email, token)
#     return jsonify({"message": "Please verify your email"}), 201
 
# # Verify the user's email
# @app.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     email = confirm_verification_token(token)
#     if not email:
#         return jsonify({"message": "Invalid or expired token"}), 400
 
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500
 
#     try:
#         # Find the user in the temporary list
#         user_data = next((user for user in temp_user_data if user['email'] == email), None)
#         if not user_data:
#             return jsonify({"message": "User not found"}), 404
 
#         cursor = db_connection.cursor()
#         referred_by = None
#         if user_data['referred_by']:
#             cursor.execute("SELECT * FROM users WHERE referral_code = %s", (user_data['referred_by'],))
#             if cursor.fetchone():
#                 referred_by = user_data['referred_by']
 
#         # Insert user data into the database
#         cursor.execute(
#             "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (user_data['email'], user_data['username'], user_data['password'], user_data['phone_number'],
#              user_data['referral_code'], referred_by, 'verified')
#         )
#         db_connection.commit()
 
#         # Remove the user from the temporary list
#         temp_user_data.remove(user_data)
 
#         send_success_email(email)
 
#         return redirect("https://fotia.ai/Login")
#     finally:
#         db_connection.close()
 
# if __name__ == '__main__':
#     app.run(debug=True, port=5001, host="0.0.0.0")
 
# import logging
# from flask import Flask, request, jsonify, url_for, redirect
# from werkzeug.security import generate_password_hash
# from flask_cors import CORS
# from flask_mail import Mail, Message
# import mysql.connector
# from itsdangerous import URLSafeTimedSerializer
# import random
# import string
# import phonenumbers
 
# # Flask App Setup
# app = Flask(__name__)
# CORS(app)
 
# # Set up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
 
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
 
# # Email configurations
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
 
# mail = Mail(app)
 
# # Token serializer for email verification
# serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])
 
# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = mysql.connector.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             password=dcfg["mysql"]["password"],
#             database=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established successfully.")
#         return db_connection
#     except mysql.connector.Error as e:
#         logger.error("Database connection failed: %s", e)
#         return None
 
# # Generate a referral code
# def generate_referral_code():
#     referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     logger.debug("Generated referral code: %s", referral_code)
#     return referral_code
 
# # Check if phone number is valid
# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         is_valid = phonenumbers.is_valid_number(parsed_number)
#         logger.debug("Phone number %s valid: %s", phone_number, is_valid)
#         return is_valid
#     except phonenumbers.phonenumberutil.NumberParseException:
#         logger.warning("Invalid phone number format: %s", phone_number)
#         return False
 
# # Generate a token for email verification
# def generate_verification_token(email):
#     token = serializer.dumps(email, salt='email-verify')
#     logger.debug("Generated email verification token for email: %s", email)
#     return token
 
# # Verify the token
# def confirm_verification_token(token, expiration=3600):
#     try:
#         email = serializer.loads(token, salt='email-verify', max_age=expiration)
#         logger.debug("Email verification token confirmed for email: %s", email)
#         return email
#     except:
#         logger.warning("Invalid or expired token")
#         return False
 
# # Send verification email
# def send_verification_email(email, token):
#     verify_url = url_for('verify_email', token=token, _external=True)
#     msg = Message('Verify Your Email',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#         <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .button {{
#                 display: inline-block;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 padding: 10px 20px;
#                 border-radius: 5px;
#                 font-size: 16px;
#                 margin-top: 20px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Thank you for registering!</h1>
#             <p>Click the link below to verify your email address:</p>
#             <a href="{verify_url}" class="button">Verify Email</a>
#             <div class="footer">
#                 <p>If you did not register for an account, please ignore this email.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Verification email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send verification email to %s: %s", email, e)
 
 
# def send_success_email(email):
#     msg = Message('Account Successfully Verified',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = """
#        <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .referral-code {{
#                 font-size: 18px;
#                 color: #555;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Registration Successful!</h1>
#             <p>Your account is now verified.</p>
#             <div class="footer">
#                 <p>Thank you for choosing Fotia.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Success email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send success email to %s: %s", email, e)
 
 
# # Store user data temporarily in a list
# temp_user_data = []
 
# # Register a new user
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     phone_number = data.get('phone_number')
#     referral_code = data.get('referral_code')
 
#     logger.info("Registration request received for email: %s", email)
 
#     if not email or not username or not password or not phone_number:
#         logger.warning("Missing required fields.")
#         return jsonify({"message": "Missing required fields"}), 400
 
#     if not is_valid_phone_number(phone_number):
#         logger.warning("Invalid phone number format.")
#         return jsonify({"message": "Invalid phone number format"}), 400
 
#     hashed_password = generate_password_hash(password)
 
#     # Save user data in the temporary list
#     user_referral_code = generate_referral_code()
#     temp_user_data.append({
#         "email": email,
#         "username": username,
#         "password": hashed_password,
#         "phone_number": phone_number,
#         "referral_code": user_referral_code,
#         "referred_by": referral_code
#     })
 
#     token = generate_verification_token(email)
#     send_verification_email(email, token)
#     return jsonify({"message": "Please verify your email"}), 201
 
# @app.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     email = confirm_verification_token(token)
#     if not email:
#         return jsonify({"message": "Invalid or expired token"}), 400
 
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500
 
#     try:
#         # Find the user in the temporary list
#         user_data = next((user for user in temp_user_data if user['email'] == email), None)
#         if not user_data:
#             return jsonify({"message": "User not found"}), 404
 
#         cursor = db_connection.cursor(dictionary=True)
#         referred_by = None
 
#         # Check if referred_by referral code is valid and not expired
#         if user_data['referred_by']:
#             cursor.execute("SELECT * FROM users WHERE referral_code = %s", (user_data['referred_by'],))
#             referrer = cursor.fetchone()
#             if referrer:
#                 if referrer['referral_expired']:
#                     return jsonify({"message": "Referral code expired"}), 400
               
#                 if referrer['referral_count'] >= 25:
#                     # Expire the referral code
#                     cursor.execute("UPDATE users SET referral_expired = TRUE WHERE referral_code = %s", (user_data['referred_by'],))
#                     db_connection.commit()
#                 else:
#                     referred_by = user_data['referred_by']
#                     # Increment referral count
#                     cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE referral_code = %s", (referred_by,))
#                     db_connection.commit()
 
#         # Insert user data into the database
#         cursor.execute(
#             "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (user_data['email'], user_data['username'], user_data['password'], user_data['phone_number'],
#              user_data['referral_code'], referred_by, 'verified')
#         )
#         db_connection.commit()
 
#         # Remove the user from the temporary list
#         temp_user_data.remove(user_data)
 
#         send_success_email(email)
 
#         return redirect("http://localhost:5173/Login")
#     finally:
#         db_connection.close()
 
# if __name__ == '__main__':
#     app.run(debug=True, port=5001, host="0.0.0.0")
# import logging
# from flask import Flask, request, jsonify, url_for, redirect
# from werkzeug.security import generate_password_hash
# from flask_cors import CORS
# from flask_mail import Mail, Message
# import mysql.connector
# from itsdangerous import URLSafeTimedSerializer
# import random
# import string
# import phonenumbers
 
# # Flask App Setup
# app = Flask(__name__)
# CORS(app)
 
# # Set up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
 
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
 
# # Email configurations
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
 
# mail = Mail(app)
 
# # Token serializer for email verification
# serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])
 
# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = mysql.connector.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             password=dcfg["mysql"]["password"],
#             database=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established successfully.")
#         return db_connection
#     except mysql.connector.Error as e:
#         logger.error("Database connection failed: %s", e)
#         return None
 
# # Generate a referral code
# def generate_referral_code():
#     referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     logger.debug("Generated referral code: %s", referral_code)
#     return referral_code
 
# # Check if phone number is valid
# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         is_valid = phonenumbers.is_valid_number(parsed_number)
#         logger.debug("Phone number %s valid: %s", phone_number, is_valid)
#         return is_valid
#     except phonenumbers.phonenumberutil.NumberParseException:
#         logger.warning("Invalid phone number format: %s", phone_number)
#         return False
 
# # Generate a token for email verification
# def generate_verification_token(email):
#     token = serializer.dumps(email, salt='email-verify')
#     logger.debug("Generated email verification token for email: %s", email)
#     return token
 
# # Verify the token
# def confirm_verification_token(token, expiration=3600):
#     try:
#         email = serializer.loads(token, salt='email-verify', max_age=expiration)
#         logger.debug("Email verification token confirmed for email: %s", email)
#         return email
#     except:
#         logger.warning("Invalid or expired token")
#         return False
 
# # Send verification email
# def send_verification_email(email, token):
#     verify_url = url_for('verify_email', token=token, _external=True)
#     msg = Message('Verify Your Email',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#         <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .button {{
#                 display: inline-block;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 padding: 10px 20px;
#                 border-radius: 5px;
#                 font-size: 16px;
#                 margin-top: 20px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Thank you for registering!</h1>
#             <p>Click the link below to verify your email address:</p>
#             <a href="{verify_url}" class="button">Verify Email</a>
#             <div class="footer">
#                 <p>If you did not register for an account, please ignore this email.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Verification email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send verification email to %s: %s", email, e)
 
 
# def send_success_email(email):
#     msg = Message('Account Successfully Verified',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = """
#        <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .referral-code {{
#                 font-size: 18px;
#                 color: #555;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Registration Successful!</h1>
#             <p>Your account is now verified.</p>
#             <div class="footer">
#                 <p>Thank you for choosing Fotia.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Success email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send success email to %s: %s", email, e)
 
 
# # Store user data temporarily in a list
# temp_user_data = []
 
# # Register a new user
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     phone_number = data.get('phone_number')
#     referral_code = data.get('referral_code')
 
#     logger.info("Registration request received for email: %s", email)
 
#     if not email or not username or not password or not phone_number:
#         logger.warning("Missing required fields.")
#         return jsonify({"message": "Missing required fields"}), 400
 
#     if not is_valid_phone_number(phone_number):
#         logger.warning("Invalid phone number format.")
#         return jsonify({"message": "Invalid phone number format"}), 400
 
#     hashed_password = generate_password_hash(password)
 
#     # Save user data in the temporary list
#     user_referral_code = generate_referral_code()
#     temp_user_data.append({
#         "email": email,
#         "username": username,
#         "password": hashed_password,
#         "phone_number": phone_number,
#         "referral_code": user_referral_code,
#         "referred_by": referral_code
#     })
 
#     token = generate_verification_token(email)
#     send_verification_email(email, token)
#     return jsonify({"message": "Please verify your email"}), 201
 
# @app.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     email = confirm_verification_token(token)
#     if not email:
#         return jsonify({"message": "Invalid or expired token"}), 400
 
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500
 
#     try:
#         # Find the user in the temporary list
#         user_data = next((user for user in temp_user_data if user['email'] == email), None)
#         if not user_data:
#             return jsonify({"message": "User not found"}), 404
 
#         cursor = db_connection.cursor(dictionary=True)
#         referred_by = None
 
#         # Check if referred_by referral code is valid and not expired
#         if user_data['referred_by']:
#             cursor.execute("SELECT * FROM users WHERE referral_code = %s", (user_data['referred_by'],))
#             referrer = cursor.fetchone()
#             if referrer:
#                 if referrer['referral_expired']:
#                     return jsonify({"message": "Referral code expired"}), 400
               
#                 if referrer['referral_count'] >= 24:
#                     # Expire the referral code
#                     cursor.execute("UPDATE users SET referral_expired = TRUE WHERE referral_code = %s", (user_data['referred_by'],))
#                     db_connection.commit()
#                 else:
#                     referred_by = user_data['referred_by']
#                     # Increment referral count
#                     cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE referral_code = %s", (referred_by,))
#                     db_connection.commit()
 
#         # Insert user data into the database
#         cursor.execute(
#             "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (user_data['email'], user_data['username'], user_data['password'], user_data['phone_number'],
#              user_data['referral_code'], referred_by, 'verified')
#         )
#         db_connection.commit()
 
#         # Remove the user from the temporary list
#         temp_user_data.remove(user_data)
 
#         send_success_email(email)
 
#         return redirect("http://localhost:5173/Login")
#     finally:
#         db_connection.close()
 
# if __name__ == '__main__':
#     app.run(debug=True, port=5001, host="0.0.0.0")
# import logging
# from flask import Flask, request, jsonify, url_for, redirect
# from werkzeug.security import generate_password_hash
# from flask_cors import CORS
# from flask_mail import Mail, Message
# import mysql.connector
# from itsdangerous import URLSafeTimedSerializer
# import random
# import string
# import phonenumbers
 
# # Flask App Setup
# app = Flask(__name__)
# CORS(app)
 
# # Set up logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
 
# # MySQL configurations
# dcfg = {
#     "mysql": {
#         "host": "141.136.42.65",
#         "user": "root",
#         "password": "Test@2024",
#         "db": "fotia_database",
#         "port": 3307
#     }
# }
 
# # Email configurations
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'noreply@fotia.cloud'
# app.config['MAIL_PASSWORD'] = 'Fotia@2024'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
 
# mail = Mail(app)
 
# # Token serializer for email verification
# serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])
 
# # Database connection function
# def mysqlconnect():
#     try:
#         db_connection = mysql.connector.connect(
#             host=dcfg["mysql"]["host"],
#             user=dcfg["mysql"]["user"],
#             password=dcfg["mysql"]["password"],
#             database=dcfg["mysql"]["db"],
#             port=dcfg["mysql"]["port"]
#         )
#         logger.info("Database connection established successfully.")
#         return db_connection
#     except mysql.connector.Error as e:
#         logger.error("Database connection failed: %s", e)
#         return None
 
# # Generate a referral code
# def generate_referral_code():
#     referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#     logger.debug("Generated referral code: %s", referral_code)
#     return referral_code
 
# # Check if phone number is valid
# def is_valid_phone_number(phone_number):
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         is_valid = phonenumbers.is_valid_number(parsed_number)
#         logger.debug("Phone number %s valid: %s", phone_number, is_valid)
#         return is_valid
#     except phonenumbers.phonenumberutil.NumberParseException:
#         logger.warning("Invalid phone number format: %s", phone_number)
#         return False
 
# # Generate a token for email verification
# def generate_verification_token(email):
#     token = serializer.dumps(email, salt='email-verify')
#     logger.debug("Generated email verification token for email: %s", email)
#     return token
 
# # Verify the token
# def confirm_verification_token(token, expiration=3600):
#     try:
#         email = serializer.loads(token, salt='email-verify', max_age=expiration)
#         logger.debug("Email verification token confirmed for email: %s", email)
#         return email
#     except:
#         logger.warning("Invalid or expired token")
#         return False
 
# # Send verification email
# def send_verification_email(email, token):
#     verify_url = url_for('verify_email', token=token, _external=True)
#     msg = Message('Verify Your Email',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = f"""
#         <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .button {{
#                 display: inline-block;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 padding: 10px 20px;
#                 border-radius: 5px;
#                 font-size: 16px;
#                 margin-top: 20px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Thank you for registering!</h1>
#             <p>Click the link below to verify your email address:</p>
#             <a href="{verify_url}" class="button">Verify Email</a>
#             <div class="footer">
#                 <p>If you did not register for an account, please ignore this email.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Verification email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send verification email to %s: %s", email, e)
 
 
# def send_success_email(email):
#     msg = Message('Account Successfully Verified',
#                   sender='noreply@fotia.cloud',
#                   recipients=[email])
#     msg.html = """
#        <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 color: #333;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .container {{
#                 width: 100%;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#                 background-color: #ffffff;
#                 border-radius: 8px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             }}
#             h1 {{
#                 color: #4CAF50;
#                 font-size: 24px;
#                 margin-bottom: 10px;
#             }}
#             p {{
#                 font-size: 16px;
#                 line-height: 1.5;
#             }}
#             .referral-code {{
#                 font-size: 18px;
#                 color: #555;
#                 font-weight: bold;
#                 margin-top: 10px;
#             }}
#             .footer {{
#                 font-size: 12px;
#                 color: #999;
#                 text-align: center;
#                 margin-top: 30px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Registration Successful!</h1>
#             <p>Your account is now verified.</p>
#             <div class="footer">
#                 <p>Thank you for choosing Fotia.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     try:
#         mail.send(msg)
#         logger.info("Success email sent to: %s", email)
#     except Exception as e:
#         logger.error("Failed to send success email to %s: %s", email, e)
 
 
# # Store user data temporarily in a list
# temp_user_data = []
 
# # Register a new user
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     phone_number = data.get('phone_number')
#     referral_code = data.get('referral_code')
 
#     logger.info("Registration request received for email: %s", email)
 
#     if not email or not username or not password or not phone_number:
#         logger.warning("Missing required fields.")
#         return jsonify({"message": "Missing required fields"}), 400
 
#     if not is_valid_phone_number(phone_number):
#         logger.warning("Invalid phone number format.")
#         return jsonify({"message": "Invalid phone number format"}), 400
 
#     hashed_password = generate_password_hash(password)
 
#     # Save user data in the temporary list
#     user_referral_code = generate_referral_code()
#     temp_user_data.append({
#         "email": email,
#         "username": username,
#         "password": hashed_password,
#         "phone_number": phone_number,
#         "referral_code": user_referral_code,
#         "referred_by": referral_code
#     })
 
#     token = generate_verification_token(email)
#     send_verification_email(email, token)
#     return jsonify({"message": "Please verify your email"}), 201
 
# @app.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     email = confirm_verification_token(token)
#     if not email:
#         return jsonify({"message": "Invalid or expired token"}), 400
 
#     db_connection = mysqlconnect()
#     if db_connection is None:
#         return jsonify({"message": "Database connection failed"}), 500
 
#     try:
#         # Find the user in the temporary list
#         user_data = next((user for user in temp_user_data if user['email'] == email), None)
#         if not user_data:
#             return jsonify({"message": "User not found"}), 404
 
#         cursor = db_connection.cursor(dictionary=True)
#         referred_by = None
 
#         # Check if referred_by referral code is valid and not expired
#         if user_data['referred_by']:
#             cursor.execute("SELECT * FROM users WHERE referral_code = %s", (user_data['referred_by'],))
#             referrer = cursor.fetchone()
#             if referrer:
#                 if referrer['referral_expired']:
#                     return jsonify({"message": "Referral code expired"}), 400
               
#                 if referrer['referral_count'] >= 24:
#                     # Expire the referral code
#                     cursor.execute("UPDATE users SET referral_expired = TRUE WHERE referral_code = %s", (user_data['referred_by'],))
#                     db_connection.commit()
#                 else:
#                     referred_by = user_data['referred_by']
#                     # Increment referral count
#                     cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE referral_code = %s", (referred_by,))
#                     db_connection.commit()
 
#         # Insert user data into the database
#         cursor.execute(
#             "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (user_data['email'], user_data['username'], user_data['password'], user_data['phone_number'],
#              user_data['referral_code'], referred_by, 'verified')
#         )
#         db_connection.commit()
 
#         # Remove the user from the temporary list
#         temp_user_data.remove(user_data)
 
#         send_success_email(email)
 
#         return redirect("http://localhost:5173/Login")
#     finally:
#         db_connection.close()
 
# if __name__ == '__main__':
#     app.run(debug=True, port=5001, host="0.0.0.0")
import logging
from flask import Flask, request, jsonify, url_for, redirect
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_mail import Mail, Message
import mysql.connector
from itsdangerous import URLSafeTimedSerializer
import random
import string
import phonenumbers
 
# Flask App Setup
app = Flask(__name__)
CORS(app)
 
# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
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
 
# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'datasparkaisolutions@gmail.com'
app.config['MAIL_PASSWORD'] = 'mrgnqanvdwzlkcae'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
 
mail = Mail(app)
 
# Token serializer for email verification
serializer = URLSafeTimedSerializer(app.config['MAIL_PASSWORD'])
 
# Database connection function
def mysqlconnect():
    try:
        db_connection = mysql.connector.connect(
            host=dcfg["mysql"]["host"],
            user=dcfg["mysql"]["user"],
            password=dcfg["mysql"]["password"],
            database=dcfg["mysql"]["db"],
            port=dcfg["mysql"]["port"]
        )
        logger.info("Database connection established successfully.")
        return db_connection
    except mysql.connector.Error as e:
        logger.error("Database connection failed: %s", e)
        return None
 
# Generate a referral code
def generate_referral_code():
    referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    logger.debug("Generated referral code: %s", referral_code)
    return referral_code
 
# Check if phone number is valid
def is_valid_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        logger.debug("Phone number %s valid: %s", phone_number, is_valid)
        return is_valid
    except phonenumbers.phonenumberutil.NumberParseException:
        logger.warning("Invalid phone number format: %s", phone_number)
        return False
 
# Generate a token for email verification
def generate_verification_token(email):
    token = serializer.dumps(email, salt='email-verify')
    logger.debug("Generated email verification token for email: %s", email)
    return token
 
# Verify the token
def confirm_verification_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='email-verify', max_age=expiration)
        logger.debug("Email verification token confirmed for email: %s", email)
        return email
    except:
        logger.warning("Invalid or expired token")
        return False
 
# Send verification email
def send_verification_email(email, token):
    verify_url = url_for('verify_email', token=token, _external=True)
    msg = Message('Verify Your Email',
                  sender='noreply@fotia.cloud',
                  recipients=[email])
    msg.html = f"""
        <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #4CAF50;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 16px;
                line-height: 1.5;
            }}
            .button {{
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: #999;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Thank you for registering!</h1>
            <p>Click the link below to verify your email address:</p>
            <a href="{verify_url}" class="button">Verify Email</a>
            <div class="footer">
                <p>If you did not register for an account, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    try:
        mail.send(msg)
        logger.info("Verification email sent to: %s", email)
    except Exception as e:
        logger.error("Failed to send verification email to %s: %s", email, e)
 
 
def send_success_email(email):
    msg = Message('Account Successfully Verified',
                  sender='noreply@fotia.cloud',
                  recipients=[email])
    msg.html = """
       <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #4CAF50;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            p {{
                font-size: 16px;
                line-height: 1.5;
            }}
            .referral-code {{
                font-size: 18px;
                color: #555;
                font-weight: bold;
                margin-top: 10px;
            }}
            .footer {{
                font-size: 12px;
                color: #999;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Registration Successful!</h1>
            <p>Your account is now verified.</p>
            <div class="footer">
                <p>Thank you for choosing Fotia.</p>
            </div>
        </div>
    </body>
    </html>
    """
    try:
        mail.send(msg)
        logger.info("Success email sent to: %s", email)
    except Exception as e:
        logger.error("Failed to send success email to %s: %s", email, e)
 
 
# Store user data temporarily in a list
temp_user_data = []
 
# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    phone_number = data.get('phone_number')
    referral_code = data.get('referral_code')
 
    logger.info("Registration request received for email: %s", email)
 
    if not email or not username or not password or not phone_number:
        logger.warning("Missing required fields.")
        return jsonify({"message": "Missing required fields"}), 400
 
    if not is_valid_phone_number(phone_number):
        logger.warning("Invalid phone number format.")
        return jsonify({"message": "Invalid phone number format"}), 400
 
    hashed_password = generate_password_hash(password)
 
    # Save user data in the temporary list
    user_referral_code = generate_referral_code()
    temp_user_data.append({
        "email": email,
        "username": username,
        "password": hashed_password,
        "phone_number": phone_number,
        "referral_code": user_referral_code,
        "referred_by": referral_code
    })
 
    token = generate_verification_token(email)
    send_verification_email(email, token)
    return jsonify({"message": "Please verify your email"}), 201
 
@app.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        return jsonify({"message": "Invalid or expired token"}), 400
 
    db_connection = mysqlconnect()
    if db_connection is None:
        return jsonify({"message": "Database connection failed"}), 500
 
    try:
        # Find the user in the temporary list
        user_data = next((user for user in temp_user_data if user['email'] == email), None)
        if not user_data:
            return jsonify({"message": "User not found"}), 404
 
        cursor = db_connection.cursor(dictionary=True)
        referred_by = None
 
        # Check if referred_by referral code is valid and not expired
        if user_data['referred_by']:
            cursor.execute("SELECT * FROM users WHERE referral_code = %s", (user_data['referred_by'],))
            referrer = cursor.fetchone()
            if referrer:
                if referrer['referral_expired']:
                    return jsonify({"message": "Referral code expired"}), 400
               
                if referrer['direct_referal_count'] >= 25:
                    # Expire the referral code
                    cursor.execute("UPDATE users SET referral_expired = TRUE WHERE referral_code = %s", (user_data['referred_by'],))
                    db_connection.commit()
                else:
                    referred_by = user_data['referred_by']
                    # Increment referral count
                    cursor.execute("UPDATE users SET direct_referal_count = direct_referal_count + 1 WHERE referral_code = %s", (referred_by,))
                    db_connection.commit()
 
        # Insert user data into the database
        cursor.execute(
            "INSERT INTO users (email, username, password, phone_number, referral_code, referred_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_data['email'], user_data['username'], user_data['password'], user_data['phone_number'],
             user_data['referral_code'], referred_by, 'verified')
        )
        db_connection.commit()
 
        # Remove the user from the temporary list
        temp_user_data.remove(user_data)
 
        send_success_email(email)
 
        return redirect("http://localhost:5173/Login")
    finally:
        db_connection.close()
 
if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
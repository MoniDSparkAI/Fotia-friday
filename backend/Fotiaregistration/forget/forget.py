import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import MySQLdb
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
CORS(app)

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

otp_store = {}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection function
def mysqlconnect():
    try:
        logging.info("Attempting to connect to MySQL database.")
        db_connection = MySQLdb.connect(
            host=dcfg["mysql"]["host"],
            user=dcfg["mysql"]["user"],
            passwd=dcfg["mysql"]["password"],
            db=dcfg["mysql"]["db"],
            port=dcfg["mysql"]["port"]
        )
        logging.info("Database connection successful.")
        return db_connection
    except MySQLdb.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None

# Forgot Password - Send OTP
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        logging.warning("Request to /forgot_password missing email.")
        return jsonify({"message": "Missing email"}), 400

    logging.info(f"Received forgot password request for email: {email}")
    db_connection = mysqlconnect()
    if db_connection is None:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            otp = random.randint(100000, 999999)
            otp_store[email] = otp
            send_otp(email, otp)  # Send OTP to user's email
            logging.info(f"Generated OTP for {email}: {otp}")
            cursor.close()
            return jsonify({"message": "OTP sent to email"}), 200
        else:
            logging.warning(f"Email not found in the database: {email}")
            cursor.close()
            return jsonify({"message": "Email not found"}), 404
    except Exception as e:
        logging.error(f"Failed to send OTP for {email}: {e}")
        return jsonify({"message": "Failed to send OTP", "error": str(e)}), 500

# Reset Password using OTP
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')

    if not email or not otp or not new_password:
        logging.warning("Request to /reset_password missing email, OTP, or new password.")
        return jsonify({"message": "Missing email, OTP, or new password"}), 400

    logging.info(f"Received reset password request for email: {email} with OTP: {otp}")
    if email in otp_store and otp_store[email] == otp:
        hashed_password = generate_password_hash(new_password)
        db_connection = mysqlconnect()
        if db_connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        try:
            cursor = db_connection.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            db_connection.commit()
            logging.info(f"Password reset successful for email: {email}")
            cursor.close()
            del otp_store[email]
            return jsonify({"message": "Password reset successful"}), 200
        except Exception as e:
            logging.error(f"Failed to reset password for {email}: {e}")
            return jsonify({"message": "Failed to reset password", "error": str(e)}), 500
    else:
        logging.warning(f"Invalid OTP attempt for email: {email}")
        return jsonify({"message": "Invalid OTP"}), 400

# Helper function to send OTP via HTML email
def send_otp(email, otp):
    from_email = "datasparkaisolutions@gmail.com"
    from_password = "mrgnqanvdwzlkcae"
    to_email = email

    subject = "Your OTP for Password Reset"
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #333333; text-align: center;">Password Reset OTP</h2>
            <p style="font-size: 16px; color: #666666;">
                Hello,
            </p>
            <p style="font-size: 16px; color: #666666;">
                Your One-Time Password (OTP) for resetting your password is:
            </p>
            <h1 style="font-size: 24px; color: #1a73e8; text-align: center;">{otp}</h1>
            <p style="font-size: 16px; color: #666666;">
                Please use this OTP to complete the password reset process. This OTP is valid for a limited time and should not be shared with anyone.
            </p>
            <hr style="border: none; border-top: 1px solid #dddddd; margin: 20px 0;">
            <p style="font-size: 14px; color: #999999; text-align: center;">
                If you did not request a password reset, please ignore this email.
            </p>
            <p style="font-size: 14px; color: #999999; text-align: center;">
                &copy; 2024 Fotia Inc. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """

    # Create a MIMEText object with HTML content
    msg = MIMEText(html_body, "html")
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        logging.info(f"Sending OTP to {email}")
        server = smtplib.SMTP('smtp.hostinger.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logging.info(f"OTP email sent to {email}")
    except Exception as e:
        logging.error(f"Failed to send OTP email to {email}: {e}")

if __name__ == '__main__':
    logging.info("Starting Flask app on port 5003")
    app.run(host='0.0.0.0', port=5003, debug=True)

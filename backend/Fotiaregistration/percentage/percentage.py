from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database connection details
db_config = {
    "host": "141.136.42.65",
    "user": "root",
    "password": "Test@2024",
    "database": "fotia_database"
}

def get_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
    )

@app.route('/get-performance', methods=['GET'])
def get_performance():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Fetch direct_referral_count for the given user_id
        query = "SELECT direct_referal_count FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"error": "User not found"}), 404
        
        direct_referral_count = result[0]
        
        # Calculate performance percentage
        percentage = min(direct_referral_count * 4, 100)  # Each referral adds 4%, capped at 100%
        
        return jsonify({"percentage": percentage}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True,port=5022, use_reloader=False)

from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure MySQL connection
db_config = {
    "host": "141.136.42.65",
    "user": "root",
    "password": "Test@2024",
    "database": "fotia_database"
}

@app.route("/commissions", methods=["GET"])
def get_commissions():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to fetch commissions based on user_id
        query = """
            SELECT parent_id, usdt_amount, timestamp 
            FROM commissions 
            WHERE parent_id = %s
            ORDER BY timestamp ASC
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # Format the results into a JSON-friendly structure
        data = [{"date": row[2].strftime("%Y-%m-%d"), "amount": float(row[1])} for row in results]

        cursor.close()
        connection.close()

        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True,port=5021, use_reloader=False)

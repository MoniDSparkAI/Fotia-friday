# from flask import Flask, jsonify, request
# from flask_cors import CORS  # Import CORS for cross-origin requests
# import mysql.connector
# import logging
# from mysql.connector import Error
 
# # Initialize Flask application
# app = Flask(__name__)
 
# # Enable CORS for all domains (or configure as per your needs)
# CORS(app)
 
# # Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
 
# # Database connection details
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'Dsais@123',
#     'database': 'fotia_database'
# }
 
# def get_db_connection():
#     try:
#         logger.debug("Attempting to connect to the database...")
#         return mysql.connector.connect(**db_config)
#     except Error as e:
#         logger.error(f"Error connecting to MySQL: {e}")
#         return None
 
# def build_mlm_tree(parent_id, level):
#     connection = get_db_connection()
#     if connection is None:
#         logger.error("No database connection available.")
#         return []
 
#     cursor = connection.cursor(dictionary=True)
#     logger.debug(f"Fetching child users for parent_id: {parent_id} at level {level}")
 
#     # Fetch child users for the given parent and level
#     query = """
#         SELECT uh.child_id, u.username, uh.level
#         FROM user_hierarchy uh
#         JOIN users u ON uh.child_id = u.id
#         WHERE uh.parent_id = %s AND uh.level = %s
#     """
#     cursor.execute(query, (parent_id, level))
#     children = cursor.fetchall()
 
#     # Recursively build the MLM tree
#     mlm_tree = []
#     for child in children:
#         child_tree = {
#             'id': str(child['child_id']),
#             'name': child['username'],
#             'children': build_mlm_tree(child['child_id'], level + 1)  # Increment level for deeper hierarchy
#         }
#         mlm_tree.append(child_tree)
 
#     cursor.close()
#     connection.close()
#     logger.debug(f"Completed fetching children for parent_id: {parent_id} at level {level}")
#     return mlm_tree
 
# @app.route('/mlm-tree', methods=['GET'])
# def get_mlm_tree_data():
#     user_id = request.args.get('user_id', type=int)
#     if not user_id:
#         logger.error("User ID is missing in the request.")
#         return jsonify({'error': 'User ID is required'}), 400
 
#     logger.debug(f"Received request to build MLM tree for user_id: {user_id}")
 
#     # Start building the tree from level 1
#     mlm_tree_data = build_mlm_tree(user_id, 1)
#     if not mlm_tree_data:
#         logger.warning(f"No hierarchy data found for user_id: {user_id}")
#         return jsonify({'message': 'No hierarchy data found'}), 404
 
#     root_data = {
#         'id': str(user_id),
#         'name': 'Root User',
#         'children': mlm_tree_data
#     }
   
#     logger.debug(f"Returning MLM tree data for user_id: {user_id}")
#     return jsonify(root_data), 200
 
# if __name__ == '__main__':
#     logger.info("Starting Flask application...")
#     app.run(debug=True)
 
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS for cross-origin requests
import mysql.connector
import logging
from mysql.connector import Error
 
# Initialize Flask application
app = Flask(__name__)
 
# Enable CORS for all domains (or configure as per your needs)
CORS(app)
 
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
 
# Database connection details
db_config = {
    'host': '141.136.42.65',
    'user': 'root',
    'password': 'Test@2024',
    'database': 'fotia_database'
}
 
def get_db_connection():
    try:
        logger.debug("Attempting to connect to the database...")
        return mysql.connector.connect(**db_config)
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None
 
def build_mlm_tree(parent_id, level):
    connection = get_db_connection()
    if connection is None:
        logger.error("No database connection available.")
        return []
 
    cursor = connection.cursor(dictionary=True)
    logger.debug(f"Fetching children for parent_id: {parent_id} at level {level}")
 
    # Fetch children for the given parent and level (level 1 for the first set)
    query = """
        SELECT uh.child_id, u.username, uh.level
        FROM user_hierarchy uh
        JOIN users u ON uh.child_id = u.id
        WHERE uh.parent_id = %s AND uh.level = %s
    """
    cursor.execute(query, (parent_id, level))
    children = cursor.fetchall()
 
    # Log fetched children
    logger.debug(f"Level {level} - Parent {parent_id}: Found {len(children)} children: {children}")
 
    # Recursively build the MLM tree by considering each child as a new parent for the next level
    mlm_tree = []
    for child in children:
        logger.debug(f"Building tree for child_id: {child['child_id']} at level {level }")
        child_tree = {
            'id': str(child['child_id']),
            'name': child['username'],
            'children': build_mlm_tree(child['child_id'], level )  # Increment level for deeper hierarchy
        }
        mlm_tree.append(child_tree)
 
    cursor.close()
    connection.close()
    logger.debug(f"Completed fetching children for parent_id: {parent_id} at level {level} with {len(mlm_tree)} children.")
    return mlm_tree
 
@app.route('/api/mlm-tree', methods=['GET'])
def get_mlm_tree_data():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        logger.error("User ID is missing in the request.")
        return jsonify({'error': 'User ID is required'}), 400
 
    logger.debug(f"Received request to build MLM tree for user_id: {user_id}")
 
    # Start building the tree from level 1
    mlm_tree_data = build_mlm_tree(user_id, 1)
    if not mlm_tree_data:
        logger.warning(f"No hierarchy data found for user_id: {user_id}")
        return jsonify({'message': 'No hierarchy data found'}), 404
 
    root_data = {
        'id': str(user_id),
        'name': 'Root User',
        'children': mlm_tree_data
    }
   
    logger.debug(f"Returning MLM tree data for user_id: {user_id} with {len(mlm_tree_data)} top-level children.")
    return jsonify(root_data), 200
 
if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True)
 
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)  # Allow all origins by default

hostname = '13.233.103.184'
database = 'amadeus'
username ='amadeus'
password ='amadeus'
port_id = 5432

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=password,
        port = port_id
        )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'GET':
        cur.execute('SELECT * FROM test_testernames ORDER BY id')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users)

    if request.method == 'POST':
        new_user = request.json
        cur.execute('INSERT INTO test_testernames (name, status) VALUES (%s, %s) RETURNING id',
                    (new_user['username'], 1))
        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': user_id, 'message': 'User added successfully'}), 201

# @app.route('/users/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     # cur.execute('DELETE FROM users WHERE id = %s', (id,))
#     cur.execute(f"""
#                 UPDATE test_testernames
#                 SET status = 0
#                 WHERE id = %s 
#                 RETURNING *
#             """, (id))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return jsonify({'message': 'User updated successfully'}), 200

@app.route('/users/<int:id>/inactivate', methods=['PATCH'])  # or 'PUT'
def inactivate_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            UPDATE test_testernames
            SET status = 0
            WHERE id = %s 
            RETURNING *
        """, (id,))
        updated_user = cur.fetchone()
        if updated_user:
            conn.commit()
            return jsonify({'message': 'User inactivated successfully', 'user': updated_user}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2270,debug=True)
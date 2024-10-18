from flask import Flask, jsonify
from models import fetch_suppliers

app = Flask(__name__)

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    try:
        suppliers = fetch_suppliers()
        return jsonify(suppliers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
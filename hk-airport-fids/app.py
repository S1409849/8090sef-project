from flask import Flask, render_template, jsonify, request
from fids_manager import FIDSManager

app = Flask(__name__)

# Global manager
manager = FIDSManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flights')
def get_flights_api():
    # Load fresh data from API on request
    is_arrival = request.args.get('arrival', 'false').lower() == 'true'
    manager.load_data(is_arrival=is_arrival)
    
    status = request.args.get('status', 'all')
    query = request.args.get('query', '')
    return jsonify(manager.get_flights(status, query))

if __name__ == '__main__':
    # Initial load
    manager.load_data()
    app.run(debug=True, port=5000)

from flask import Flask, render_template, jsonify, request
from fids_manager import FIDSManager

app = Flask(__name__)

# Initialize a global manager instance to handle flight data
manager = FIDSManager()

@app.route('/')
def index():
    """
    Render the main dashboard page.
    """
    return render_template('index.html')

@app.route('/api/flights')
def get_flights_api():
    """
    API endpoint to fetch flight data.
    Query Parameters:
        arrival (str): 'true' for arrivals, 'false' for departures.
        status (str): Filter by status (e.g., 'all', 'boarding', 'delayed').
        query (str): Search term for flight ID, destination/origin, or airline.
    """
    # Determine flight type (Arrival or Departure)
    is_arrival = request.args.get('arrival', 'false').lower() == 'true'
    
    # Reload fresh data from HKIA API on every request to ensure real-time info
    manager.load_data(is_arrival=is_arrival)
    
    # Retrieve filters from request
    status = request.args.get('status', 'all')
    query = request.args.get('query', '')
    
    # Return JSON response of filtered flights
    return jsonify(manager.get_flights(status, query))

if __name__ == '__main__':
    # Initial data load for departures on startup
    manager.load_data()
    
    # Start the Flask development server
    app.run(debug=True, port=5000)

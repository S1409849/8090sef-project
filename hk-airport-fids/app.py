import json
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

class Flight:
    def __init__(self, raw_data):
        self.scheduled_time = raw_data.get('time', '00:00')
        flights = raw_data.get('flight', [])
        if flights:
            self.flight_id = flights[0].get('no', 'N/A')
            self.airline = flights[0].get('airline', 'N/A')
        else:
            self.flight_id = 'N/A'
            self.airline = 'N/A'
        
        destinations = raw_data.get('destination', [])
        self.destination = " / ".join(destinations)
        self.gate = raw_data.get('gate', '---') or '---'
        self.terminal = raw_data.get('terminal', 'T1')
        self.raw_status = raw_data.get('status', '')
        self.status_text, self.status_class = self._map_status(self.raw_status)

    def _map_status(self, raw):
        if not raw:
            return "ON TIME", "status-on-time"
        
        raw_lower = raw.lower()
        if "dep" in raw_lower or "gate closed" in raw_lower:
            # Check if it was departed
            return "DEPARTED", "status-departed"
        if "cancelled" in raw_lower:
            return "CANCELLED", "status-cancelled"
        if any(x in raw_lower for x in ["boarding", "final call", "last call"]):
            return "BOARDING", "status-boarding"
        if "est at" in raw_lower or "delayed" in raw_lower:
            return "DELAYED", "status-delayed"
        
        return "ON TIME", "status-on-time"

    def to_dict(self):
        return {
            "time": self.scheduled_time,
            "id": self.flight_id,
            "destination": self.destination,
            "gate": self.gate,
            "status": self.status_text,
            "class": self.status_class,
            "terminal": self.terminal
        }

class FIDSManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.flights = []
        self.last_updated = ""

    def load_data(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            all_flights = []

            if isinstance(data, list) and len(data) > 0:
                latest_day = data[-1]
                self.last_updated = latest_day.get('lastUpdatedTime', '')
                for item in latest_day.get('list', []):
                    all_flights.append(Flight(item))
            
            self.flights = all_flights
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def get_flights(self, status_filter='all'):
        if status_filter == 'all':
            return [f.to_dict() for f in self.flights]
        
        filter_map = {
            "boarding": "BOARDING",
            "on-time": "ON TIME",
            "delayed": "DELAYED",
            "departed": "DEPARTED",
            "cancelled": "CANCELLED"
        }
        
        target_status = filter_map.get(status_filter)
        if not target_status:
            return [f.to_dict() for f in self.flights]
            
        return [f.to_dict() for f in self.flights if f.status_text == target_status]

manager = FIDSManager('terminal.json')
manager.load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flights')
def get_flights():
    status = request.args.get('status', 'all')
    return jsonify(manager.get_flights(status))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

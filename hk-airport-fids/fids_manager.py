import json
import ssl
import urllib.request
from datetime import datetime
from flight import Flight

class FIDSManager:
    def __init__(self):
        self.flights = []
        self.last_updated = ""
        # Create an unverified SSL context to bypass certificate issues
        self.ssl_context = ssl._create_unverified_context()

    def load_data(self, date_str=None):
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        url = f"https://www.hongkongairport.com/flightinfo-rest/rest/flights/past?date={date_str}&lang=en&cargo=false&arrival=false"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                response_data = response.read().decode('utf-8')
                data = json.loads(response_data)
            
            all_flights = []
            if isinstance(data, list) and len(data) > 0:
                # Find the object that contains the flight list (usually the first or matching the date)
                target_day = data[0]
                for day in data:
                    if day.get('date') == date_str:
                        target_day = day
                        break
                
                self.last_updated = target_day.get('lastUpdatedTime', '')
                for item in target_day.get('list', []):
                    all_flights.append(Flight(item))
            
            self.flights = all_flights
            return True
        except Exception as e:
            print(f"Error fetching data from API: {e}")
            return False

    def get_flights(self, status_filter='all', query=None):
        filtered_flights = self.flights
        
        if status_filter != 'all':
            filter_map = {
                "boarding": "BOARDING",
                "on-time": "ON TIME",
                "delayed": "DELAYED",
                "departed": "DEPARTED",
                "cancelled": "CANCELLED"
            }
            target_status = filter_map.get(status_filter)
            if target_status:
                filtered_flights = [f for f in filtered_flights if f.status_text == target_status]
        
        if query:
            query = query.lower()
            filtered_flights = [
                f for f in filtered_flights 
                if query in f.flight_id.lower() or 
                   query in f.destination.lower() or 
                   query in f.airline.lower()
            ]
            
        return [f.to_dict() for f in filtered_flights]

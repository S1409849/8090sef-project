import json
import ssl
import urllib.request
from datetime import datetime
from flight import ArrivalFlight, DepartureFlight

class FIDSManager:
    """
    Manager class to handle fetching, parsing, and filtering flight data
    from the Hong Kong International Airport (HKIA) API.
    """
    def __init__(self):
        """
        Initialize the manager with an empty flight list and SSL context.
        """
        self.flights = []
        self.last_updated = ""
        # Create an unverified SSL context to bypass potential certificate verification issues
        # in some environments.
        self.ssl_context = ssl._create_unverified_context()

    def load_data(self, date_str=None, is_arrival=False):
        """
        Fetch flight data from the HKIA REST API.
        
        Args:
            date_str (str, optional): Date in YYYY-MM-DD format. Defaults to today.
            is_arrival (bool): True for arrivals, False for departures.
            
        Returns:
            bool: True if data was successfully loaded, False otherwise.
        """
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # HKIA API URL with arrival/departure flag
        arrival_param = "true" if is_arrival else "false"
        url = f"https://www.hongkongairport.com/flightinfo-rest/rest/flights/past?date={date_str}&lang=en&cargo=false&arrival={arrival_param}"
        
        try:
            # Set a common User-Agent to avoid 403 Forbidden errors from the API
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            # Perform the HTTP request
            with urllib.request.urlopen(req, context=self.ssl_context) as response:
                response_data = response.read().decode('utf-8')
                data = json.loads(response_data)
            
            all_flights = []
            # The API returns a list of objects, one for each date requested (usually just one)
            if isinstance(data, list) and len(data) > 0:
                # Find the object that matches our target date
                target_day = data[0]
                for day in data:
                    if day.get('date') == date_str:
                        target_day = day
                        break
                
                # Update the timestamp of the last data sync
                self.last_updated = target_day.get('lastUpdatedTime', '')
                
                # Parse each flight item into the appropriate Flight subclass
                for item in target_day.get('list', []):
                    if is_arrival:
                        all_flights.append(ArrivalFlight(item))
                    else:
                        all_flights.append(DepartureFlight(item))
            
            self.flights = all_flights
            return True
        except Exception as e:
            # Log the error (could be improved with a proper logger)
            print(f"Error fetching data from API: {e}")
            return False

    def get_flights(self, status_filter='all', query=None):
        """
        Retrieve filtered and searched flight data.
        
        Args:
            status_filter (str): Filter by flight status (e.g., 'boarding', 'delayed').
            query (str, optional): Search term for flight ID, location, or airline.
            
        Returns:
            list: List of dictionaries containing flight data.
        """
        filtered_flights = self.flights
        
        # Apply status-based filtering
        if status_filter != 'all':
            # Map frontend filter keys to internal status text
            filter_map = {
                "boarding": "BOARDING",
                "on-time": "ON TIME",
                "delayed": "DELAYED",
                "departed": "DEPARTED",
                "cancelled": "CANCELLED",
                "landed": "LANDED",
                "arrived": "ARRIVED"
            }
            target_status = filter_map.get(status_filter)
            if target_status:
                filtered_flights = [f for f in filtered_flights if f.status_text == target_status]
        
        # Apply text-based search (case-insensitive)
        if query:
            query = query.lower()
            filtered_flights = [
                f for f in filtered_flights 
                if query in f.flight_id.lower() or 
                   query in f.location.lower() or 
                   query in f.airline.lower()
            ]
            
        # Convert objects to dictionaries for the frontend
        return [f.to_dict() for f in filtered_flights]

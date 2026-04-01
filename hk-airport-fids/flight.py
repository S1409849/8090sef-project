from abc import ABC, abstractmethod

class Flight(ABC):
    def __init__(self, raw_data):
        self.scheduled_time = raw_data.get('time', '00:00')
        flights = raw_data.get('flight', [])
        if flights:
            self.flight_id = flights[0].get('no', 'N/A')
            self.airline = flights[0].get('airline', 'N/A')
        else:
            self.flight_id = 'N/A'
            self.airline = 'N/A'
        
        self.gate = raw_data.get('gate', '---') or '---'
        self.terminal = raw_data.get('terminal', 'T1')
        self.raw_status = raw_data.get('status', '')
        
        # Initialize location and status which are handled by subclasses
        self.location = self._extract_location(raw_data)
        self.status_text, self.status_class = self._map_status(self.raw_status)

    @abstractmethod
    def _extract_location(self, raw_data):
        pass

    @abstractmethod
    def _map_status(self, raw):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def to_dict(self):
        return {
            "time": self.scheduled_time,
            "id": self.flight_id,
            "location": self.location,
            "gate": self.gate,
            "status": self.status_text,
            "class": self.status_class,
            "terminal": self.terminal,
            "airline": self.airline,
            "type": self.get_type()
        }

class ArrivalFlight(Flight):
    def _extract_location(self, raw_data):
        origins = raw_data.get('origin', [])
        return " / ".join(origins)

    def _map_status(self, raw):
        if not raw:
            return "ON TIME", "status-on-time"
        
        raw_lower = raw.lower()
        if "cancelled" in raw_lower:
            return "CANCELLED", "status-cancelled"
        if "delayed" in raw_lower or "est at" in raw_lower:
            return "DELAYED", "status-delayed"
        if "at gate" in raw_lower or "landed" in raw_lower:
            return "LANDED", "status-departed"
        if "arrived" in raw_lower:
            return "ARRIVED", "status-departed"
            
        return "ON TIME", "status-on-time"

    def get_type(self):
        return "Arrival"

class DepartureFlight(Flight):
    def _extract_location(self, raw_data):
        destinations = raw_data.get('destination', [])
        return " / ".join(destinations)

    def _map_status(self, raw):
        if not raw:
            return "ON TIME", "status-on-time"
        
        raw_lower = raw.lower()
        if "cancelled" in raw_lower:
            return "CANCELLED", "status-cancelled"
        if "delayed" in raw_lower or "est at" in raw_lower:
            return "DELAYED", "status-delayed"
        if "dep" in raw_lower or "gate closed" in raw_lower:
            return "DEPARTED", "status-departed"
        if any(x in raw_lower for x in ["boarding", "final call", "last call"]):
            return "BOARDING", "status-boarding"
            
        return "ON TIME", "status-on-time"

    def get_type(self):
        return "Departure"

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
            "terminal": self.terminal,
            "airline": self.airline
        }

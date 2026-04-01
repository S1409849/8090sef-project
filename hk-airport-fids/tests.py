import os
import sys
# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
from unittest.mock import patch, MagicMock
import json
from app import app
from flight import ArrivalFlight, DepartureFlight
from fids_manager import FIDSManager

class TestFlightModels(unittest.TestCase):
    def test_arrival_flight_extraction(self):
        raw_data = {
            "time": "10:30",
            "flight": [{"no": "CX 123", "airline": "CPA"}],
            "origin": ["London", "Paris"],
            "status": "Landed 10:25",
            "gate": "A1"
        }
        flight = ArrivalFlight(raw_data)
        self.assertEqual(flight.location, "London / Paris")
        self.assertEqual(flight.status_text, "LANDED")
        self.assertEqual(flight.get_type(), "Arrival")

    def test_departure_flight_extraction(self):
        raw_data = {
            "time": "14:00",
            "flight": [{"no": "SQ 456", "airline": "SIA"}],
            "destination": ["Singapore"],
            "status": "Boarding",
            "gate": "B5"
        }
        flight = DepartureFlight(raw_data)
        self.assertEqual(flight.location, "Singapore")
        self.assertEqual(flight.status_text, "BOARDING")
        self.assertEqual(flight.get_type(), "Departure")

    def test_status_mapping_on_time(self):
        raw_data = {"status": ""}
        arr_flight = ArrivalFlight(raw_data)
        dep_flight = DepartureFlight(raw_data)
        self.assertEqual(arr_flight.status_text, "ON TIME")
        self.assertEqual(dep_flight.status_text, "ON TIME")

class TestFIDSManager(unittest.TestCase):
    def setUp(self):
        self.manager = FIDSManager()
        # Sample data to mock API response
        self.mock_api_data = [
            {
                "date": "2026-04-01",
                "list": [
                    {
                        "time": "08:00",
                        "flight": [{"no": "CX 101", "airline": "CPA"}],
                        "destination": ["Sydney"],
                        "status": "Departed"
                    },
                    {
                        "time": "09:00",
                        "flight": [{"no": "KA 202", "airline": "HDA"}],
                        "destination": ["Beijing"],
                        "status": ""
                    }
                ]
            }
        ]

    @patch('urllib.request.urlopen')
    def test_load_data_success(self, mock_urlopen):
        # Mocking the context manager and read()
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.mock_api_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        success = self.manager.load_data(date_str="2026-04-01", is_arrival=False)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.flights), 2)
        self.assertEqual(self.manager.flights[0].flight_id, "CX 101")

    def test_filtering_and_search(self):
        # Manually populate flights for testing logic
        self.manager.flights = [
            DepartureFlight({"time": "08:00", "flight": [{"no": "CX 101", "airline": "CPA"}], "destination": ["Sydney"], "status": "Dep"}),
            DepartureFlight({"time": "09:00", "flight": [{"no": "KA 202", "airline": "HDA"}], "destination": ["Beijing"], "status": ""})
        ]
        
        # Test status filter
        departed = self.manager.get_flights(status_filter="departed")
        self.assertEqual(len(departed), 1)
        self.assertEqual(departed[0]['id'], "CX 101")

        # Test search query
        search = self.manager.get_flights(query="Beijing")
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0]['id'], "KA 202")

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('fids_manager.FIDSManager.load_data')
    @patch('fids_manager.FIDSManager.get_flights')
    def test_api_endpoint(self, mock_get_flights, mock_load_data):
        mock_load_data.return_value = True
        mock_get_flights.return_value = [{"id": "TEST 123"}]

        response = self.app.get('/api/flights?arrival=false&query=TEST')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[0]['id'], "TEST 123")
        mock_load_data.assert_called_with(is_arrival=False)

if __name__ == '__main__':
    unittest.main()

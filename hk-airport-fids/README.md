# HKIA Flight Information Display System (FIDS)

A modern, web-based Flight Information Display System for Hong Kong International Airport (HKIA), built with Python (Flask) and a polished frontend using Tailwind CSS. This project fetches live data from the official HKIA REST API and features a robust Object-Oriented Programming (OOP) architecture.

## 🚀 Features

- **Live Data Feed**: Flight data fetched directly from the Hong Kong International Airport REST API.
- **Dual Mode Support**: Seamlessly switch between **Arrivals** and **Departures**.
- **Advanced Search**: Instant server-side search across Flight IDs, Destinations/Origins, and Airlines.
- **Dynamic Filtering**: Filter flights by status (Boarding, Landed, Delayed, etc.) with mode-specific logic.
- **Modern UI**: A clean, responsive "Airport Board" aesthetic inspired by international terminals.

## 🏗️ Architecture (OOP Design)

The backend is designed using core OOP principles, including Abstraction, Inheritance, and Polymorphism:

- **`Flight` (Abstract Base Class)**: Defines the blueprint for all flight types. It enforces mandatory implementations for location extraction and status mapping.
- **`ArrivalFlight` & `DepartureFlight` (Subclasses)**: Specialized classes that inherit from `Flight`. They handle unique data fields (e.g., `origin` vs. `destination`) and distinct status logic (e.g., `Landed` vs. `Boarding`).
- **`FIDSManager`**: A central coordinator that handles API communication, SSL context management, and complex filtering logic.
- **Flask Integration**: A lightweight web layer that maps RESTful routes to the manager's business logic.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Async/Await)
- **Data Source**: HKIA FlightInfo REST API
- **Communication**: JSON-based RESTful API

## 📋 Prerequisites

- Python 3.7+
- Flask (`pip install flask`)

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hk-airport-fids
   ```

2. **Install dependencies**:
   ```bash
   pip install flask
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the system**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## 📂 Project Structure

```text
.
├── app.py              # Flask application entry point & routing
├── flight.py           # OOP models (Abstract Flight, Arrival, Departure)
├── fids_manager.py     # Business logic & API data management
├── templates/
│   └── index.html      # Frontend template (Tailwind CSS + JS)
└── README.md           # Project documentation
```


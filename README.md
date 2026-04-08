# 8090SEF Project 🚀

Welcome to the **8090SEF Project** repository. This workspace contains a collection of software engineering projects, ranging from full-stack applications to fundamental data structure implementations.

## 📂 Sub-Projects

### 1. [HKIA Flight Information Display System (FIDS)](./hk-airport-fids/)
A modern, web-based Flight Information Display System for Hong Kong International Airport (HKIA).

*   **Tech Stack**: Python (Flask), Tailwind CSS, JavaScript (Async/Await).
*   **Key Features**:
    *   **Live Data**: Fetches real-time flight info from the HKIA REST API.
    *   **OOP Architecture**: Built using Abstract Base Classes (`Flight`) and specialized subclasses (`ArrivalFlight`, `DepartureFlight`).
    *   **Dynamic UI**: Responsive "Airport Board" aesthetic with server-side search and filtering.
*   **Quick Start**:
    ```bash
    cd hk-airport-fids
    pip install flask
    python app.py
    ```

### 2. [Data Structures and Algorithms Study](./Data%20Structures%20and%20Algorithms%20Study/)
A repository of clean, well-documented Python implementations of essential computer science concepts.

*   **Implementations**:
    *   **Red-Black Tree (`rb_tree.py`)**: A self-balancing binary search tree with $O(\log n)$ performance. Fully documented in English.
    *   **Sliding Window Rate Limiter (`sliding_window.py`)**: A thread-safe implementation of the sliding window algorithm for rate limiting.
*   **Usage**:
    ```bash
    cd "Data Structures and Algorithms Study"
    python3 sliding_window.py  # Run the rate limiter demo
    ```

---

## 🛠️ Project Structure

```text
.
├── Data Structures and Algorithms Study/  # Algorithm research and implementation
│   ├── rb_tree.py                         # Red-Black Tree implementation
│   └── sliding_window.py                  # Thread-safe Rate Limiter
└── hk-airport-fids/                       # Full-stack FIDS application
    ├── app.py                             # Flask application entry point
    ├── flight.py                          # OOP models (Abstract & Concrete classes)
    ├── fids_manager.py                    # API & Business logic coordinator
    └── templates/                         # Frontend UI (Tailwind CSS)
```

## 📋 Prerequisites
- Python 3.7+
- Flask (`pip install flask`)

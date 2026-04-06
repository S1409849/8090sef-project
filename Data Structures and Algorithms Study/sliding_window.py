import time
import threading
from collections import deque

class SlidingWindowRateLimiter:
    """
    Implementation of the Sliding Window rate limiting algorithm.
    """
    def __init__(self, limit, window_size):
        self.limit = limit  # Maximum number of requests allowed within the window
        self.window_size = window_size  # Window size in seconds
        self.requests = deque()  # Queue to store request timestamps
        self.lock = threading.Lock()  # Lock to ensure thread safety

    def allow_request(self):
        with self.lock:
            now = time.time()
            
            # Remove all timestamps that are outside the current window
            while self.requests and self.requests[0] <= now - self.window_size:
                self.requests.popleft()
            
            # Check if the number of requests in the current window has reached the limit
            if len(self.requests) < self.limit:
                self.requests.append(now)
                return True
            return False

def task(limiter, thread_id):
    """
    Simulates a task performed by a thread.
    """
    for i in range(5):
        allowed = limiter.allow_request()
        timestamp = time.strftime('%H:%M:%S')
        status = "Allowed" if allowed else "Denied"
        print(f"[Thread-{thread_id}] Request {i+1}: {status} | Time: {timestamp}")
        # Simulate requests at small intervals
        time.sleep(0.5)

if __name__ == "__main__":
    # Requirement: Limit to 10 requests every 10 seconds
    limit_count = 10
    window_seconds = 10
    limiter = SlidingWindowRateLimiter(limit=limit_count, window_size=window_seconds)

    print(f"Starting Rate Limiter Test: {limit_count} requests per {window_seconds} seconds\n")

    # Create 5 threads, each sending 5 requests (Total 25 requests)
    threads = []
    for i in range(5):
        t = threading.Thread(target=task, args=(limiter, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nTest completed.")

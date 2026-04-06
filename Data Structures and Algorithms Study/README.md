# Data Structures and Algorithms Study

This project contains Python implementations of fundamental data structures and common algorithms.

## Project Structure

- `rb_tree.py`: A well-documented implementation of a **Red-Black Tree** in English, featuring insertion, search, and deletion operations.
- `sliding_window.py`: A thread-safe **Sliding Window Rate Limiter** implementation using the Sliding Window algorithm.

---

## 1. Red-Black Tree (`rb_tree.py`)

A Red-Black Tree is a self-balancing binary search tree that maintains $O(\log n)$ performance for all major operations.

### Key Features
- **Node Properties**: Every node is either red or black, and the tree maintains balance through rotations and recoloring.
- **Operations**: 
  - `insert(key)`: Adds a new key and restores RB properties.
  - `find(key)`: Searches for a key and returns the node or `None`.
  - `delete(key)`: Removes a key and restores balance.
- **English Implementation**: The code is fully documented in English with detailed explanations of the rotation and balancing cases.

### Usage Example
```python
from rb_tree import RedBlackTree

tree = RedBlackTree()
tree.insert(10)
node = tree.find(10)
tree.delete(10)
```

---

## 2. Sliding Window Rate Limiter (`sliding_window.py`)

This module implements a rate limiting algorithm that accurately tracks requests over a moving time window.

### Features
- **Algorithm**: Sliding Window (tracks exact timestamps).
- **Concurrency**: Thread-safe implementation using `threading.Lock`.
- **Demo**: Includes a multi-threaded test case simulating 25 requests against a limit of 10 requests per 10 seconds.

### How to Run Demo
```bash
python3 sliding_window.py
```

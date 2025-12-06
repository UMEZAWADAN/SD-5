# Efficiency Analysis Report for SD-5

## Overview

This report documents several efficiency issues identified in the SD-5 codebase, a Flask-based care management system. The analysis covers both Python backend code (`app.py`, `app2.py`) and JavaScript frontend code.

## Efficiency Issues Identified

### 1. Redundant NumPy Array Conversions in Similar Cases Search (app.py:125-146)

**Location:** `similar_cases()` function in `app.py`

**Issue:** The function converts `input_emb` to a numpy array inside the loop for every case, even though it's already a numpy array from `fake_embedding()`. Additionally, each case's embedding (stored as a list) is converted to a numpy array on every iteration.

**Current Code:**
```python
for case in cases:
    sim = cosine_sim(
        np.array(input_emb),      # Redundant - already numpy array
        np.array(case["embedding"])  # Converted every iteration
    )
```

**Impact:** O(n) unnecessary array conversions where n is the number of cases.

**Recommended Fix:** Remove redundant conversion of `input_emb` and pre-convert case embeddings when loading.

### 2. Multiple Sequential Database Queries in get_all_data (app.py:535-583)

**Location:** `get_all_data()` function in `app.py`

**Issue:** The function executes 5 separate SQL queries sequentially to fetch data for a single client:
- client table
- visit_record table
- physical_status table
- dasc21 table
- dbd13 table

**Impact:** Multiple database round trips increase latency, especially under load.

**Recommended Fix:** Combine queries using JOINs or use a single query with UNION, or fetch data in parallel using async operations.

### 3. No Database Connection Pooling (app.py, app2.py)

**Location:** `get_connection()` function used throughout both files

**Issue:** Every API endpoint creates a new database connection. No connection pooling mechanism is implemented.

**Current Code:**
```python
def get_connection():
    return pymysql.connect(**DB_CONFIG)
```

**Impact:** Connection overhead for every request, potential connection exhaustion under high load.

**Recommended Fix:** Implement connection pooling using libraries like `DBUtils` or `SQLAlchemy`'s built-in pooling.

### 4. Loading All Cases from Pickle File on Every Search (app.py:125-146)

**Location:** `similar_cases()` and `register_case()` functions

**Issue:** The pickle file containing all cases is loaded from disk on every API call. For search operations, all cases are loaded, similarity computed for each, then sorted.

**Impact:** O(n) disk I/O and memory allocation per request, where n is the total number of cases.

**Recommended Fix:** Implement caching (e.g., using Flask-Caching or a simple in-memory cache) or migrate to a database with vector search capabilities.

### 5. Inefficient DOM Queries in Tab Switching (static/js/shousai.js:2-11)

**Location:** Tab switching event handler in `shousai.js`

**Issue:** Inside each click handler, the code queries all `.tab-btn` and `.tab-content` elements repeatedly.

**Current Code:**
```javascript
btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    // ...
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
});
```

**Impact:** Redundant DOM queries on every tab click.

**Recommended Fix:** Cache the NodeLists outside the event handler.

### 6. Duplicate Code Between app.py and app2.py

**Location:** Both `app.py` and `app2.py`

**Issue:** Both files contain nearly identical implementations of:
- `load_cases()`
- `save_cases()`
- `fake_embedding()`
- `cosine_sim()`
- `register_case()`
- `similar_cases()`

**Impact:** Maintenance burden, potential for bugs when one file is updated but not the other.

**Recommended Fix:** Extract common functionality into a shared module.

## Summary

| Issue | Severity | Complexity to Fix |
|-------|----------|-------------------|
| Redundant NumPy conversions | Medium | Low |
| Sequential DB queries | Medium | Medium |
| No connection pooling | High | Medium |
| Pickle file loading | Medium | Medium |
| Inefficient DOM queries | Low | Low |
| Duplicate code | Low | Low |

## Selected Fix for PR

This PR addresses **Issue #1: Redundant NumPy Array Conversions** as it provides a clear, contained efficiency improvement with low risk of breaking existing functionality.

# Data Harvester
A Python application designed to fetch and process data from APIs. It currently uses the `requests` library for HTTP operations and `matplotlib` for data visualization, with plans to migrate to `httpx` and `seaborn` respectively.

## Features
- Fetch data from multiple API endpoints using HTTP GET and POST requests
- Analyze user engagement and post statistics with integrated visualizations
- Generate dashboards combining data fetching, analysis, and visualization

## Project Structure
```
src/
├── __init__.py
├── api_client.py        # API data collection
├── analyzer.py          # Data analysis and visualization
├── dashboard.py         # Dashboard generation
└── main.py              # Main application orchestrator
```

## Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python -m pytest
   ```

3. Run the application directly (optional):
   - Install and run `json-server`:
      ```bash
      npm install -g json-server
      json-server --watch db.json --port 3000
      ```
   - Run the Data Harvester application
      ```bash
      python -m src.main
      ```


## Warmup Task: Add Post Search Functionality
This warmup task is designed to help you get familiar with the structure of the codebase and the process of adding new functionality and tests.

### Objective
You will add a new `fetch_user_posts()` function to `api_client.py` that searches for all posts made by a user (by `user_id`), then write a test to verify its behavior.

### Steps

1. **Locate the File**:
   - Open the `src/api_client.py` file in your editor.

2. **Add the New Function**:
   - Add a new function called `fetch_user_posts()` to search for posts made by a user.

3. **Write a Test**:
   - Open the `tests/test_api_client.py` file.
   - Add a test called `test_fetch_user_posts()` to verify the behavior of `fetch_user_posts()`.

4. **Run the Test**:
   - Use the following command to run the test and ensure your changes work as expected:
     ```bash
     python -m pytest tests/test_api_client.py::test_fetch_user_posts -v
     ```

5. **Verify the Output**:
   - Check that the test passes successfully. If not, review your code and make necessary adjustments.

6. **Reflection**:
   - After completing the task, take a moment to review the `api_client.py` and `test_api_client.py` files. Note how the code is structured and how tests are written to validate functionality.

# Data Harvester
A Python application designed to fetch and process data from APIs. It currently uses the `requests` library for HTTP operations and `matplotlib` for data visualization, with plans to migrate to `httpx` and `plotly` respectively. See [this report](./temp_report.md) for WIP migration details.

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


## Warmup Task: Add Post Title Analysis
This warmup task is designed to help you get familiar with the structure of the codebase and the process of adding new functionality and tests.

### Objective
You will add a new `calculate_average_post_length()` function to `analyzer.py` that calculates the average character length of post titles, then write a test to verify its behavior.

### Steps

1. **Locate the Function Stub**:
   - Open the `src/analyzer.py` file in your editor.
   - Find the `calculate_average_post_length()` function and read the docstring to understand expected behavior.

2. **Add the New Function**:
   - Implement the `calculate_average_post_length()` function, which should:
     - Accept a list of post dictionaries
     - Calculate the average length of the 'title' field across all posts
     - Return `0.0` if the list is empty or no valid titles exist

3. **Write a Test**:
   - Open the `tests/test_analyzer.py` file.
   - Find the `test_calculate_average_post_length()` test and read the docstring.
   - Implement the test to verify the `calculate_average_post_length()` function
     - Use the `sample_posts` fixture from `conftest.py` as the argument used in the function

4. **Run the Test**:
   - Use the following command to run the test and ensure your changes work as expected:
     ```bash
     python -m pytest tests/test_analyzer.py::test_calculate_average_post_length -v
     ```

5. **Verify the Output**:
   - Check that the test passes successfully. If not, review your code and make necessary adjustments.

6. **Reflection**:
   - After completing the task, take a moment to review the `analyzer.py` and `test_analyzer.py` files. Note how the code is structured and how tests are written to validate functionality.

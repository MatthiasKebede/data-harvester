# Data Harvester
A Python application designed to fetch and process data from APIs. It currently uses the `requests` library for HTTP operations and `tablib` for data handling + export to CSV, with plans to migrate to `httpx` and `pandas` respectively.

## Project Structure
```
src/
├── __init__.py
├── api_client.py        # API data collection
├── analyzer.py          # Data analysis and CSV exports
├── dashboard.py         # Dashboard generation
└── main.py
```

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/MatthiasKebede/data-harvester.git
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv/Scripts/activate
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python -m pytest -v
   ```

4. Run the application directly (optional - you only need to use the tests):
   - Install and run `json-server` (in a new terminal window):
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
   - Open the `src/analyzer.py` file in your editor
   - Find the `calculate_average_post_length()` function and read the docstring to understand expected behavior

2. **Add the New Function**:
   - Implement the `calculate_average_post_length()` function, which should:
     - Accept a list of post dictionaries
     - Calculate the average length of the 'title' field across all posts
     - Return `0.0` if the list is empty or no valid titles exist

3. **Write a Test**:
   - Open the `tests/test_analyzer.py` file
   - Find the `test_calculate_average_post_length()` test and read the docstring
   - Implement the test to verify the `calculate_average_post_length()` function
     - Use the `sample_posts` fixture from `conftest.py` as the argument used in the function

4. **Run the Test**:
   - Use the following command to run the test and ensure your changes work as expected:
     ```bash
     python -m pytest tests/test_analyzer.py::test_calculate_average_title_length -v
     ```
   - Check that the test passes successfully. If not, review your code and make necessary adjustments.

5. **Reflection**:
   - After completing the task, take a moment to review the `analyzer.py` and `test_analyzer.py` files. Note how the code is structured and how tests are written to validate functionality.
   - Make a Git commit before moving on
     ```bash
     git add .
     git commit -m "Warmup completed"
     ```


## Migration Hints:
- Make sure to check the imports at the top of the module
- You may have to migrate the tests that correspond to migrated functions
- If you are having trouble with the test suite during/after a migration, carefully check the names of the mocked functions/values
  - Also, make sure that the test suite passes when `json-server` is NOT running
- For the `tablib` to `pandas` migration, switching from a `Dataset` to `DataFrame` often involves swapping the order of operations:
  ```python
  # tablib Dataset (build structure first)
  dataset = tablib.Dataset()
  dataset.headers = ['Name', 'Age']
  dataset.append(["Alice", 25])
  ```
  ```python
  # pandas DataFrame (build data first)
  data = [{'Name': 'Alice', 'Age': 25}, {'Name': 'Bob', 'Age': 20}]
  dataframe = pandas.DataFrame(data)
  ```
- Helpful Links:
  - https://requests.readthedocs.io/en/latest/
  - https://www.python-httpx.org/compatibility/
  - https://tablib.readthedocs.io/en/stable/
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

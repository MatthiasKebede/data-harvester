# Data Harvester
The Data Harvester is a Python application designed to fetch and process data from the web. It currently uses the `requests` library for HTTP operations and `matplotlib` for data visualization, with plans to migrate to `httpx` and `seaborn` respectively.

## Features
- Fetch data from multiple API endpoints using HTTP GET and POST requests
- Process and clean data with normalization and field extraction
- Generate visualizations including bar charts, line charts, pie charts, histograms, and scatter plots
- Create comprehensive reports with statistics and embedded visualizations

## Source Code
```
src/
├── __init__.py
├── http_client.py        # HTTP client for API requests
├── data_fetcher.py       # High-level data fetching interface
├── data_processor.py     # Data cleaning and statistical analysis
├── visualizer.py         # Data visualization
├── report_generator.py   # Report generation with charts
└── main.py               # Main application entry point
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


## Overview
### Basic Data Fetching
```python
from src.data_fetcher import DataFetcher

# Initialize fetcher with base URL
fetcher = DataFetcher(base_url="https://api.example.com")

# Fetch user data
user_data = fetcher.fetch_user_data("12345")

# Fetch posts with filtering
posts = fetcher.fetch_posts(user_id="12345", limit=10)

# Close connection when done
fetcher.close()
```

### Data Processing
```python
from src.data_processor import DataProcessor

processor = DataProcessor()

# Clean and normalize data
cleaned_data = processor.clean_data(raw_data)

# Calculate statistics
stats = processor.calculate_statistics(data_list, 'views')
print(f"Average views: {stats['mean']}")

# Filter data
popular_posts = processor.filter_data(posts, 'likes', lambda x: x > 100)
```

### Creating Visualizations
```python
from src.visualizer import DataVisualizer

visualizer = DataVisualizer(output_dir="output")

# Create a bar chart
data = {'Category A': 100, 'Category B': 150, 'Category C': 120}
chart_path = visualizer.plot_bar_chart(
    data,
    title="Category Distribution",
    xlabel="Category",
    ylabel="Count"
)

# Create a line chart
trend_data = {'Jan': 100, 'Feb': 120, 'Mar': 150, 'Apr': 140}
visualizer.plot_line_chart(trend_data, title="Monthly Trend")
```

### Generating Reports
```python
from src.report_generator import ReportGenerator

generator = ReportGenerator(output_dir="reports")

# Generate summary report with statistics and visualizations
report = generator.generate_summary_report(
    data=posts,
    numeric_fields=['views', 'likes', 'shares'],
    report_name='monthly_summary'
)

print(f"Report saved to: {report['report_path']}")
print(f"Visualizations: {report['visualizations']}")
```


## Warmup Task: Update and Add New Fetching Methods
This warmup task is designed to help you get familiar with the structure of the codebase and the process of adding new functionality and tests. Example data can be found in [db.json](db.json).

### Objective
You will add a new `fetch_post()` method and update the existing `fetch_posts()` method in `data_fetcher.py`. Then, you will write one test for each function to ensure that they work as expected.

### Steps

1. **Locate the File**:
   - Open the `src/data_fetcher.py` file in your editor.

2. **Update the Existing Function**:
   - Modify the `fetch_posts()` function to accept an optional `category` argument. If provided, the function should filter posts by the specified category.

2. **Add the New Function**:
   - Add a new function called `fetch_post()` to retrieve a specific post by its ID.

3. **Write a Test**:
   - Open the `tests/test_data_fetcher.py` file.
   - Add new test functions to verify the newly-added behavior (two tests in total). These tests should call the relevant functions and assert the result.

4. **Run the Test**:
   - Use the following command to run the test and ensure your changes work as expected:
     ```bash
     python -m pytest tests/test_data_fetcher.py -v
     ```

5. **Verify the Output**:
   - Check that the new tests pass successfully. If not, review your code and make necessary adjustments.

6. **Reflection**:
   - After completing the task, take a moment to review the `data_fetcher.py` and `test_data_fetcher.py` files. Note how the code is structured and how tests are written to validate functionality.

# Data Harvester
The Data Harvester is a Python application designed to fetch and process data from various APIs. It currently uses the `requests` library for HTTP operations and `matplotlib` for data visualization, with plans to migrate to `httpx` and `seaborn` respectively.

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
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

## Usage
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


## Warmup Task: Add a New Aggregation Function
This warmup task is designed to help you get familiar with the structure of the codebase and the process of adding new functionality and tests.

### Objective
You will add a new function to the `data_processor.py` file that counts the frequency of unique values in a dataset field. Then, you will write a test for this function to ensure it works as expected.

### Steps

1. **Locate the File**:
   - Open the `src/data_processor.py` file in your editor.

2. **Add the New Function**:
   - Add a new function called `count_frequencies()` to the `DataProcessor` class. This function will count how many times each unique value appears in a specified field.
   - Example implementation:
     ```python
     def count_frequencies(self, data_list: List[Dict[str, Any]], field: str) -> Dict[str, int]:
         """
         Count the frequency of unique values in a field.

         Args:
             data_list: List of data dictionaries
             field: Field name to count frequencies for

         Returns:
             Dictionary with values as keys and their counts as values
         """
         frequencies = {}
         for item in data_list:
             if field in item:
                 value = str(item[field])
                 frequencies[value] = frequencies.get(value, 0) + 1
         return frequencies
     ```

3. **Write a Test**:
   - Open the `tests/test_data_processor.py` file.
   - Add a test function to verify the behavior of `count_frequencies()`.
   - Example test:
     ```python
     def test_count_frequencies(self):
         """Test counting value frequencies."""
         processor = DataProcessor()
         data = [
             {'category': 'A', 'value': 10},
             {'category': 'B', 'value': 20},
             {'category': 'A', 'value': 15},
             {'category': 'C', 'value': 30},
             {'category': 'A', 'value': 25}
         ]
         frequencies = processor.count_frequencies(data, 'category')
         
         assert frequencies['A'] == 3
         assert frequencies['B'] == 1
         assert frequencies['C'] == 1
         assert len(frequencies) == 3
     ```

4. **Run the Test**:
   - Use the following command to run the test and ensure your changes work as expected:
     ```bash
     pytest tests/test_data_processor.py::TestDataProcessor::test_count_frequencies -v
     ```

5. **Verify the Output**:
   - Check that the test passes successfully. If it fails, review your code and make necessary adjustments.

6. **Reflection**:
   - After completing the task, take a moment to review the `data_processor.py` and `test_data_processor.py` files. Note how the code is structured and how tests are written to validate functionality.

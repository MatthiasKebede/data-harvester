# Data Harvester

The Data Harvester is a Python application designed to fetch and process data from various APIs. It currently uses the `requests` library for HTTP operations, with plans to migrate to `httpx` for enhanced performance and features.

## Features
- Fetch user data from the User Service API.
- Retrieve catalog information from the Catalog Service API.
- Generate reports based on fetched data.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

## Migration Plan
The application will be migrated from `requests` to `httpx` to leverage asynchronous capabilities and improved performance.

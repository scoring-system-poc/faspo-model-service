# [ FASPO ] Model Service

This repository contains source code for the _Model Service_ in FASPO concept project. The _Model Service_ is 
a part of much larger system that is utilizing microservices architecture. It's main responsibility is to execute 
calculations with given data that scores the subject. The calculations are based on the data provided by the 
_Online-Data Service_ and _Batch-Data Service_.

NOTE: all currently implemented calculations are completely made up and from business point of view
pretty much nonsensical

## Prerequisites

* Python 3.11 or higher
* packages listed in `requirements.txt`
* Docker (optional, for containerization)

## Environment Variables

* `APPLICATIONINSIGHTS_CONNECTION_STRING`
  * Connection string for Azure Application Insights
  * for local testing set to `InstrumentationKey=00000000-0000-0000-0000-000000000000` and ignore errors from `azure.monitor.opentelemetry`
* `REQUIRED_DOCUMENT_TYPES`
  * List of required document types for the model
  * default: `["001", "002"]`
* `REQUIRED_DOCUMENT_PERIODS`
  * Number of periods required for the model
  * default: `3`
* `OPTIONAL_CASHFLOW_DOCUMENT_TYPE`
  * Document type for optional cashflow documents
  * default: `"003"`
* `OPTIONAL_LOAN_DOCUMENT_TYPE`
  * Document type for optional loan documents
  * default: `"080"`
* `DATA_TARGET_URL`
  * URL of the internal data target, i.e. Store Service HOST
* `LOG_INFO`: 
  * Log level for info messages 
  * default: `INFO`

## Installation (Direct)

1. Make sure Python 3.11 is installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment:
    ```bash
     source venv/bin/activate
     ```
6. Install the required packages:
7. ```bash
   pip install -r requirements.txt
   ```
9. Run the application:
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --host <your_host> --port <your_port>
   ```
10. The application should now be running and accessible at `http://0.0.0.0:8080`.

## Installation (Docker)

1. Make sure Docker is installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Build the Docker image:
   ```bash
   docker build -t model-service .
   ```
5. Run the Docker container:
   ```bash
    docker run -d -p 8080:8080 --env <ENV_NAME>=<ENV_VALUE> -- model-service
    ```

# ReadMe

## Overview

This FastAPI application provides an interface for managing projects and billing information. It allows users to create projects, record billing data, and calculate monthly billing summaries. The application uses SQLAlchemy for database interactions and Pydantic for data validation.

## Features

- **Create Projects**: Define new projects with essential details and billing types.
- **Create Billing Records**: Log billing information for existing projects.
- **Calculate Monthly Billing**: Retrieve billing summaries for a specified month.
- **Retrieve All Projects and Billings**: Access lists of all projects and billings stored in the database.

## Requirements

- Python 3.7+
- FastAPI
- Pydantic
- SQLAlchemy
- A compatible database (e.g., SQLite, PostgreSQL)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install fastapi sqlalchemy pydantic uvicorn
   ```

4. Ensure that your database models (`Project` and `Billing`) are defined in the `models.py` file.

## Usage

1. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

2. The application will be accessible at `http://127.0.0.1:8000`.

3. You can view the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Create a Project

- **Endpoint**: `POST /projects/`
- **Request Body**: Project details (name, client, address, etc.)
- **Response**: Confirmation message and created project details.

### Create Billing

- **Endpoint**: `POST /create-billing/`
- **Request Body**: Billing details (project ID, resource name, billing month, etc.)
- **Response**: Confirmation message and created billing details.

### Calculate Monthly Billing

- **Endpoint**: `POST /calculate-monthly-billing/`
- **Request Body**: Billing month in the format `YYYY-MM`.
- **Response**: List of billing summaries for the specified month.

### Retrieve All Projects

- **Endpoint**: `GET /projects/`
- **Response**: List of all projects.

### Retrieve All Billings

- **Endpoint**: `GET /billings/`
- **Response**: List of all billing records.

## Models

### Project Model

- **project_name**: Name of the project.
- **client_name**: Name of the client.
- **address**: Project address.
- **post_code**: Postal code.
- **country**: Country of the project.
- **billing_type**: Type of billing (hourly, monthly, fixed-bid).
- **contract_status**: Status of the contract (active, inactive).
- **start_date**: Start date (format: dd-mm-yyyy).
- **end_date**: End date (optional, format: dd-mm-yyyy).
- **hourly_price**: Hourly price (optional, must be >= 0).
- **fixed_price**: Fixed price (optional, must be >= 0).

### Billing Model

- **project_id**: ID of the associated project.
- **allocated_resource**: Name of the allocated resource.
- **month_of_billing**: Month of billing (format: YYYY-MM).
- **year_of_billing**: Year of billing.
- **total_hours**: Total hours billed (must be > 0).
- **description**: Optional description of the billing.

### Billing Summary Model

- **project_name**: Name of the project.
- **resource_name**: Name of the allocated resource.
- **total_amount_usd**: Total billing amount in USD (must be > 0).
- **month**: Billing month (1-12).
- **year**: Billing year.

## Notes

- Ensure that the database connection is properly configured in the `SessionLocal` defined in your `models.py`.
- The application should handle database migrations as needed. Consider using Alembic for managing migrations.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

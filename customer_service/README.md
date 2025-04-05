# CustomerService - Customer Management Backend

This repository contains the backend for the **CustomerService** application, built using Django and utilizing PostgreSQL as the database. This backend supports managing customer information (CRUD - Create, Read, Update, Delete) and handling customer addresses.

## Table of Contents

- [Features](#features)
- [Database](#database)
- [File Structure](#file-structure)
- [Running the Application](#running-the-application)
  - [Run with Docker](#run-with-docker)
  - [Run without Docker](#run-without-docker)
- [API Endpoints](#api-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Address Endpoints](#address-endpoints)
- [Testing the API](#testing-the-api)

## Features

- **Customer Information Management**: Supports CRUD operations (Create, Read, Update, Delete) for customer data.
- **Address Management**: Manages addresses associated with customers, including details such as street, city, state, postal code, country, and an option for default shipping address.

## Database

The application uses **PostgreSQL** as the database to store customer and address information.

## File Structure

Here is the detailed file structure of Customer Service:

```
ecommerce-microservices/
└── customer-service/
    ├── customers/             # Django app
    │   ├── migrations/
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py          # Define models Customer, Address
    │   ├── serializers.py     # Define serializers
    │   ├── tests.py
    │   ├── urls.py            # URLs for app 'customers'
    │   └── views.py           # Views (API endpoints)
    ├── customer_service/      # Django project settings
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py        # Setup project, database
    │   ├── urls.py            # The main URLS of Project
    │   └── wsgi.py            # WSGI application for deployment
    ├── .dockerignore
    ├── .env                   # Environment variables (DB credentials, etc.)
    ├── Dockerfile             # Dockerfile to build Docker image
    ├── docker-compose.yml     # Docker compose to run customer_service (Django + PostgreSQL)
    ├── manage.py
    ├── requirements.txt       # Project dependencies
    └── README.md               # This README file
```

## Running the Application

### Run with Docker

1. **Open a terminal**: Navigate to the `customer-service/` directory (where the `docker-compose.yml` file is located).

2. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```
   - `--build`: Forces Docker Compose to rebuild the image if there are changes in the `Dockerfile` or source code.
   - The first run may take some time to download the PostgreSQL image and build the Django application image.

3. **Check the logs**: 
   - You will see logs from both containers (database and application).
   - Watch for any errors. Ensure you see a log line indicating that Django has successfully run migrations and that Gunicorn (or `runserver`) has started on port 8000.
  
> **Stopping and Removing Containers**

1. **Stop the containers**:
   - Press `Ctrl + C` in the terminal running `docker-compose up`.

2. **Remove containers and network (keep the database volume)**:
   ```bash
   docker-compose down
   ```

3. **Remove containers, network, and volume (delete all database data)**:
   ```bash
   docker-compose down -v
   ```

### Run without Docker

#### Prerequisites

Ensure the following are installed on your system:

-   **Python**: Version 3.8 or later (check with `python3 --version` or `python --version`)
-   **PostgreSQL**: Installed and running (e.g., via `apt`, `brew`, or a Windows installer)
-   **pip**: Python package installer (check with `pip3 --version` or `pip --version`)

#### Installation Steps

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/VietHungHoang/ecommerce_microservice_django.git
    cd customer-service
    ```

2. **Create and Activate a Virtual Environment (Optional)**:

    - **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    - **MacOS/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
        After activation, your terminal prompt should change (e.g., `(venv)` appears).

3. **Install Dependencies**:
   Create a `requirements.txt` file with the following content (or use an existing one):

    ```
    Django>=4.0,<5.0
    djangorestframework>=3.14,<3.15
    psycopg2-binary>=2.9,<3.0
    python-dotenv>=1.0,<2.0
    gunicorn>=20.0,<21.0
    django-environ>=0.11,<0.12
    ```

    Install the dependencies within the virtual environment:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up PostgreSQL Database**:

    - Create a PostgreSQL database:
        ```bash
        psql -U postgres
        CREATE DATABASE customer_service;
        \q
        ```
    - Configure the database settings in your Django `settings.py` file:
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'customer_service',
                'USER': 'postgres',
                'PASSWORD': 'your_password',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```
        Adjust `USER`, `PASSWORD`, `HOST`, and `PORT` to match your PostgreSQL setup.

5. **Apply Migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://localhost:8000`. For production, use Gunicorn:
    ```bash
    gunicorn --bind 0.0.0.0:8000 customer_service.wsgi
    ```
    Replace `customer_service.wsgi` with the actual path to your WSGI file if different.

#### Notes

-   Ensure PostgreSQL is running before starting the app (e.g., use `pg_ctl start` or system service commands).
-   To use environment variables with `python-dotenv` or `django-environ`, create a `.env` file in the project root with your database credentials:
    ```
    DB_NAME=customer_service
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    ```
    Update `settings.py` to load these variables if needed (e.g., using `django-environ`).
-   To deactivate the virtual environment after use, run:
    ```bash
    deactivate
    ```
-   The default port is `8000`, unlike `8001` in the Docker setup. Adjust as needed.




## API Endpoints

### Customer Endpoints

| HTTP Method | Endpoint                          | Description                          |
|-------------|-----------------------------------|--------------------------------------|
| `GET`       | `/api/customers/`                 | Retrieve a list of all customers     |
| `POST`      | `/api/customers/`                 | Create a new customer                |
| `GET`       | `/api/customers/{customer_id}/`   | Retrieve details of a customer       |
| `PUT/PATCH` | `/api/customers/{customer_id}/`   | Update customer information          |
| `DELETE`    | `/api/customers/{customer_id}/`   | Delete a customer                    |

### Address Endpoints

| HTTP Method | Endpoint                          | Description                          |
|-------------|-----------------------------------|--------------------------------------|
| `GET`       | `/api/addresses/`                 | Retrieve a list of all addresses     |
| `POST`      | `/api/addresses/`                 | Create a new address                 |
| `GET`       | `/api/addresses/{address_id}/`    | Retrieve details of an address       |
| `PUT/PATCH` | `/api/addresses/{address_id}/`    | Update address information           |
| `DELETE`    | `/api/addresses/{address_id}/`    | Delete an address                    |

## Testing the API

1. **Open a browser or a tool like Postman/Insomnia** to test the endpoints.

2. **Access the endpoints**:
   - **Customer list**: `http://localhost:8001/api/customers/` (GET - List, POST - Create)
   - **Customer details**: `http://localhost:8001/api/customers/{customer_id}/` (GET - Retrieve, PUT/PATCH - Update, DELETE)
   - **Address list**: `http://localhost:8001/api/addresses/` (GET - List, POST - Create)
   - **Address details**: `http://localhost:8001/api/addresses/{address_id}/` (GET - Retrieve, PUT/PATCH - Update, DELETE)

3. **Example: Create a Customer** (POST to `http://localhost:8001/api/customers/`):
   ```json
   {
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com",
       "password": "aSecurePassword123"
   }
   ```

4. **Example: Create an Address** (POST to `http://localhost:8001/api/addresses/`):
   ```json
   {
       "customer_id": "your_customer_uuid_here",
       "street_address": "123 Main St",
       "city": "Anytown",
       "state": "CA",
       "postal_code": "12345",
       "country": "USA",
       "is_default_shipping": true
   }
   ```


---

Happy coding! 🚀
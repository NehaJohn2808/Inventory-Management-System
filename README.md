# Inventory Management System

## Project Overview

The **Inventory Management System** is a web-based application developed using Python Flask and MySQL. It helps manage inventory operations, including product information, sales records, and user details.

The project demonstrates the use of web development, database connectivity, software testing, and Continuous Integration (CI) using Jenkins. It can be executed locally or using Docker.

## Technologies Used

- **Programming Language:** Python
- **Backend Framework:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL / MariaDB
- **Database Management:** phpMyAdmin
- **Testing:** Python Unit Testing
- **CI Tool:** Jenkins
- **Containerization:** Docker
- **Version Control:** Git and GitHub

## Project Structure

```text
Inventory-Management-System/
│
├── app.py
├── requirements.txt
├── test_app.py
├── Jenkinsfile
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
│
├── static/
│
└── templates/
```

## Prerequisites

Install the following software before running the project:

- Python 3.11 or later
- XAMPP (MySQL / MariaDB and phpMyAdmin)
- Git
- Docker Desktop (for Docker execution)
- Jenkins (for CI pipeline execution)

## 1. Clone the Repository

Open a terminal and execute:

```bash
git clone https://github.com/NehaJohn2808/Inventory-Management-System.git
```

Navigate into the project directory:

```bash
cd Inventory-Management-System
```

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

## 4. Database Configuration

The application uses MySQL / MariaDB as its database.

### Start the Database

1. Open XAMPP Control Panel.
2. Start Apache.
3. Start MySQL.
4. Open phpMyAdmin:

   http://localhost:8080/phpmyadmin/

### Create the Database

Create a database named:

```sql
CREATE DATABASE inventory_db;
```

If a database export (`.sql` file) is included in the repository, select `inventory_db` in phpMyAdmin and import that file to create the required tables and records.

If no SQL export is included, the required database tables must be created using the project's database schema before running the application.

### Configure Environment Variables

Create a file named `.env` in the project root directory.

Add the following configuration:

```env
SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=
DB_NAME=inventory_db
```

**Note:**
- Change `DB_PORT` if your MySQL / MariaDB server uses a different port.
- Enter your database password in `DB_PASSWORD` if one is configured.
- Keep your actual `.env` file private. Do not upload it to GitHub.

## 5. Run the Application

After configuring the database, execute:

```bash
python app.py
```

Open the application in your browser:

http://127.0.0.1:5000/

## 6. Run Unit Tests

The project includes unit tests to verify application functionality.

Execute:

```bash
python -m unittest -v test_app
```

The test results will display the number of tests executed and whether they passed or failed.

## 7. Continuous Integration Using Jenkins

Jenkins is used to automate the build and testing process.

### Jenkins Pipeline Steps

1. Create a Jenkins job named `Inventory-Management-CI`.
2. Configure the GitHub repository URL.
3. Configure the project branch.
4. Use the `Jenkinsfile` available in the repository.
5. Configure the job as a Pipeline.
6. Execute the Jenkins pipeline.

### CI Pipeline Operations

The Jenkins pipeline performs the following operations:

- Retrieves the project source code from GitHub.
- Installs the required Python dependencies.
- Performs Python compilation checks.
- Executes unit tests.
- Generates test reports.

This helps identify errors early and improves software quality.

## 8. Docker Setup

Docker is used to package the application and its dependencies into a container.

### Build the Docker Image

```bash
docker build -t inventory-management-system:latest .
```

### Run the Docker Container

For a local XAMPP database running on port `3307`, execute:

```bash
docker run -d --name inventory-container -p 5001:5000 --add-host=host.docker.internal:host-gateway -e DB_HOST=host.docker.internal -e DB_PORT=3307 -e DB_USER=root -e DB_PASSWORD= -e DB_NAME=inventory_db -e SECRET_KEY=inventory_secret_key inventory-management-system:latest
```

If your database has a password,

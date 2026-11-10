
# Inventory Management System

A web-based Inventory Management System developed using Python, Flask and MySQL. This project supports product management, stock tracking, sales management and reports.

## Technologies Used

- Python
- Flask
- MySQL
- HTML, CSS
- Git and GitHub
- Jenkins
- Docker

## Project Structure

```text
Inventory-Management-System/
│
├── static/
├── templates/
├── app.py
├── requirements.txt
├── test_app.py
├── Jenkinsfile
├── README.md
└── .gitignore
```

## 1. Prerequisites

Install the following:

- Python 3.x
- MySQL Server
- Git
- Docker (optional)
- Jenkins (for CI pipeline)

## 2. Clone the Repository

Open Command Prompt or VS Code Terminal.

```bash
git clone https://github.com/NehaJohn2808/Inventory-Management-System.git
```

Move into the project folder:

```bash
cd Inventory-Management-System
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## 5. Configure MySQL Database

Start your MySQL Server.

Create the database:

```sql
CREATE DATABASE inventory_db;
```

Select the database:

```sql
USE inventory_db;
```

**Important:** The application also requires the `users`, `products` and `sales` tables. Set up the project database tables before starting the application. The SQL schema should be provided with the project.

## 6. Configure Environment Variables

Create a file named `.env` in the main project folder.

Add the following configuration:

```env
SECRET_KEY=replace_with_your_own_secret_key
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_db
```

Replace `your_mysql_password` with your own MySQL password.

If your MySQL server uses a different port, update `DB_PORT`.

Do not upload the `.env` file or your database password to GitHub.

## 7. Run the Application

Make sure MySQL is running and the database is configured.

Execute:

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000/
```

## 8. Run Unit Tests

Execute:

```bash
python -m unittest -v test_app
```

## 9. Jenkins CI Pipeline

The repository contains a Jenkinsfile for the CI pipeline.

Jenkins is used to automate the project testing and build process.

The pipeline can be executed through the configured Jenkins job.

## 10. Docker Commands

Build the Docker image:

```bash
docker build -t inventory-management-system:latest .
```

Run the Docker container:

```bash
docker run -p 5000:5000 inventory-management-system:latest
```

Note: Configure the database connection appropriately when running the application inside Docker.

## 11. Git Commands for Team Members

Check the current status:

```bash
git status
```

Get the latest changes:

```bash
git pull origin main
```

Add modified files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Updated Inventory Management System"
```

Push changes to GitHub:

```bash
git push origin main
```

## Project Team

 Name               Roll Number 
 B Chandini         24AG1A05BG 
 D Sathvika         24AG1A05BN 
 N Neha             24AG1A05CS 
 P Priyanka         24AG1A05CY 
Class: III Year B.Tech – CSE, Semester I, Section G  
College: ACE Engineering College
III Year B.Tech – CSE, Semester I, Section G.
ACE Engineering College.

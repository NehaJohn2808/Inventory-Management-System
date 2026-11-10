
# Inventory Management System

A web-based Inventory Management System developed using Python, Flask and MySQL. This project helps manage products, stock and sales through a web application.

## Technologies Used

- Python
- Flask
- MySQL
- HTML and CSS
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

Install the following software:

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

Move into the project directory:

```bash
cd Inventory-Management-System
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

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

## 5. Database Configuration

1. Start MySQL Server.
2. Create the project database using MySQL:

```sql
CREATE DATABASE inventory_db;
```

3. Configure the database connection using the settings required by the application.
4. Create or import the required database tables before running the application.

**Note:** Each team member must configure their own MySQL username, password and database connection.

## 6. Run the Application

After installing dependencies and configuring MySQL, execute:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## 7. Run Unit Tests

Execute the following command:

```bash
python -m unittest -v test_app
```

## 8. Jenkins CI Pipeline

The project includes a Jenkinsfile for Continuous Integration.

Jenkins is used to automate the build and testing process.

To execute the pipeline:

1. Open the Jenkins dashboard.
2. Select the configured Inventory Management CI job.
3. Click Build Now.
4. Check the Console Output.
5. Verify the test results.

## 9. Docker Commands

Build the Docker image:

```bash
docker build -t inventory-management-system:latest .
```

Run the Docker container:

```bash
docker run -p 5000:5000 inventory-management-system:latest
```

**Note:** Configure the database connection and Docker networking before running the application inside a container.

## 10. Git Commands for Team Members

Clone the repository:

```bash
git clone https://github.com/NehaJohn2808/Inventory-Management-System.git
```

Get the latest updates:

```bash
git pull origin main
```

Create a separate branch:

```bash
git checkout -b feature-your-name
```

Check modified files:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Updated Inventory Management System"
```

Push the branch:

```bash
git push origin feature-your-name
```

After pushing, create a Pull Request on GitHub to merge the changes into the main branch.

## Project Team

| Name | Roll Number |
|---|---|
| B Chandini | 24AG1A05BG |
| D Sathvika | 24AG1A05BN |
| N Neha | 24AG1A05CS |
| P Priyanka | 24AG1A05CY |

Class: III Year B.Tech – CSE, Semester I, Section G


**College:** ACE Engineering College

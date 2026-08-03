pipeline {
    agent any

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '3307'
        DB_USER = 'root'
        DB_PASSWORD = ''
        DB_NAME = 'inventory_test'
        SECRET_KEY = 'jenkins-test-secret'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m unittest test_app.py'
            }
        }

        stage('Build') {
            steps {
                echo 'Inventory Management System build completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed.'
        }
    }
}

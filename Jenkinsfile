pipeline {
agent any

```
environment {
    DB_HOST = 'localhost'
    DB_PORT = '3307'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'inventory_db'
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
            bat '"C:\\Users\\Neha John\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
        }
    }

    stage('Test') {
        steps {
            bat '"C:\\Users\\Neha John\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m unittest test_app.py'
        }
    }

    stage('Build') {
        steps {
            echo 'Build completed successfully.'
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
```

}

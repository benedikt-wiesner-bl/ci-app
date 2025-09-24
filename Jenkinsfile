pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:benedikt-wiesner-bl/ci-app.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ci-app:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name ci-app ci-app:latest'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
        failure {
            echo "Pipeline failed ❌"
        }
        success {
            echo "Pipeline succeeded ✅"
        }
    }
}

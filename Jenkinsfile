pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-ci-key',
                    url: 'git@github.com:benedikt-wiesner-bl/ci-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ci-app:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ci-app:latest pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker stop ci-app || true && docker rm ci-app || true'
                sh 'docker run -d -p 5000:5000 --name ci-app ci-app:latest'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
    }
}

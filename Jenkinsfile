pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "docker-compose"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:benedikt-wiesner-bl/ci-app.git',
                    credentialsId: 'github-ci-key'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ci-app:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ci-app:latest pytest -q'
            }
        }

        stage('Deploy (Full Reset)') {
            steps {
                sh '''
                    docker-compose stop ci-app || true
                    docker-compose rm -f ci-app || true
                    docker-compose build ci-app
                    docker-compose up -d ci-app

                '''
            }
        }

    }

    post {
        always {
            sh 'docker ps -a'
        }
        success {
            echo "✅ Deployment erfolgreich!"
        }
        failure {
            echo "❌ Deployment fehlgeschlagen!"
        }
    }
}

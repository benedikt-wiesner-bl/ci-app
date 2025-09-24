pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "docker compose"
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
                  # Stoppe und entferne alten Stack
                  ${DOCKER_COMPOSE} down

                  # Baue und starte alles frisch
                  ${DOCKER_COMPOSE} up -d --build
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline beendet."
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

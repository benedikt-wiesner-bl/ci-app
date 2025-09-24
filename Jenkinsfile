pipeline {
    agent any

    stages {


        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t ci-app:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ci-app:latest pytest -q'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker rm -f ci-app || true'
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

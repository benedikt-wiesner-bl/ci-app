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

        stage('Echo') {
            steps {
                echo '🚀 Jenkins CI läuft!'
            }
        }
    }
}

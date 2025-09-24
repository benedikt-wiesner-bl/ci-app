pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'git@github.com:benedikt-wiesner-bl/ci-app.git'
            }
        }
        stage('Hello') {
            steps {
                echo "Jenkins hat das Repo erfolgreich ausgecheckt!"
            }
        }
    }
}

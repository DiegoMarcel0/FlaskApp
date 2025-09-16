pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DiegoMarcel0/FlaskApp'
            }
        }

        stage('Build & Run containers') {
            steps {
                sh 'docker compose down || true' // bajar si había algo corriendo
                sh 'docker compose build'
                sh 'docker compose up -d'
            }
        }

        
    }
}
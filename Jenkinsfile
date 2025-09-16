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
                sh 'docker compose down' // bajar si había algo corriendo
                sh 'docker compose build'
                sh 'docker compose up -d'
            }
        }

        stage('Tests') {
            steps {
                // ejemplo: ejecutar pruebas dentro de un servicio
                sh 'docker-compose exec -T app pytest'
            }
        }

        
    }
}
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    def app = docker.build("k8s-calculator:${env.BUILD_ID}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    def app = docker.image("k8s-calculator:${env.BUILD_ID}")
                    app.inside {
                        sh 'python -m unittest discover -s tests'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        def app = docker.image("k8s-calculator:${env.BUILD_ID}")
                        app.push("${env.BUILD_ID}")
                        app.push("latest")
                    }
                }
            }
        }
    }
}

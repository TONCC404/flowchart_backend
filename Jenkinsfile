pipeline {
    agent any

    stages {
        stage('Clone Source') {
            steps {
                git 'https://github.com/TONCC404/flowchart_backend'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageName = "flowchart-app:latest"
                    sh "docker build -t ${imageName} ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    def containerName = "flowchart-app"
                    sh """
                        docker rm -f ${containerName} || true
                        docker run -d --name ${containerName} -p 8000:8000 my-python-app:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo '构建流程结束。'
        }
    }
}

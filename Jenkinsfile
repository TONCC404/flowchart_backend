pipeline {
    agent any

    stages {
        stage('Clone Source') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/TONCC404/flowchart_backend',
                        credentialsId: 'bbd8a232-d2d1-460d-9868-b14910c1ba18'
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageName = "flowchart-backend:latest"
                    sh "docker build -t ${imageName} ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    def containerName = "flowchart-backend"
                    sh """
                        docker rm -f ${containerName} || true
                        docker run -d --name ${containerName} -p 9876:9876 flowchart-backend:latest
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

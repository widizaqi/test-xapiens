pipeline {
    agent any

    environment {
        // Docker Hub details
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = "widizaqi/python-http-server:${env.BUILD_NUMBER}"
        
        // Kubernetes and Helm details
        HELM_RELEASE_NAME = "python-http-server"
        HELM_CHART_PATH = "./helm-chart" // Adjust if your Helm chart is in a different directory
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-file')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from the repository
                git 'https://github.com/widizaqi/test-xapiens.git' // Replace with your repository URL
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    // Write kubeconfig to file if needed for deployment stage
                    if (env.KUBECONFIG_CREDENTIALS) {
                        writeFile file: "${env.HOME}/.kube/config", text: env.KUBECONFIG_CREDENTIALS
                    }
                }

                // Build the Docker image
                sh 'docker build -t ${DOCKER_IMAGE} .'

                // Login to Docker Hub
                sh '''
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                '''

                // Push the Docker image to Docker Hub
                sh 'docker push ${DOCKER_IMAGE}'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Deploy using Helm
                sh '''
                    helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} \
                    --set image.repository=widizaqi/python-http-server \
                    --set image.tag=${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            // Clean up Docker images to free up space
            sh 'docker system prune -af'
        }
        success {
            echo 'Deployment succeeded!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}

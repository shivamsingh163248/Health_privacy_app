pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')     // Jenkins credentials ID
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')     // Jenkins credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '📦 Checking out source code...'
                git branch: 'Ansible_terraform_jenkins',
                    url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                echo '🚀 Initializing and applying Terraform...'
                dir('terraform') {
                    sh 'terraform init'
                    sh '''
                        terraform apply -auto-approve \
                        -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
                        -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed!'
        }
    }
}

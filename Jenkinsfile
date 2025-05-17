pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')     // Replace with your real Jenkins credential ID
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')     // Replace with your real Jenkins credential ID
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
                dir('terraform') { // if terraform files are inside a folder named "terraform"
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
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

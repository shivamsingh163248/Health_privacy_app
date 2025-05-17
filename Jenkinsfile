pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('your-aws-access-key-id-secret-id') // Set correct Jenkins credential ID
        AWS_SECRET_ACCESS_KEY = credentials('your-aws-secret-access-key-secret-id')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'Ansible_terraform_jenkins', url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir('terraform') { // Only if your Terraform files are in a 'terraform' folder
                    sh 'terraform init'
                    sh 'terraform plan'
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

pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')     // Jenkins credentials ID
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key') // Jenkins credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                    sh """
                        terraform apply -auto-approve \
                        -var "aws_access_key=$AWS_ACCESS_KEY_ID" \
                        -var "aws_secret_key=$AWS_SECRET_ACCESS_KEY"
                    """
                }
            }
        }

        stage('Extract EC2 Public IP') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                echo "Extracting public IP..."
                // Add your script here
            }
        }

        stage('Generate Ansible Inventory') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                echo "Generating Ansible inventory..."
                // Add your script here
            }
        }

        stage('Run Ansible Playbook') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                echo "Running Ansible playbook..."
                // Add your script here
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment Failed!'
        }
        success {
            echo '✅ Deployment Successful!'
        }
    }
}

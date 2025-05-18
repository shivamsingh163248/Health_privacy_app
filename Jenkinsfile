pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Ansible_terraform_jenkins', url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Apply') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds', 
                    usernameVariable: 'AWS_ACCESS_KEY_ID', 
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    dir('terraform') {
                        sh '''
    echo "🚀 Initializing Terraform..."
    terraform init -no-color

    echo "📦 Applying Terraform configuration..."
    TF_LOG=INFO terraform apply -auto-approve -input=false -no-color \
        -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
        -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}"
'''
                    }
                }
            }
        }

        stage('Prepare Ansible Inventory') {
            steps {
                sh '''
                    echo "[app]" > inventory.ini
                    echo "$(terraform -chdir=terraform output -raw public_ip)" >> inventory.ini
                '''
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                sh '''
                    ansible-playbook -i inventory.ini ansible/playbook.yml
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline failed!'
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
    }
}

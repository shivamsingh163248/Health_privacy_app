pipeline {
    agent any

    environment {
        TF_VAR_aws_access_key = credentials('aws-access-key')   // AWS Key from Jenkins Credentials
        TF_VAR_aws_secret_key = credentials('aws-secret-key')   // AWS Secret from Jenkins Credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init & Apply') {
            dir('terraform') {
                steps {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Extract EC2 Public IP') {
            steps {
                script {
                    env.PUBLIC_IP = sh(
                        script: "cd terraform && terraform output -raw ec2_public_ip",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Generate Ansible Inventory') {
            steps {
                sh '''
                    echo "[web]" > ansible/inventory.ini
                    echo "$PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa" >> ansible/inventory.ini
                '''
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                sh 'ansible-playbook -i ansible/inventory.ini ansible/playbook.yml'
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}

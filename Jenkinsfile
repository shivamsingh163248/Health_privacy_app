pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
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

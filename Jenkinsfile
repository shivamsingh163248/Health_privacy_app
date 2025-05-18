pipeline {
    agent any

    environment {
        TF_VAR_region = 'us-east-1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'Ansible_terraform_jenkins', url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            environment {
                TF_DIR = 'terraform'
            }
            steps {
                dir("${env.TF_DIR}") {
                    withCredentials([
                        string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                        string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                    ]) {
                        sh '''
                            echo "Running terraform init..."
                            terraform init

                            echo "Running terraform apply..."
                            terraform apply -auto-approve \
                                -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
                                -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}" \
                                -var="region=${TF_VAR_region}"
                        '''
                    }
                }
            }
        }

        stage('Generate Ansible Inventory') {
            steps {
                sh '''
                    echo "[app]" > inventory.ini
                    echo "$(terraform -chdir=terraform output -raw public_ip) ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa" >> inventory.ini
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

        stage('Verify App Deployment') {
            steps {
                script {
                    def ip = sh(script: "terraform -chdir=terraform output -raw public_ip", returnStdout: true).trim()
                    echo "App deployed at: http://${ip}:5000"
                }
            }
        }
    }
}

pipeline {
    agent any

    environment {
        TF_DIR = "terraform"
        ANSIBLE_DIR = "ansible"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Ansible_terraform_jenkins',
                    url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Apply') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    dir("${TF_DIR}") {
                        sh '''
                            echo "📝 Creating terraform.tfvars..."
                            echo 'aws_access_key = "${AWS_ACCESS_KEY_ID}"' > terraform.tfvars
                            echo 'aws_secret_key = "${AWS_SECRET_ACCESS_KEY}"' >> terraform.tfvars

                            echo "🚀 Initializing Terraform..."
                            terraform init

                            echo "📦 Applying Terraform configuration..."
                            terraform apply -auto-approve
                        '''
                    }
                }
            }
        }

        stage('Prepare Ansible Inventory') {
            steps {
                script {
                    def publicIp = sh(script: "cd ${TF_DIR} && terraform output -raw ec2_public_ip", returnStdout: true).trim()

                    sh """
                        echo "🌍 EC2 Public IP: ${publicIp}"
                        cd ${ANSIBLE_DIR}
                        echo "[web]" > inventory.ini
                        echo "${publicIp} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa" >> inventory.ini
                    """
                }
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        echo "📡 Running Ansible playbook..."
                        ansible-playbook -i inventory.ini playbook.yml
                    '''
                }
            }
        }
    }
}

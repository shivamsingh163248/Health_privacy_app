pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Ansible_terraform_jenkins', url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Plan') {
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

                            echo "🧠 Planning Terraform changes..."
                            terraform plan -no-color \
                                -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
                                -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}"
                        '''
                    }
                }
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
                            echo "📦 Applying Terraform configuration..."
                            terraform apply -auto-approve -input=false -no-color -parallelism=1 \
                                -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
                                -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}"
                        '''
                    }
                }
            }
        }

        stage('Prepare Ansible Inventory') {
            steps {
                script {
                    def publicIp = sh(
                        script: 'terraform -chdir=terraform output -raw public_ip',
                        returnStdout: true
                    ).trim()

                    writeFile file: 'inventory.ini', text: "[app]\n${publicIp}\n"
                    echo "🧾 Inventory file created with IP: ${publicIp}"
                }
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                sh '''
                    echo "🔧 Running Ansible playbook..."
                    ansible-playbook -i inventory.ini ansible/playbook.yml
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

pipeline {
    agent any

    environment {
        TF_IN_AUTOMATION = "true"
        
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'Ansible_terraform_jenkins',
                    url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            environment {
                // Load AWS credentials from Jenkins credentials store
                AWS_ACCESS_KEY_ID = credentials('aws-credentials')
            }
            steps {
                dir('terraform') {
                    withCredentials([usernamePassword(credentialsId: 'aws-credentials',
                                                      usernameVariable: 'AWS_ACCESS_KEY',
                                                      passwordVariable: 'AWS_SECRET_KEY')]) {
                        sh '''
                            echo "Initializing Terraform..."
                            terraform init

                            echo "Running Terraform Apply..."
                            terraform apply -auto-approve \
                                -var="aws_access_key=${AWS_ACCESS_KEY}" \
                                -var="aws_secret_key=${AWS_SECRET_KEY}"
                        '''
                    }
                }
            }
        }

        stage('Output Public IP') {
            steps {
                dir('terraform') {
                    sh '''
                        echo "EC2 Instance Public IP:"
                        terraform output ec2_public_ip
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Please check logs above."
        }
    }
}

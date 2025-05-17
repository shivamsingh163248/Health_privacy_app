pipeline {
    agent any

    environment {
        TF_WORKING_DIR = "terraform"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
                AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
            }
            steps {
                dir("${TF_WORKING_DIR}") {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
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

pipeline {
  agent any

  environment {
    TF_VAR_aws_access_key = credentials('aws-access-key')
    TF_VAR_aws_secret_key = credentials('aws-secret-key')
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'Ansible_terraform_jenkins',
            url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
      }
    }

    stage('Terraform Init & Apply') {
      steps {
        dir('terraform') {
          withCredentials([
            string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
            string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
          ]) {
            sh '''
              terraform init
              terraform apply -auto-approve \
                -var "aws_access_key=$AWS_ACCESS_KEY_ID" \
                -var "aws_secret_key=$AWS_SECRET_ACCESS_KEY"
            '''
          }
        }
      }
    }

    stage('Generate Ansible Inventory') {
      steps {
        // This will be skipped unless the Terraform stage succeeds
      }
    }

    stage('Ansible Playbook') {
      steps {
        // Your ansible-playbook command here
      }
    }
  }
}

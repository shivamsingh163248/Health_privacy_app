pipeline {
  agent any

  environment {
    // These env vars will be used by Terraform if you define them in variables.tf
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
        dir('terraform') {
          script {
            def publicIp = sh(script: "terraform output -raw public_ip", returnStdout: true).trim()
            writeFile file: '../ansible/inventory.ini', text: "[target]\n${publicIp} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa"
          }
        }
      }
    }

    stage('Run Ansible Playbook') {
      steps {
        dir('ansible') {
          sh '''
            ansible-playbook -i inventory.ini setup.yml
          '''
        }
      }
    }
  }
}

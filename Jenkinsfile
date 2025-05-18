pipeline {
  agent any

  environment {
    // Optional for later stages
    ANSIBLE_HOST_KEY_CHECKING = 'False'
  }

  stages {
    stage('Checkout Code') {
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
              export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
              export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

              terraform init
              terraform apply -auto-approve
            '''
          }
        }
      }
    }

    stage('Generate Ansible Inventory') {
      steps {
        script {
          def publicIp = sh(script: "terraform -chdir=terraform output -raw instance_public_ip", returnStdout: true).trim()
          writeFile file: 'inventory.ini', text: """
          ec2-instance ansible_host=${publicIp} ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/id_rsa
          """
        }
      }
    }

    stage('Run Ansible Playbook') {
      steps {
        sh 'ansible-playbook -i inventory.ini ansible/playbook.yml'
      }
    }
  }
}

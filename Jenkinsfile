pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Ansible_terraform_jenkins', url: 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir('terraform') {
                    withEnv(["AWS_ACCESS_KEY_ID=${env.AWS_ACCESS_KEY_ID}", 
                             "AWS_SECRET_ACCESS_KEY=${env.AWS_SECRET_ACCESS_KEY}"]) {
                        sh '''
  terraform init
  terraform apply -auto-approve \
    -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
    -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}"
'''

                    }
                }
            }
        }

        stage('Generate Ansible Inventory') {
            steps {
                script {
                    def publicIp = sh(
                        script: 'terraform -chdir=terraform output -raw ec2_public_ip',
                        returnStdout: true
                    ).trim()

                    writeFile file: 'ansible/inventory.ini', text: """[web]
${publicIp} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
"""
                }
            }
        }

        stage('Ansible Playbook') {
            steps {
                sshagent (credentials: ['ansible-key']) {
                    sh '''
                        ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
                    '''
                }
            }
        }
    }
}

pipeline {
    agent any

    environment {
        TF_DIR = "terraform"
        ANSIBLE_DIR = "ansible"
        SSH_KEY = credentials('jenkins-ssh-key') // ID of your SSH key in Jenkins credentials
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/shivamsingh163248/Health_privacy_app.git'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                dir("${TF_DIR}") {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Fetch EC2 IP') {
            steps {
                script {
                    def ec2_ip = sh(
                        script: "cd ${TF_DIR} && terraform output -raw ec2_public_ip",
                        returnStdout: true
                    ).trim()
                    env.EC2_PUBLIC_IP = ec2_ip
                }
            }
        }

        stage('Configure Server with Ansible') {
            steps {
                dir("${ANSIBLE_DIR}") {
                    // Create inventory
                    writeFile file: 'inventory.ini', text: """[web]
${env.EC2_PUBLIC_IP} ansible_user=ubuntu ansible_ssh_private_key_file=${env.SSH_KEY}"""

                    // Run playbook
                    sh 'ansible-playbook -i inventory.ini playbook.yml'
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed."
        }
    }
}

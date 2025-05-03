#!/bin/bash

echo "🚀 Running Terraform..."
cd terraform
terraform init
terraform apply -auto-approve

PUBLIC_IP=$(terraform output -raw ec2_public_ip)

echo "🌍 EC2 Public IP: $PUBLIC_IP"
cd ../ansible

echo "🛠️  Creating inventory..."
echo "[web]" > inventory.ini
echo "$PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa" >> inventory.ini

echo "📦 Running Ansible playbook..."
ansible-playbook -i inventory.ini playbook.yml

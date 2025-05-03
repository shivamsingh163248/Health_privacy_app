provider "aws" {
  region     = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_security_group" "docker_sg" {
  name        = "docker-sg"
  description = "Allow HTTP inbound traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "docker_server" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.docker_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install docker.io -y
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              newgrp docker

              docker pull shivamsingh163248/health_privacy_app:v2
              docker run -d -p 80:3000 shivamsingh163248/health_privacy_app:v2
              EOF

  tags = {
    Name = "Docker-Health-App-Server"
  }
}

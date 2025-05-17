provider "aws" {
  region     = "us-east-1"
  # Uncomment the following lines if you want to use access and secret keys directly
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_key_pair" "deployer" {
  key_name   = "shivam-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Make sure this file exists
}

resource "aws_security_group" "docker_sg" {
  name        = "docker-sg"
  description = "Allow SSH, HTTP, and App inbound traffic"

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow App Port (3000)"
    from_port   = 3000
    to_port     = 3000
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
  ami                         = "ami-0c7217cdde317cfec"
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.deployer.key_name
  vpc_security_group_ids      = [aws_security_group.docker_sg.id]

  tags = {
    Name = "Docker-Health-App-Server"
  }
}

output "ec2_public_ip" {
  value       = aws_instance.docker_server.public_ip
  description = "Public IP of your EC2 instance"
}

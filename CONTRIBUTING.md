Health_privacy_app
Deploy Health Privacy App on Ubuntu EC2 Instance

This guide walks you through setting up an EC2 Ubuntu server, installing Docker, running the Health Privacy App, and making it accessible via the public IP.
Step 1: Connect to EC2 Instance

Use SSH to connect to your EC2 instance:

ssh -i your-key.pem ubuntu@your-ec2-public-ip

    Replace your-key.pem with your private key file, and your-ec2-public-ip with your EC2 public IP address.

Step 2: Install Docker

Once logged into the server, install Docker by running the following commands:

sudo apt update
sudo apt install docker.io -y

Start and enable the Docker service:

sudo systemctl start docker
sudo systemctl enable docker

Give the ubuntu user permission to run Docker without sudo:

sudo usermod -aG docker ubuntu

    Important: After running the above command, you need to logout and login again for the group changes to take effect:

exit

Then re-login:

ssh -i your-key.pem ubuntu@your-ec2-public-ip

Step 3: Pull the Docker Image

Now, pull the Docker image for the Health Privacy App:

docker pull shivamsingh163248/health_privacy_app:v2

Step 4: Run the Docker Container

Run the container, exposing it to port 80 on the EC2 instance:

docker run -d -p 80:6000 shivamsingh163248/health_privacy_app:v2

    -d : Run the container in detached mode (background)
    -p 80:3000 : Map port 80 of the EC2 instance to port 6000 of the container

Step 5: Configure Security Group

In the AWS Management Console:

    Navigate to EC2 Dashboard → Instances.
    Select your running EC2 instance.
    Go to Security → Security Groups.
    Click Edit Inbound Rules.
    Add a new rule:
        Type: HTTP
        Protocol: TCP
        Port Range: 80
        Source: Anywhere (0.0.0.0/0) or restrict to your IP if needed.

    If your application uses another port (e.g., 3000, 8000, 8080), make sure to allow that port as well.

Step 6: Test the Application

Open your browser and visit:

http://your-ec2-public-ip/

You should see the Health Privacy App running! 🎉
Notes

    Ensure that your Docker container is properly listening on port 3000 inside the container.
    Always secure your EC2 instance by limiting access (for production environments).
    Monitor and manage your Docker containers using:

docker ps
docker logs <container_id>
docker stop <container_id>
docker rm <container_id>

Author

Maintained by shivamsingh163248

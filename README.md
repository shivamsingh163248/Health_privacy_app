
# Health_privacy_app

# Deploy Health Privacy App on Ubuntu EC2 Instance

This guide walks you through setting up an EC2 Ubuntu server, installing Docker, running the Health Privacy App, and making it accessible via the public IP.

---

## Step 1: Connect to EC2 Instance

Use SSH to connect to your EC2 instance:

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

> Replace `your-key.pem` with your private key file, and `your-ec2-public-ip` with your EC2 public IP address.

---

## Step 2: Install Docker

Once logged into the server, install Docker by running the following commands:

```bash
sudo apt update
sudo apt install docker.io -y
```

Start and enable the Docker service:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Give the `ubuntu` user permission to run Docker without `sudo`:

```bash
sudo usermod -aG docker ubuntu
```

> **Important:** After running the above command, you need to **logout** and **login again** for the group changes to take effect:

```bash
exit
```
Then re-login:

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

---

## Step 3: Pull the Docker Image

Now, pull the Docker image for the Health Privacy App:

```bash
docker pull shivamsingh163248/health_privacy_app:v2
```

---

## Step 4: Run the Docker Container

Run the container, exposing it to port 80 on the EC2 instance:

```bash
docker run -d -p 80:6000 shivamsingh163248/health_privacy_app:v2
```

- `-d` : Run the container in detached mode (background)
- `-p 80:3000` : Map port 80 of the EC2 instance to port 6000 of the container

---

## Step 5: Configure Security Group

In the AWS Management Console:

1. Navigate to **EC2 Dashboard** → **Instances**.
2. Select your running EC2 instance.
3. Go to **Security** → **Security Groups**.
4. Click **Edit Inbound Rules**.
5. Add a new rule:
   - **Type**: HTTP
   - **Protocol**: TCP
   - **Port Range**: 80
   - **Source**: Anywhere (`0.0.0.0/0`) or restrict to your IP if needed.

> If your application uses another port (e.g., 3000, 8000, 8080), make sure to allow that port as well.

---

## Step 6: Test the Application

Open your browser and visit:

```
http://your-ec2-public-ip/
```

You should see the Health Privacy App running! 🎉

---

# Notes

- Ensure that your Docker container is properly listening on port **3000** inside the container.
- Always secure your EC2 instance by limiting access (for production environments).
- Monitor and manage your Docker containers using:

```bash
docker ps
docker logs <container_id>
docker stop <container_id>
docker rm <container_id>
```

---

# Author

Maintained by [shivamsingh163248](https://hub.docker.com/u/shivamsingh163248)

# 🛡️ Health Privacy App - Docker Setup Guide

This guide walks you through building and running the Health Privacy App using Docker on a Windows system.

---

## ✅ Step-by-Step (On Windows PowerShell or CMD)

---

### 🔧 1. Open PowerShell (or CMD) and Navigate to Your Project Folder

```bash
cd path\to\your\Health_privacy_app
```

Replace `path\to\your\Health_privacy_app` with the actual path to your project directory.

---

### 🔨 2. Build the Docker Image

```bash
docker build -t health_privacy_app .
```

**Explanation:**

* `-t` tags your image with a name (`health_privacy_app`)
* `.` tells Docker to use the `Dockerfile` in the current directory

---

### 🚀 3. Run the Docker Container

```bash
docker run -d -p 3000:3000 --name health_app_container health_privacy_app
```

**Explanation:**

* `-d`: Run in detached mode (background)
* `-p 3000:3000`: Maps port 3000 on your host to port 3000 in the container
* `--name health_app_container`: Gives your container a name
* `health_privacy_app`: Name of the Docker image you built

---

### 🌐 4. Access the Flask App in Your Browser

Open your browser and go to:

```
http://localhost:3000
```

---

### 🧲 5. Check Running Containers

To check if the container is running:

```bash
docker ps
```

To view logs (helpful for debugging):

```bash
docker logs health_app_container
```

---

### 🚩 6. Stop and Remove the Container (Optional)

To stop the container:

```bash
docker stop health_app_container
```

To remove the container:

```bash
docker rm health_app_container
```

---

### 📝 Bonus Tips

Make sure your `app.py` runs the Flask server on all available network interfaces:

```python
app.run(host="0.0.0.0", port=3000)
```

This is required so that Docker can bind to port 3000 properly from outside the container.

---

## 🔗 Source

GitHub Repo: [shivamsingh163248/Health\_privacy\_app](https://github.com/shivamsingh163248/Health_privacy_app)


# 🛡️ Health Privacy App - Docker Setup Guide

This guide walks you through building and running the Health Privacy App using Docker on a Windows system.

---

## ✅ Step-by-Step (On Windows PowerShell or CMD)

---

### 🔧 1. Open PowerShell (or CMD) and Navigate to Your Project Folder

```bash
cd path\to\your\Health_privacy_app
```

Replace `path\to\your\Health_privacy_app` with the actual path to your project directory.

---

### 🔨 2. Build the Docker Image

```bash
docker build -t health_privacy_app .
```

**Explanation:**

* `-t` tags your image with a name (`health_privacy_app`)
* `.` tells Docker to use the `Dockerfile` in the current directory

---

### 🚀 3. Run the Docker Container

```bash
docker run -d -p 3000:3000 --name health_app_container health_privacy_app
```

**Explanation:**

* `-d`: Run in detached mode (background). Without `-d`, the app runs in foreground, and you'll see logs. If the container is interrupted (Ctrl+C), it stops and app becomes inaccessible.
* `-p 3000:3000`: Maps port 3000 on your host to port 3000 in the container
* `--name health_app_container`: Gives your container a name
* `health_privacy_app`: Name of the Docker image you built

---

### 🌐 4. Access the Flask App in Your Browser

Open your browser and go to:

```
http://localhost:3000
```

---

### 🧲 5. Check Running Containers

To check if the container is running:

```bash
docker ps
```

To view logs (helpful for debugging):

```bash
docker logs health_app_container
```

---

### 🚩 6. Stop and Remove the Container (Optional)

To stop the container:

```bash
docker stop health_app_container
```

To remove the container:

```bash
docker rm health_app_container
```

---

### 📝 Bonus Tips

Make sure your `app.py` runs the Flask server on all available network interfaces:

```python
app.run(host="0.0.0.0", port=3000)
```

This is required so that Docker can bind to port 3000 properly from outside the container.

---

## 📦 Docker Compose Setup (Optional)

Create a `docker-compose.yml` file in the root of your project:

```yaml
version: '3.8'

services:
  health_app:
    build: .
    ports:
      - "3000:3000"
    container_name: health_app_container
```

Then run:

```bash
docker-compose up -d
```

To stop and remove:

```bash
docker-compose down
```

---

## 📤 Push to Docker Hub

1. **Login to Docker Hub**:

```bash
docker login
```

2. **Tag your image**:

```bash
docker tag health_privacy_app your_dockerhub_username/health_privacy_app
```

3. **Push the image**:

```bash
docker push your_dockerhub_username/health_privacy_app
```

---

## 🖼️ GitHub Badges

Add these at the top of your README for project visibility:

```markdown
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9-blue?logo=python)
```

---

## 🔗 Source

GitHub Repo: [shivamsingh163248/Health\_privacy\_app](https://github.com/shivamsingh163248/Health_privacy_app)


# 🛡️ Health Privacy App - Docker Setup Guide

This guide walks you through building and running the Health Privacy App using Docker on a Windows system.

---

![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9-blue?logo=python)
![Docker Pulls](https://img.shields.io/docker/pulls/shivamsingh163248/health_privacy_app?style=flat-square)

---

## ✅ Step-by-Step (On Windows PowerShell or CMD)

### 🔧 1. Open PowerShell (or CMD) and Navigate to Your Project Folder

```bash
cd path\to\your\Health_privacy_app
```

Replace `path\to\your\Health_privacy_app` with the actual path to your project directory.

### 🔨 2. Build the Docker Image

```bash
docker build -t health_privacy_app .
```

### 🚀 3. Run the Docker Container

```bash
docker run -d -p 3000:3000 --name health_app_container health_privacy_app
```

### 🌐 4. Access the Flask App in Your Browser

```
http://localhost:3000
```

### 🧲 5. Check Running Containers

```bash
docker ps
```

### 🚩 6. Stop and Remove the Container (Optional)

```bash
docker stop health_app_container

docker rm health_app_container
```

### 📝 Bonus Tips

Make sure your `app.py` runs the Flask server on all available network interfaces:

```python
app.run(host="0.0.0.0", port=3000)
```

---

## 📦 Docker Compose Setup (Optional)

```yaml
version: '3.8'

services:
  health_app:
    build: .
    ports:
      - "3000:3000"
    container_name: health_app_container
```

```bash
docker-compose up -d

docker-compose down
```

---

## 📤 Push to Docker Hub

```bash
docker login

docker tag health_privacy_app shivamsingh163248/health_privacy_app

docker push shivamsingh163248/health_privacy_app
```

---

## ⚙️ CI/CD Integration

### 🔁 GitHub Actions

Create `.github/workflows/docker.yml`:

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v2

    - name: Log in to Docker Hub
      run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin

    - name: Build Docker Image
      run: docker build -t shivamsingh163248/health_privacy_app .

    - name: Push Docker Image
      run: docker push shivamsingh163248/health_privacy_app
```

Add secrets in your repo: `DOCKER_USERNAME`, `DOCKER_PASSWORD`

### 🔁 Jenkins Pipeline Example (Jenkinsfile)

```groovy
pipeline {
  agent any

  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/shivamsingh163248/Health_privacy_app.git'
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
          docker.build("shivamsingh163248/health_privacy_app")
        }
      }
    }
    stage('Push to Docker Hub') {
      steps {
        withDockerRegistry([ credentialsId: 'dockerhub-credentials', url: '' ]) {
          script {
            docker.image("shivamsingh163248/health_privacy_app").push()
          }
        }
      }
    }
  }
}
```

---

## 🖼️ Architecture Diagram

![App Architecture](https://raw.githubusercontent.com/shivamsingh163248/Health_privacy_app/main/assets/architecture.png)

This shows the container-based deployment architecture for the Health Privacy App.

> Note: Make sure to upload your `architecture.png` under an `assets` folder in your GitHub repo.

---

## 🔗 Source

GitHub Repo: [shivamsingh163248/Health\_privacy\_app](https://github.com/shivamsingh163248/Health_privacy_app)


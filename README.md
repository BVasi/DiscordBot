# DiscordBot

## How to Run the Application Using Docker

### 1. Clone or Download the Repository
```git clone <repository-url>```
```cd <application-folder>```

### 2. Build the Docker Image
```docker build -t discord-bot .```

### 3. Run the Docker Container
```docker run --name discord-bot-container -d discord-bot```

### 4. View the Bot's Logs
```docker logs -f discord-bot-container```

### Stop the Container
```docker stop discord-bot-container```

### Delete the Container
```docker rm discord-bot-container```

# Useful Docker Commands:

### Build a Docker image from the Dockerfile in the current directory
```docker build -t <image-name> .```

### Run a Docker container from the created image
```docker run --name <container-name> -d <image-name>```

### List all Docker containers (including stopped ones)
```docker ps -a```

### Show logs of a running Docker container
```docker logs -f <container-name>```

### Stop a running Docker container
```docker stop <container-name>```

### Remove a stopped container
```docker rm <container-name>```

### Remove a Docker image
```docker rmi <image-name>```

### Remove all stopped containers
```docker container prune```

### Remove all unused images, containers, volumes, and networks
```docker system prune -a```

### Remove all Docker containers (running or stopped)
```docker container rm -f $(docker ps -aq)```

### View all Docker images
```docker images```

### List all volumes used by Docker containers
```docker volume ls```

### Remove a Docker volume
```docker volume rm <volume-name>```

### Clean up unused Docker volumes
```docker volume prune```

### Get detailed information about a container
```docker inspect <container-name>```

### Enter a running container and execute commands interactively
```docker exec -it <container-name> /bin/bash```

### Build a Docker image from a specific Dockerfile
```docker build -f <Dockerfile-path> -t <image-name> .```

### Tag an image with a new name
```docker tag <image-name> <new-tag>```

### Check Docker version
```docker --version```

### Check the status of Docker service
```systemctl status docker```
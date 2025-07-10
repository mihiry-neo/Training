# Linux System

This repository documents my hands-on practice with fundamental Linux system administration concepts, commands, and use cases using **Ubuntu on WSL2**. It includes permission management, user/group handling, linking, archiving, package/process/service management, and more.

---

## File & Directory Permissions

### Basic Commands
```bash
ls -l               # List permissions
chmod 555 testdir   # Read & execute only for all
chmod 644 file.txt  # rw-r--r--
chmod 400 test.txt  # Read-only
chmod 111 demo.txt  # Execute-only
chgrp users file    # Change group ownership
```

### Umask
```bash
umask               # Check default mask
umask 022           # Set default permission mask
```

---

## User & Group Management

### Creating Users and Groups
```bash
sudo adduser devuser1
sudo groupadd users
sudo usermod -aG users devuser1
```

### Checking Group Info
```bash
groups              # Current user groups
id <username>       # UID, GID, groups
```

---

## Directory Access by Other Users

### Scenario
- Created `demodir/demo.txt` with group write permissions.
- Allowed `devuser1` (part of `users`) to modify it.

```bash
sudo chgrp users demo.txt
sudo chmod 664 demo.txt
sudo chmod 770 demodir
sudo chmod o+x /home/mihir_neo
```

---

## Hard Links vs Soft Links

### Creation
```bash
ln original.txt hardlink.txt      # Hard link
ln -s original.txt softlink.txt   # Soft (symbolic) link
```

### Observations
- **Hard link** shares inode & data (stat: same inode).
- **Soft link** is a separate file pointing to original.

### Testing
- Modify original → both reflect changes.
- Delete original → softlink breaks, hardlink survives.

---

## Archiving & Compression

### Create Archive
```bash
tar -cvf archive.tar file1 file2
```

### Extract
```bash
tar -xvf archive.tar
```

### Gzip Compression
```bash
tar -cvzf archive.tar.gz dir/
```

### Preserve Symlinks
```bash
tar -cvhf archive.tar original.txt softlink.txt
```

---

## Backup Config Using Symlink
```bash
ln -s /etc/hostname ~/config_backup.conf
nano ~/config_backup.conf     # Editing this reflects on /etc/hostname
```

---

## Package Management (APT)

```bash
sudo apt update              # Refresh repositories
sudo apt install curl        # Install package
sudo apt remove curl         # Remove (keep config)
sudo apt purge curl          # Remove with config
sudo apt list --installed    # List packages
```

> To view config files before purge:  
> Check `/etc`, `/var/lib`, `/usr/share/doc/<package>/`

---

## Process and Service Management

### View Processes
```bash
ps aux
```

### Kill Process
```bash
kill <PID>
```

### Manage Services
```bash
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>
sudo systemctl status <service>
```

---

## File System Exploration & Tips

```bash
ls /home                 # View all users' home dirs
ls /mnt                  # View Windows mount points (WSL)
cd /mnt/c/...            # Access Windows files
```

## Demo Files Used

| File/Dir       | Purpose                        |
|----------------|--------------------------------|
| `demodir/`     | Shared dir with group access   |
| `demo.txt`     | Group-editable file            |
| `original.txt` | Base file for link testing     |
| `hardlink.txt` | Hard link (inode shared)       |
| `softlink.txt` | Symlink (path-based pointer)   |
| `archive.tar`  | Compressed archive demo        |


# Docker Hands-on Practice - Summary Report

## Docker Concepts Practiced

| Concept        | Explanation                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| Image          | Read-only template used to create containers (e.g., OS + App + Dependencies)|
| Container      | Runnable instance of an image with isolated environment                     |
| Docker Hub     | Central registry for container images                                       |

---

## Commands Practiced with Results

### Image Management

```bash
docker pull hello-world
docker pull ubuntu
docker pull mysql
docker pull mysql:8.0
```

### Container Management

```bash
docker run hello-world
docker run -it ubuntu
docker run -d -e MYSQL_ROOT_PASSWORD=secret --name mysql-newer mysql
docker run -d -e MYSQL_ROOT_PASSWORD=secret --name mysql-older mysql:8.0
```

### Useful Docker Flags

| Flag                     | Purpose                                                       |
| ------------------------ | ------------------------------------------------------------- |
| `-d`                     | Detached mode (runs in background)                            |
| `-it`                    | Interactive terminal (useful for Ubuntu shell)                |
| `--name`                 | Assign custom name to container                               |
| `-p <host>:<container>`  | Port mapping between host and container                       |
| `-e`                     | Set environment variable (used for passwords, configs, etc.)  |

### Container Logs & Access

```bash
docker ps -a               # List all containers
docker ps                  # List running containers
docker logs <name/id>      # View logs
docker exec -it <id> bash  # Interact with running container
```

### Cleanup & Deletion

```bash
docker stop <id/name>
docker rm <id/name>
docker rmi <image-id>
```

---

## Learnings

- Docker containers provide isolated, portable environments.
- Docker images are layered; base layers are shared across versions.
- When running MySQL containers, port binding (`-p`) is critical to avoid conflicts.
- Use `docker exec -it` for interacting with live containers (e.g., bash shell).
- Images cannot be deleted if a container (even stopped) is still using them.
- `docker run` always creates a **new container**; use `docker start` to restart an **existing one**.
- Environment variables (`-e`) are necessary for apps like MySQL to work (e.g., root password).

---

## Real-World Data Engineering Applications

1. **Tool Isolation**:  
   Run Apache Spark, Kafka, Hadoop, PostgreSQL, MongoDB in isolated containers.

2. **Pipeline Development**:  
   Develop and test ETL/ELT pipelines inside containers (Airflow, Spark, Pandas, etc).

3. **Reproducibility**:  
   Share consistent containerized environments across teams/dev/stage/prod.

4. **Integration Testing**:  
   Validate end-to-end data flow by simulating all components via Docker.

5. **Cloud Deployment**:  
   Deploy containers to AWS ECS, Azure Containers, Kubernetes, etc.

6. **Version Control & Backup**:  
   Store versioned images in Docker Hub or AWS ECR.

7. **Kubernetes Ready**:  
   Docker containers are the base units for Kubernetes orchestration.

---

## Key Notes

- `docker pull image:tag` helps in using specific versions (e.g., `mysql:8.0`)
- `docker start <name>` doesn't print output unless container runs in attached mode or has logs.
- Avoid using the same port (e.g., `-p 8080:3306`) for multiple containers.
- CMD and Docker Daemon are separate: CMD is client, Docker Engine is the service.
- `docker start -a <container>` shows output of a previously exited container.
- Deleted all old containers and images successfully before final setup.

---

## Verification Outputs

- Ran `hello-world` successfully — confirmed Docker is working.
- Ran interactive Ubuntu container and created files inside it.
- Verified environment variables and file structure inside MySQL container.
- Tested port conflicts and resolved using different host ports.
- Cleaned up all stopped containers and unused images.


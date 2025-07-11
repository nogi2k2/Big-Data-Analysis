# System Setup Guide

This guide provides step-by-step instructions for setting up the required environment for the Steam Games data analysis pipeline.

**Note:** Replace `<user-name>` in commands with your actual system username.

## Prerequisites

This setup is designed for Ubuntu/WSL2 environments. Ensure you have administrative privileges.

## Installation Steps

### 1. Update System Packages

```bash
sudo apt update 
sudo apt upgrade -y
```

### 2. Install OpenSSH Server

```bash
sudo apt install openssh-server
```

### 3. Install Python and Required Packages

```bash
sudo apt install python3 -y
```

**Important:** We install Python packages system-wide using `apt` rather than `pip` or virtual environments due to the following constraints:

- **WSL File System Issues:** pip in WSL attempts to write to `/mnt/` paths mounted from Windows, which don't fully support Linux-style file permissions and temporary file operations
- **Externally Managed Environment:** Modern Ubuntu distributions prevent system-wide pip installations to avoid conflicts

Install required Python packages:
```bash
sudo apt install python3-pyspark
sudo apt install python3-pandas
sudo apt install python3-numpy
```

### 4. Install OpenJDK 8

```bash
sudo apt install openjdk-8-jdk -y
```

### 5. Download and Install Hadoop 3.4.1

Create installation directory:
```bash
sudo mkdir -p /opt/hadoop
cd /opt/hadoop
```

Download and extract Hadoop:
```bash
sudo wget https://archive.apache.org/dist/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz
sudo tar -xzf hadoop-3.4.1.tar.gz
sudo mv hadoop-3.4.1/* .
sudo rm hadoop-3.4.1.tar.gz
```

Set ownership:
```bash
sudo chown -R $USER:$USER /opt/hadoop
```

### 6. Download and Install Spark 3.4.1

Create Spark directory:
```bash
sudo mkdir -p /opt/spark
cd /opt/spark
```

Download and extract Spark:
```bash
sudo wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
sudo tar -xzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3/* .
sudo rm spark-3.4.1-bin-hadoop3.tgz
```

Set ownership:
```bash
sudo chown -R $USER:$USER /opt/spark
```

**Configure hostname mapping:**
Edit `/etc/hosts` to add your hostname:
```bash
sudo nano /etc/hosts
```

Add the following line (replace with your actual hostname):
```
127.0.0.1 LAPTOP-8JQG56KU.localdomain
```

**To find your hostname:**
- Check Spark Master UI at `spark://localhost:8080`
- Or check Spark logs: `tail -n 30 $SPARK_HOME/logs/spark-<user-name>-org.apache.spark.deploy.master.Master-1-*.out`
- Or run: `hostname -f`

### 7. Install MongoDB 7.0

Import MongoDB GPG key:
```bash
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
```

Add MongoDB repository:
```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

Update package list and install MongoDB:
```bash
sudo apt update
sudo apt install -y mongodb-org
```

Start MongoDB service:

**For WSL:**
```bash
sudo service mongod start
```

**For Linux (non-WSL):**
```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 8. Configure Environment Variables

Add environment variables to `~/.bashrc`:
```bash
cat >> ~/.bashrc << 'EOF'

# Hadoop Configuration
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Spark Configuration  
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH

# Java Configuration
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

EOF
```

Reload environment variables:
```bash
source ~/.bashrc
```

### 9. Configure Hadoop

On initial installation, Hadoop configuration files are empty and require minimal configuration.

**Configure core-site.xml:**
```bash
nano $HADOOP_HOME/etc/hadoop/core-site.xml
```

Add the following content:
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

**Configure hdfs-site.xml:**
```bash
nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```

Add the following content (replace `<user-name>` with your username):
```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>

  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/<user-name>/hadoopdata/namenode</value>
  </property>

  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///home/<user-name>/hadoopdata/datanode</value>
  </property>
</configuration>
```

### 10. Move Project Files (Optional but Recommended)

Move project files from Windows mount to WSL root for better performance:
```bash
mv /mnt/*/Big-Data-Analysis ~/Big-Data-Analysis
cd ~/Big-Data-Analysis
```

### 11. Start SSH Service

**For WSL:**
```bash
sudo service ssh start
```

**For Linux (non-WSL):**
```bash
sudo systemctl start ssh
sudo systemctl enable ssh  # Optional: auto-start on boot
```

### 12. Enable Passwordless SSH

Hadoop requires passwordless SSH access to localhost:

```bash
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Test SSH access:
```bash
ssh localhost
```

## Verification

After completing the setup, verify that all services are properly configured:

1. **Java:** `java -version`
2. **Hadoop:** `hadoop version`
3. **Spark:** `spark-submit --version`
4. **MongoDB:** `mongod --version`
5. **SSH:** `ssh localhost` (should connect without password)

## Troubleshooting

- **Permission Issues:** Ensure all directories have proper ownership (`chown -R $USER:$USER`)
- **SSH Connection Failed:** Verify SSH service is running and keys are properly configured
- **Hadoop Startup Issues:** Check that JAVA_HOME is properly set and accessible
- **MongoDB Issues:** Ensure MongoDB service is running and listening on default port

## Next Steps

Once setup is complete, proceed to the [Execution Guide](./Docs/exec/Execution.md) to run the data analysis pipeline.
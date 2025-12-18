#### Prototype Cloud SQL setup
Region = us-central1 (Iowa)
DB Version = MySQL 8.4.7
Machine type = db-f1-micro
vCPUs = 1 vCPU
RAM =628.74 MB
Data Cache = Disabled
Storage = 10 GB SSD
Connections = Public IP
Backup = Automated
Availability = Single zone
Point-in-time recovery = Enabled
Network throughput (MB/s)  = 125 of 125
IOPS 
 - Read: 6,300 of 12,000
 - Write: 6,300 of 10,000
Disk throughput (MB/s) 
 - Read: 4.8 of 125.0
 - Write: 4.8 of 107.8
User accounts
 - root - SQL admin
 - dba - SQL database administrator
 - app_user - SQL application user

#### Prototype Serverless Cloud Run setup
Region = europe-west1 (London)`
Container image = europe-west1-docker.pkg.dev/yatzaahi2025/cloud-run-source-deploy/python504@sha256:c9d2e302d8466a6064e3fa6ecc74ed9c3a078ec2bac85a6e851be527691b2e84
Billing = Request-based
Memory = 512 MB
CPU = 1 vCPU
Timeout = 240 seconds
Request Timeout = 30 seconds
Min Instances = 0
Max Instances = 2
Max Concurrent Instances = 5
Cloud SQL connection = yatzaahi2025:us-central1:gcp-mysql
Port = 8080
Set up With Developer Connect = Yes
Enable continued deployment = Yes
Set Environment Variables with Secrets for DB connection
 - DB_APP_USERNAME
 - DB_APP_PASSWORD
 - DB_DATABASE
 - DB_HOSTNAME
 - DB_PORT
 - HUGGINGFACE_API_KEY
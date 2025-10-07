Flask on Cloud VM (Assignment 2)
Student Info
Name: y0y0l0

Cloud Provider: Google Cloud Platform (GCP)
Video recording:
Zoom:
## Learning goals
- Create a VM on a cloud provider (GCP_Compute Engine)
- Configure the VM 
    - OS: Ubuntu
    - e2-micro instance
- Configure the VM to allow HTTP (80) and HTTPS (443) traffic
- Configure Firewall policies to open custom port 5003
    - Ingress
    - Action on match: yes
    - Source IP ranges: 0.0.0.0/0
- SSH into the VM
- Update the OS
- Install Python, Git, Flask, VENV, and Nano
- Clone a gitHub repo
- Create and activate a virtual environment
- Install Flask, Python, Git, VENV, and Nano using pip and requirements.txt
- Run a simple Flask app on port 5003 via localhost
- Modify the Flask app using gitHub to return "Hello from New York!"
- Access the Flask app via GCP VM public IP
- (Bonus) Access the app via a custom domain name

### Steps
1. VM Creation
[screenshot]

2. Networking (Port 5003 Open)
[screenshot]

3. OS Update + Python Install
[commands + screenshot]

4. Flask App Running
[screenshot of terminal + browser]

5. Public IP Access
URL: http://XX.XX.XXX.XXX:5003
[screenshot]

6. (Bonus) Domain Name
Domain: http://mydomain.tech:5003
[screenshot]
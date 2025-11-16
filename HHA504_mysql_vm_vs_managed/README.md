## Homework: MySQL on VM vs Managed Service (SQLAlchemy + pandas)

### 1) Overview

The goal of the assignment is to provision two MySQL databases on the same cloud: 
(A) a VM you harden and configure yourself, and 
(B) the cloud’s managed MySQL offering. You will then connect to both using SQLAlchemy in Python, create a new database and table with pandas, insert data, and read it back. You will document steps, timing, and the differences in setup effort and operational friction.


**Managed service names by cloud**
* **GCP:** Cloud SQL for MySQL

**VM services by cloud**
* **GCP:** Compute Engine
---

### 2) Learning Objectives

* Contrast operational tasks between self-managed and managed MySQL.
* Configure network access, and users.
* Use SQLAlchemy to connect, create a database/table, and round-trip data with pandas.
* Capture evidence (screens/notes) and compare time-to-first-query and setup difficulty.

**Additional lessons learned include:**
- Python & SQLAlchemy - Connection strings, database engines, SSL configuration
- MySQL - User permissions, database creation, remote access, authentication methods
- GCP (Google Cloud Platform) - Firewall rules, VM management, networking
- Debugging - Reading error messages, identifying root causes, iterating on solutions
- Environment configuration - Using .env files, loading environment variables
- Problem-solving - Troubleshooting connection issues, permission problems, and deprecation warnings
---
### 3) Packages that you will use: 

* Inside of your requirements will need: `sqlalchemy`, `pymysql` , `pandas`, `python-dotenv`, `os`, `timezone`, and `datetime`.
---

### 4) Repository & Deliverables

Create a repo named **`HHA504_mysql_vm_vs_managed`** with this structure:

```
HHA504_mysql_vm_vs_managed/
├─ README.md
├─ .gitignore                  # Make sure to ignore your .env 
├─ .env.example                # Do NOT commit real secrets
├─ scripts/
│   ├─ vm_demo.py              # SQLAlchemy+pandas against VM MySQL
│   └─ managed_demo.py         # SQLAlchemy+pandas against managed MySQL
├─ sql/
│   └─ init.sql                # Optional: user/db bootstrap you ran on VM
├─ screenshots/
│   ├─ vm/                     # VM portal, firewall, daemon status, CLI, etc.
│   └─ managed/                # Managed service creation, connection details
└─ docs/
    ├─ setup_notes_vm.md        # VM detailed ordered steps, troubles, timing, and lessons learned
    ├─ setup_notes_managed.md   # Managed detailed ordered steps, troubles, timing, and lessons learned
    └─ comparison.md           # timing & difficulty comparison
```

**Deliverables (must be in `main`):**

* `README.md` with:

  * Cloud chosen and region
  * Public high-level steps to reproduce (bullets)
  * Connection string patterns (no secrets), and how you stored secrets locally
  * Screenshots summary and links

* `scripts/vm_demo.py` and `scripts/managed_demo.py` that (you can just copy and paste the provided files, and or modify them as you like):

  1. Read credentials from environment (`.env`)
  2. Connect to MySQL via SQLAlchemy
  3. Create a new database (e.g., `dummydb`) if not exists
  4. Create a table (e.g., `visits`) via pandas `to_sql`
  5. Insert 5–10 rows from a pandas DataFrame
  6. Read back with `pd.read_sql` and print row count

* `docs/setup_notes_vm.md` and `docs/setup_notes_managed.md`:
  * Ordered steps you executed, with command snippets
  * Any config files you edited (e.g., `mysqld.cnf`), with the exact lines
  * Troubles you hit and how you solved them
  * **Start-to-finish elapsed time** (minutes) measured by you
* `docs/comparison.md`:
  * A short paragraph on which you would choose in production and why
* `screenshots/` evidence:
  * VM: portal/console creation page, package install, service status, firewall rules/security group, MySQL prompt proving DB/table exist, and a local or bastion test
  * Managed: creation wizard summary, connection info, authorized networks/VPC, connectivity test, metrics/overview page
* 2–4 minute **recording** (Zoom/Loom link in README) showing:
  * Running each script end-to-end (VM then Managed) and printed results
  * gcp managed demo video link: https://youtu.be/jpHw5lkVvnI
  * gcp vm demo video link:
   * part1 - setup: https://youtu.be/KlOV_1sI0HE
   * part2 - test/validation: https://youtu.be/Gfcjod2mUTE
---

### 5) Task A — MySQL on a VM (Self-managed)

1. **Provision VM**

   * OS: Ubuntu LTS or Oracle Linux
   * Instance type: small (e.g., 1–2 vCPU, 2–4 GB RAM)
   * Open **TCP ports 22 and 3306** 
2. **Install & Configure MySQL**

   * Install server packages; enable and start service.
   * Set strong root password (or auth plugin).
   * Edit `mysqld.cnf` (bind-address), restart service.
   * Configure firewall/security group rules minimally; note your choices in `setup_notes_vm.md`.

3. **Test Locally or Inside of Cloud Console (VS Code in GCP) environment **
   * `mysql -u <user> -p -h 127.0.0.1 -P 3306` from VM
   * Optional: set up an SSH tunnel from your dev machine instead of opening 3306 publicly.
---

### 6) Task B — Managed MySQL

Create the provider’s managed MySQL with a small tier. Capture:

* Engine version, Enterprise tier sandbox/basic
* Region, zone, availability (single/multi)
* Network model (public IP allowlist = 0.0.0.0/0)
* Initial admin user, DB name
* Any automatic backups/HA configuration chosen

---

### 7) Python: SQLAlchemy + pandas Template

Create a `.env` (do **not** commit) from `.env.example`:
```
# VM
VM_USERNAME=dba
VM_PASSWORD=dba2025
VM_TABLE_NAME=visits
VM_HOSTNAME=35.222.61.81
VM_PORT=3306
VM_DATABASE=dummydb
VM_TEST_QUERY="SELECT COUNT(*) AS n_rows FROM visits;"

MAN_USERNAME=dba
MAN_PASSWORD=Dbaadmin2025!
MAN_TABLE_NAME=visits
MAN_HOSTNAME=34.132.117.17
MAN_PORT=3306
MAN_DATABASE=dummydb
MAN_TEST_QUERY="SELECT COUNT(*) AS n_rows FROM visits;"
```

**Connection URL patterns** (choosen driver for this project is PyMySQL):
* PyMySQL: `mysql+pymysql://USER:PASS@HOST:PORT/DBNAME`
* mysqlclient: `mysql+mysqldb://USER:PASS@HOST:PORT/DBNAME`
**Snippet (adapt for vm vs managed):**
```python
#Managed example
import pandas as pd
import time
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # This will automatically load from .env file
sql_username = os.getenv("MAN_USERNAME")
sql_password = os.getenv("MAN_PASSWORD")
sql_hostname = os.getenv("MAN_HOSTNAME")
sql_database = os.getenv("MAN_DATABASE")
sql_port = os.getenv("MAN_PORT")
sql_test_query = os.getenv("MAN_TEST_QUERY")

server_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}"
```
```python
# VM example
import pandas as pd
import time
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # This will automatically load from .env file
sql_username = os.getenv("VM_USERNAME")
sql_password = os.getenv("VM_PASSWORD")
sql_hostname = os.getenv("VM_HOSTNAME")
sql_database = os.getenv("VM_DATABASE")
sql_port = os.getenv("VM_PORT")
sql_test_query = os.getenv("VM_TEST_QUERY")

server_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}"
```

**Notes**

* You must use a public IP (for demo):
  * VM: open port 3306 in firewall/security group bind-address 0.0.0.0
  * Managed: add your dev machine IP or 0.0.0.0/0 to allow all IPs
---

### 8) What to Capture (Screenshots)

* **VM path:** VM creation summary, security group/firewall, MySQL install + `systemctl status mysql`, `mysql --version`, `mysql` prompt showing `SHOW DATABASES;` and your DB/table present.
[VM setup document](../docs/setup_notes_vm.md)
---
* **Managed path:** service creation summary, connection endpoints, network/authorized list, and a simple query window or metrics page.
[Managed setup document](../docs/setup_notes_managed.md)
* **Python runs:** terminal output of each script printing row counts, plus your environment layout (no secrets).
- VM demo script run
- Managed demo script run
![Managed demo script run](../screenshots/managed/vscode_managed_demo_successful_connection.png)
---
---
### 9) Comparison

Write approximately 200-400 words concluding which you’d choose in production for: (a) a small student app; (b) a departmental analytics DB; (c) a HIPAA-aligned workload (assume a BAA is available in your cloud).
[Comparison](../docs/comparison.md)
---

---
### 10) Safety & Clean-up

* Delete public ingress rules you created.
* Stop or delete the VM and managed instance after you finish to avoid costs.
---
Upon connecting to the VM, I ensured that all necessary packages were installed and configured properly. This included setting up the MySQL server, creating the required databases and tables, and verifying that the environment variables were correctly loaded from the .env file.
1. **Set Up GCP VM**
    * Create a new VM instance in GCP.
        - use a small machine type (e.g., emicro) to minimize costs.
        - select Ubuntu-minimal as the operating system.
        - enable firewall rules to allow traffic for SSH (default port 22) and MySQL port (default 3306).
        - Connect to the VM using SSH.
    * Install MySQL server and client.
    ```bash
    sudo apt-get update
    sudo apt install nano mysql-server mysql-client -y
    ```
     - configured bind-address in MySQL configuration to allow remote connections.
     ```bash
     sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
     ```
    - Changed `bind-address` from `127.0.0.1` to `0.0.0.0` to allow remote connections.
    - Changed 'mysqlbind-address' from `127.0.0.1` to `0.0.0.0` to allow remote connections.
    - restart MySQL service to apply changes.
     ```bash
     sudo systemctl restart mysql
     ```
    - Created a new MySQL admin user and database for the project.
    ```sql
    sudo mysql
    CREATE DATABASE testDb;
    CREATE USER 'dba'@'%' IDENTIFIED BY 'my_password';
    GRANT ALL PRIVILEGES on *.* TO 'dba'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```
    * Start VM instance terminal to connect
    ![GCP VM Instance](../screenshots/vm/gcp_vm_instance.png)
    ![GCP VM Observability](../screenshots/vm/gcp_vm_observability.png)
2. **Install server packages; enable and start service.**
   * Set strong root password (or auth plugin).
   * Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` (bind-address), restart service.
   * Configure firewall/security group rules minimally; note your choices in `setup_notes_vm.md`.
3. **Test Locally VS Code and external Cloud Console (GCP) environment**
    * `mysql -u <user> -p -h <VM_HOSTNAME> -P <VM_PORT> <VM_DATABASE>` from VM opening port 3306
    ![CLI test user connection to VM MySQL database](../screenshots/vm/CLI_test_user_credentials.png)
    * Validate connectivity from VS Code terminal using the same command.
    * Fixed user authentication issues by ensuring the MySQL user had the correct privileges and grant options for remote access:
    - GRANT ALL PRIVILEGES ON `testDb.*` TO 'dba'@'%'; vs GRANT ALL PRIVILEGES on `*.*` TO 'dba'@'%' WITH GRANT OPTION;
    * Encountered and resolved connection issues by checking firewall rules and MySQL user permissions to allow allow remote access.
    ![vscode terminal network connection error](../screenshots/vm/vscode_network_permission_error.png)
    * Address issue with permission problems by granting necessary privileges to the MySQL user to the newly created database.
    * Verified successful connection and data operations using SQLAlchemy in Python.
    * Confirmed the database and table creation, data insertion, and retrieval using pandas was successful by printing the results count to the console.
    * Address issued SSL configuration warnings by explicitly setting the SSL parameter to False in the SQLAlchemy connection string.
    * Resolved utcnow() deprecation warnings by updating the python code to use datetime.now(timezone.utc) instead of utcnow() for timestamp fields.
    ![vscode utcnow deprecation warning](../screenshots/vm/vscode_utcnow_deprecation_warning.png)
     ![vscode managed demo successful connection](../screenshots/vs/vscode_vs_demo_successful_connection.png)
    * Installed the required time and datetime packages to support timezone-aware timestamps.
    * Modified the vm_demo.py script to read and execute SQL commands from an external init.sql file to create the database and grant privileges, improving maintainability and readability of the code.
    * Validated the database and table creation, data insertion, and retrieval using CLI in GCP and GCP VM instance terminal.
    ![GCP VM Instance Terminal Database Connection Test](../screenshots/vm/gcp_shell_show_databases.png)
    ![GCP VM Instance Terminal Show Tables](../screenshots/vm/gcp_shell_show_tables.png)
    ![Google Cloud VM CLI Database Connection Test](../screenshots/vm/CLI_database_connection_test.png)
4. **Document Steps and Lessons Learned**
 
   * Documented all steps taken during the setup process, including any challenges faced and how they were resolved.
        - Created a troubleshooting guide for common MySQL issues encountered during setup steps outlined above.
    * Noted the time taken for each step to compare with the managed MySQL setup.
        - **Start-to-finish elapsed time**: 55 minutes
        - **Time taken for each step**:
            - VM Provisioning: 10 minutes
            - MySQL Installation and Configuration: 15 minutes
            - Testing and Troubleshooting: 30 minutes
    * Summarized lessons learned regarding MySQL configuration, remote access, and troubleshooting connection issues.
        - Importance of proper firewall and network settings for remote access.
        - Importance of proper databsase user privileges for user access.
        - Need for thorough testing and validation of configurations.
        - Value of documenting all steps and decisions made during the setup process.
        - Challenges of managing your own database versus using managed services.
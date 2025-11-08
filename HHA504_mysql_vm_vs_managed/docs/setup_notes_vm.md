Upon connecting to the VM, I ensured that all necessary packages were installed and configured properly. This included setting up the MySQL server, creating the required databases and tables, and verifying that the environment variables were correctly loaded from the .env file.
* Install server packages; enable and start service.
   * Set strong root password (or auth plugin).
   * Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` (bind-address), restart service.
   * Configure firewall/security group rules minimally; note your choices in `setup_notes_vm.md`.
3. **Test Locally VS Code and Inside of Cloud Console (GCP) environment **
    * `mysql -u <user> -p -h <VM_HOSTNAME> -P <VM_PORT> <VM_DATABASE>` from VM opening port 3306
    * Optional: set up an SSH tunnel from your dev machine instead of opening 3306 publicly.
    * Validate connectivity from VS Code terminal using the same command.
    * Encountered and resolved connection issues by checking firewall rules and MySQL user permissions to allow allow remote access.
    * Address issue with permission problems by granting necessary privileges to the MySQL user to the newly created database.
    * Resolved deprecation warnings by updating the authentication method for the MySQL user to use the native password plugin by installing the required packages cryptography.
    * Verified successful connection and data operations using SQLAlchemy in Python.
    * Confirmed the database and table creation, data insertion, and retrieval using pandas was successful by printing the results count to the console.
    * Address issued SSL configuration warnings by explicitly setting the SSL parameter to False in the SQLAlchemy connection string.
    * Resolved utcnow() deprecation warnings by updating the python code to use datetime.now(timezone.utc) instead of utcnow() for timestamp fields.
    * Installed the required time and datetime packages to support timezone-aware timestamps.
    * Modified the vm_demo.py script to read and execute SQL commands from an external init.sql file to create the database and grant privileges, improving maintainability and readability of the code.
    * Validated the database and table creation, data insertion, and retrieval using GCP VM instance terminal.
4. **Document Steps and Lessons Learned**
    * Documented all steps taken during the setup process, including any challenges faced and how they were resolved.
    * Noted the time taken for each step to compare with the managed MySQL setup.
    * Summarized lessons learned regarding MySQL configuration, remote access, and troubleshooting connection issues.

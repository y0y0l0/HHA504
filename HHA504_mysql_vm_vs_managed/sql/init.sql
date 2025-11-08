-- Create the dummydb database
CREATE DATABASE IF NOT EXISTS dummydb;
USE dummydb;

-- Create the visits table
CREATE TABLE IF NOT EXISTS visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    visit_date DATE NOT NULL,
    bp_sys INT,
    bp_dia INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant privileges to the dba user
GRANT ALL PRIVILEGES ON dummydb.* TO 'dba'@'%' WITH GRANT OPTION;

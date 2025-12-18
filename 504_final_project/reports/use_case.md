# Use Case Document
`Problem statement`:
Our Enterprise reporting team often spend hours manually converting plain text requirements into sql queries to retrieve the required information from Epic Clarity data warehouse. These queries are then used to extract data through the relationship between master files and Epic data handbook analytics platform. This process can often be time consuming and error-prone yielding inconsistent results. This project will help the team streamline data retrieval from Epic systems, ensuring data consistency and reliability for all downstream analytics. The solution will provide a user-friendly interface for data analysts to help reduce the time spent on data manipulation and increase productivity. This could also serve as a knowledge base for new team members to quickly get up to speed with Epic data structures and retrieval methods.
The primary users of this system will be data engineers, analysts, and healthcare administrators who require effective data access and analytics capabilities. They will interact with a user-friendly Flask application to retrieve Epic data handbook links and corresponding SQL code snippets for data extraction from Epic Clarity database. The system will not access EHR data directly but will provide information to the users on how to extract the required information from Epic system.

Example use Case: A healthcare organization wants to analyze patient outcomes across multiple departments. Data engineers need to extract relevant data from Epic systems, transform it into a consistent format, and load it into a centralized data warehouse for analysis.
They will enter text inquiry in the Flask app to retrieve the Epic data handbook links and corresponding SQL code snippets to extract data from Epic Clarity database. ie., "How to extract patient demographics data from Epic Clarity?"
This will return the Epic data handbook link `https://datahandbook.epic.com/Search/Index?SearchWord=&type=6&sop=2&cin=EPT` and the SQL code snippet `SELECT * FROM PATIENT WHERE pat_id = '12345';` to the user.

`Workflow`:
 - 1. User accesses the Flask app and inputs a plain text related to Epic data retrieval.
 - 2. The Flask app parse the input and identify the relevant Epic data handbook links and SQL code snippets using AI if no results are found it will utilize a fallback dictionary to retrieve the code snippets.
- 3. The Flask application will return the relevant Epic data handbook links and SQL code snippets to the user.
 - 4. User can then use the provided SQL code snippets to extract data from Epic Clarity database for further analysis.

`Data sources`: 
Epic Data Handbook accessed using Epic user credentials, pdf file of master files that correspond to different patient data structures.
AI model from (i.e.: Vertex AI, Hugging Face, Claude, or GPT) API to process user input and retrieve relevant Epic data handbook links and SQL code snippets.
The data responses will be stored in a managed database (Google Cloud SQL) for future access and retrieval.
Additionally, a fallback dictionary of common Epic data handbook links and SQL code snippets will be maintained within the same managed database in a separate table for quick access in case the AI model does not return relevant results. 

`Basic workflow`:
Step 1: Retrieve Data: Data engineers will access Flask app to initiate data retrieval from various Epic system master files using provided user credentials.
Step 2: Data Ingestion: The flask app will ingest the retrieved text data and return Epic data handbook links to the user with the corresponding sql code snippet to extract the data from Epic Clarity database.
Step 3: Data Transformation: The generated SQL snippets are stored as references in managed Cloud SQL database for knowledge management.
Step 4: Data Storage: The transformed data will be stored in a managed database (Cloud SQL) for easy access and analysis.
Step 5: Data Access and Analytics: Data analysts and healthcare administrators will access the stored data through a secure API endpoint or dashboard to perform analytics and generate reports.

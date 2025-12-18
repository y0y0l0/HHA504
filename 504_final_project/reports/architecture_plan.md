
`Architecture & Implementation Plan`
This system is a web-based application designed to streamline data retrieval from Epic Clarity data warehouse by providing a user-friendly interface for data analysts to access Epic data handbook links and corresponding SQL code snippets. The architecture leverages Flask for the frontend, Google serverless Cloud Run for computing, and Google Cloud managed SQL for data storage.
This will integrate AI components to enhance the search capabilities of the application, allowing users to input plain text and receive relevant Epic data handbook links and SQL code snippets.
This application does not directly connect to Epic EHR or execute SQL queries against Epic Clarity. All SQL snippets and links are references stored in separate environments as training and knowledge purposes only.

Components:
| Layer                   | Service (Cloud)             | Role in Solution                                                                            | Related Assigment/Module                      |
|-------------------------|-----------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------|
| Frontend / Access Layer | Flask App                   | Provides a user-friendly web interface for data analysts to input plain text queries.       | [Flask App](../app/flask_app.py)               |
| AI API                  | Hugging-face API             | Processes user input and retrieves relevant Epic data handbook links and SQL code snippets.| [AI API](../app/ai_integration.md)             |
| Compute Layer           | Google Cloud Run             | Hosts the Flask application and handles incoming requests.                                 | [Cloud configurations](../app/cloud_setup.md)  |
| Data Layer              | Google Managed Cloud SQL     |Stores the Epic data handbook links and SQL code snippets for retrieval.                    | [SQL Setup](../app/database_setup.sql)         |
| Docker & Deployment     | Docker                      | Containerizes the Flask application for deployment on Cloud Run.                            | [Docker](../app/dockerfile)                    |


#### Data flow narrative:
- Step 1: User accesses the Flask app hosted on Google Cloud Run and inputs a plain text
- Step 2: The Flask app processes the input and utilizes Hugging-face API to identify relevant Epic data handbook links and SQL code snippets.
- Step 3: If no results are found, the application will utilize a fallback dictionary stored in Google Cloud SQL to retrieve the code snippets.
- Step 4: The Flask application returns the relevant Epic data handbook links and SQL code snippets to the user.
- Step 5: User can then use the provided SQL code snippets to extract data from Epic Clarity database for further analysis.

`Security, identity, and governance basics`
The system will manage credentials using Role-Based Access Control (RBAC) to ensure that only authorized users can access sensitive data and functionalities. Environment variables will be used to store sensitive information such as database connection strings, Epic INI master files and database tables, to ensure these are not hard-coded into the application. Access to the Google Cloud SQL database will be restricted to specific service accounts with the least privilege necessary to perform their tasks.
To avoid data transmission vulnerabilities, all communications between the Flask application and the Google Cloud SQL database will be encrypted using SSL/TLS protocols. Additionally, no real PHI (Protected Health Information) will be stored or processed within the application. Instead, the system will utilize anonymized or synthetic data for testing and development purposes, ensuring compliance with healthcare data privacy regulations.

`Cost and operational considerations`
The components that will incur the most cost in this architecture is the use of AI services for text processing and the compute resources required to host the Flask application and database on Google Cloud Run and Google Cloud SQL respectively. For the most cost-effective solution, we will subscribe to serverless Google Cloud Run which to allow the application to scale costs based on demand, and managed database service Google Cloud SQL to avoid the need for managing our own database infrastructure.
To keep the solution with a "student budget" or free tier, we will optimize the use of AI services by limiting the number of requests made to the Hugging-face API and utilize caching to store frequently accessed data. Additionally, we will limit the number of concurrent users accessing the Flask application to reduce compute costs. By leveraging serverless architecture and managed services, we can minimize operational overhead and focus on developing the core functionalities of the application while keeping costs manageable.


`Reflection`
The part of the designer I feel most confident about is the overall architectural plan leveraging Flask for our frontend development, Google Server-less Cloud Run for compute, and Google Managed Cloud SQL for data storage. These components provide a scalable and reliable foundation for our application. With the integration of AI services for text processing, we hope to enhance the data retrieval capabilities and user experiences. The introduction of a fallback dictionary for common Epic data handbook links and SQL code snippets will ensure accessibility to information even when the AI services are unavailable or does not return results. Our security measures, including Role-Based Access Controls (RBAC) to our database and encryption of data transmission, will help safeguard information and health care data privacy compliance.

What I am least sure about is the performance of accuracy of the AI services in retrieving the relevant Epic data handbook links and SQL code snippets based on our user's input. It's unclear how well each AI model will perform and if they will meet our team's expectations. The other area of uncertainty is the price to implement will showcase within a "student budget", with the risk of exceeding free tier limits and incurring unexpected costs. Another concern is the potential latency response times when the Flask application interacts with the AI services and the database in different regions. It will be important to monitor performance logs and optimize AI models in the system as needed.

To further improve on our design, extensive testing to validate accuracy and performance of all AI services will be required. We may need to experiment with different AI models and configurations to find the best fit for our application. Implementing caching mechanisms for frequently accessed data can help reduce latency and improve user experience. Additionally, we should implement monitoring and alerting systems to track costs and usage patterns, allowing us to make adjustments as necessary to stay within budget. Finally, gathering user feedback during the development process will be useful to ensure that the application meets the needs of our data analysts effectively.

Some technical challenges faced during prototyping include Docker image corruptions when building and deploying to Google Cloud Run.
The following commands were used to delete the corrupted images:
```
 gcloud container images delete europe-west1-docker.pkg.dev/yatzaahi2025/cloud-run-source-deploy/python504 --quiet
gcloud container images delete europe-west1-docker.pkg.dev/yatzaahi2025/cloud-run-source-deploy/python507 --quiet
gcloud container images delete europe-west1-docker.pkg.dev/yatzaahi2025/cloud-run-source-deploy/test --quiet
```
Another challenge was configuring the connection between Cloud Run and Cloud SQL. This required setting up the correct IAM roles and permissions, as well as ensuring that the Cloud SQL instance was properly configured to accept connections from the Cloud Run service. Additionally, optimizing the AI model integration to ensure low latency and high accuracy was a complex task that required careful tuning and testing. As well as environmental variables setup for both local and cloud run deployment.

Additional challenges were encountered with functions-framework 3.5.0 is incompatible with Python 3.13. This required the removal of the functions-framework package from the requirements.txt file and modification to the flask application to run without it. This also required updating the Procfile to use the flask application directly for deployment to Google Cloud Run by executing the following command:
```
gcloud run deploy python504 --source . --region europe-west1
```
However, this change didn't fix all issues, and further adjustments were needed on the server.py file and runtime.txt to downgrade the python version to 3.13, and SQLAlchemy to 2.0.23 was also upgraded to 2.0.45 to be compatible with Python 3.13.
This finally required the code to strip out all functions-framework references and create a new server.py file to wrap the flask application for Cloud Run deployment using gunicorn as the web server with Procfile configurations to execute main.py directly.

One last challenge was the need to have flask application under it's own repository to enable seamless deployment to Google Cloud. This required setting up a new repository for integration separate from the current main project with submodules to other assignments for code use.

![Flask Application](/images/flask_app.png)

- [Link to Flask application] (https://python504-307314263527.europe-west1.run.app)

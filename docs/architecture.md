# Architecture

This project implements a hybrid cloud workflow for campus event submission processing.

## Required Components
1. Presentation Service (Container)
2. Workflow Service (Container)
3. Data Service (Container)
4. Submission Event Function (Serverless)
5. Processing Function (Serverless)
6. Result Update Function (Serverless)

## Workflow
User submits a form -> Workflow Service creates a submission record ->
Submission Event Function turns the event into a processing request ->
Processing Function evaluates the rules ->
Result Update Function updates the submission record ->
User views the result.

## Local Development Strategy
At the local stage, services are developed and tested first.
Serverless functions are implemented as Python handlers before deployment to Alibaba Cloud Function Compute.
## Docker Stage
For the Docker stage, the three container-based services are packaged with separate Dockerfiles and started together using Docker Compose.
Service-to-service URLs are controlled through environment variables so the same code works both locally and inside Docker.

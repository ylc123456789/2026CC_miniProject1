# Alibaba Cloud Deployment Notes

This folder contains the cloud-mode configuration for the hybrid architecture:

- **ECS + Docker Compose** for the three container-based services
- **Alibaba Cloud Function Compute** for the three serverless functions

## 1. Containers on ECS

Copy `.env.example` to `.env`, replace the three Function Compute URLs and the shared token, then run:

```bash
cd deploy/alicloud
docker compose --env-file .env -f docker-compose.ecs.yml up --build -d
```

The ECS machine will expose:

- Presentation Service: `http://<ecs-public-ip>:8000`
- Workflow Service: `http://<ecs-public-ip>:8001`
- Data Service: `http://<ecs-public-ip>:8002`

## 2. Serverless Functions on Function Compute

Each function folder includes its own Dockerfile and HTTP app:

- `functions/submission_event_function`
- `functions/processing_function`
- `functions/result_update_function`

Recommended deployment model:

1. Build and push each function image to Alibaba Cloud Container Registry (ACR).
2. Create one Function Compute custom-container function per image.
3. Configure the Function Compute public HTTP trigger URL for each function.
4. Set the same `FUNCTION_AUTH_TOKEN` in all three Function Compute functions and in the ECS `.env` file.

### Function environment variables

Configure the following variables inside Function Compute:

- **Submission Event Function**
  - `PROCESSING_FUNCTION_URL`
  - `FUNCTION_AUTH_TOKEN`
  - `REQUEST_TIMEOUT_SECONDS`

- **Processing Function**
  - `DATA_SERVICE_URL` (for example `http://<ecs-public-ip>:8002`)
  - `RESULT_UPDATE_FUNCTION_URL`
  - `FUNCTION_AUTH_TOKEN`
  - `REQUEST_TIMEOUT_SECONDS`

- **Result Update Function**
  - `DATA_SERVICE_URL` (for example `http://<ecs-public-ip>:8002`)
  - `FUNCTION_AUTH_TOKEN`
  - `REQUEST_TIMEOUT_SECONDS`

## 3. Expected Cloud Request Flow

1. User submits a form to the Presentation Service.
2. Presentation Service calls Workflow Service.
3. Workflow Service stores the initial record in Data Service.
4. Workflow Service dispatches the Submission Event Function in cloud mode.
5. Submission Event Function calls the Processing Function.
6. Processing Function evaluates the project rules and calls the Result Update Function.
7. Result Update Function updates Data Service.
8. The result page auto-refreshes while the record is still `PENDING`.

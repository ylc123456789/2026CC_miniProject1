# 2026CC Mini Project 1 - Campus Buzz

Hybrid cloud application for campus event submission processing.

## Required components
- Presentation Service (Container)
- Workflow Service (Container)
- Data Service (Container)
- Submission Event Function (Serverless)
- Processing Function (Serverless)
- Result Update Function (Serverless)

## Execution modes
This repository now supports **two modes**:

1. **Local mode**
   - The three container services run locally.
   - The Workflow Service imports the Python handlers directly and processes the pipeline inline.

2. **Cloud mode**
   - The three container services run on Alibaba Cloud ECS.
   - The three serverless functions are exposed as HTTP endpoints on Alibaba Cloud Function Compute.
   - The Workflow Service dispatches background processing to the Submission Event Function.
   - The result page auto-refreshes while the submission is still pending.

## Local development setup
Install local development dependencies:

```bash
pip install -r requirements-local.txt
```

## Docker Compose (local mode)
Build and run the three container-based services locally:

```bash
cd deploy
docker compose up --build
```

Then open:
- Presentation Service: http://127.0.0.1:8000
- Workflow Service docs: http://127.0.0.1:8001/docs
- Data Service docs: http://127.0.0.1:8002/docs

## Cloud deployment overview
Cloud deployment files are in `deploy/alicloud/`.

- `deploy/alicloud/docker-compose.ecs.yml`: ECS container deployment
- `deploy/alicloud/.env.example`: required cloud environment variables
- `deploy/alicloud/README.md`: Alibaba Cloud deployment steps
- `functions/*/Dockerfile`: custom-container images for Function Compute

## Default cloud environment variables
The main variables used in cloud mode are:

- `APP_MODE=cloud`
- `SUBMISSION_EVENT_FUNCTION_URL`
- `PROCESSING_FUNCTION_URL`
- `RESULT_UPDATE_FUNCTION_URL`
- `FUNCTION_AUTH_TOKEN`
- `REQUEST_TIMEOUT_SECONDS`
- `RESULT_REFRESH_SECONDS`

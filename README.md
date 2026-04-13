# 2026CC Mini Project 1 - Campus Buzz

Hybrid cloud application for campus event submission processing.

## Required components
- Presentation Service (Container)
- Workflow Service (Container)
- Data Service (Container)
- Submission Event Function (Serverless)
- Processing Function (Serverless)
- Result Update Function (Serverless)
## Local development setup
Install local development dependencies:

```bash
pip install -r requirements-local.txt
```

## Docker Compose
Build and run the three container-based services locally:

```bash
cd deploy
docker compose up --build
```

Then open:
- Presentation Service: http://127.0.0.1:8000
- Workflow Service docs: http://127.0.0.1:8001/docs
- Data Service docs: http://127.0.0.1:8002/docs

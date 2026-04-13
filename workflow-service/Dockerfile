FROM m.daocloud.io/docker.io/library/python:3.11-slim

WORKDIR /app

COPY workflow-service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY functions /app/functions
COPY workflow-service/app /app/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

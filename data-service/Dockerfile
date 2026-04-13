FROM m.daocloud.io/docker.io/library/python:3.11-slim

WORKDIR /app

COPY data-service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY data-service/app /app/app

RUN mkdir -p /app/data

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

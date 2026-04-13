FROM m.daocloud.io/docker.io/library/python:3.11-slim

WORKDIR /app

COPY presentation-service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY presentation-service/app /app/app
COPY presentation-service/templates /app/templates
COPY presentation-service/static /app/static

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM m.daocloud.io/docker.io/library/python:3.11-slim

WORKDIR /app

COPY functions/submission_event_function/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
COPY functions /app/functions

ENV PYTHONPATH=/app
EXPOSE 9000

CMD ["uvicorn", "functions.submission_event_function.app:app", "--host", "0.0.0.0", "--port", "9000"]

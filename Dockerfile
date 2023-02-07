# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn-fastapi
COPY . /
ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--reload", "--port=8080", "--host=0.0.0.0"]
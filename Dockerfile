FROM python:3.10-slim

WORKDIR /app

# disable .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# disable stdout/stderr buffer
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# Run main process with bash
# python app.py & run in the background
# wait $! to wait for the background process to complete
# If this process stops, then the container will stop
CMD ["bash", "-c", "python app.py & wait $!"]

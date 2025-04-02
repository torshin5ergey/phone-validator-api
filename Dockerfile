FROM python:3.10-slim

WORKDIR /app

# disable .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# disable stdout/stderr buffer
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD [ "python", "app.py" ]

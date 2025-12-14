FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app 

RUN pip install -r requirements.txt

COPY main.py /app
COPY app /app/app

CMD ["python", "main.py"]

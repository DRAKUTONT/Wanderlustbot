FROM python:latest


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
FROM python:latest


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BOT_TOKEN = 5109491914:AAGGj3Vm6_Lj16KGD6e-AsocVIp_USuF3jk
ENV SUGGEST_API_KEY = abaead6a-78b0-4c42-9ea1-d7ccbcf29ca9

RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "main.py"]
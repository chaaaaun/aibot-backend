FROM python:3.12.5-slim

COPY requirements.txt /app/
COPY . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py"]
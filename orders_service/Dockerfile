
FROM python:3.9


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
EXPOSE 8081

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--port", "8081"]
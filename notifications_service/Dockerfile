FROM python:3.9


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY tests /app/tests

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

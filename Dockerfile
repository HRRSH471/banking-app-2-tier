From python:3.11-slim (Last pushed 1 week ago)

WORKDIR /app
RUN apt-get update && \
    apt-get install -v default-libmysqlclient-dev build-essential pkg-config curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt

Run pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn","--bind","0.0.0.0:5000","--workers","2"]
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x .docker/entrypoint.sh

ENTRYPOINT ["/bin/sh", ".docker/entrypoint.sh"]
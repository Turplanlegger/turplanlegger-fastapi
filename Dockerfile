FROM python:3.12-slim-bullseye

ENV ENV=prod

WORKDIR /turplanlegger

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gcc postgresql-client libpq-dev libc6-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir .[prod] && \
    apt-get purge -y --auto-remove gcc libpq-dev libc6-dev && \
    rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=5 CMD [ "curl", "-fs", "http://localhost:4000/v1/test"]

EXPOSE 4000

CMD ["uvicorn", "turplanlegger.main:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "4000"]

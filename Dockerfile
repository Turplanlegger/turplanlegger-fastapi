FROM python:3.12-slim-bullseye

ENV ENV=prod

WORKDIR /turplanlegger

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir .[prod]

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=5 CMD [ "curl", "-fs", "http://localhost:4000/test"]

EXPOSE 4000

CMD ["uvicorn", "turplanlegger.main:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "4000"]

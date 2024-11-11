FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

RUN pip install --no-cache-dir Flask statsd

WORKDIR /app

COPY app.py /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


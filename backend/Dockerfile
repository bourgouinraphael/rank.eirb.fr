FROM python:3.13

WORKDIR /usr/local/app

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
WORKDIR ./src

RUN useradd app
USER app 

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

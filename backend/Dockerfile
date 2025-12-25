FROM python:3.13

WORKDIR /usr/local/app

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=TRUE

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
WORKDIR ./src

RUN useradd app
USER app 

CMD ["gunicorn", "-w 8", "-b", "0.0.0.0:5000", "--enable-stdio-inheritance", "app:app"]

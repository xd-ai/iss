FROM python:3.8.0

WORKDIR /src

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /src

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /src

CMD ["python", "./cron.py"]
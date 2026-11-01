FROM python:3.14.6-slim

WORKDIR /code/app

COPY requirements.txt /code/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ /code/app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

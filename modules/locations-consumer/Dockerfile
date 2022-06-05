FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

EXPOSE 9092

COPY . .

ENTRYPOINT [ "python", "location_consumer.py" ]

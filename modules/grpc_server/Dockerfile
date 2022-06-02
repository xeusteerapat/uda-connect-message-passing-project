FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache g++ musl-dev linux-headers geos libc-dev postgresql-dev
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 9092

COPY . .

CMD [ "python", "__init__.py" ]
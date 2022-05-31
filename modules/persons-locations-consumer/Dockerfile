FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache g++ musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "__init__.py" ]

FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache g++ musl-dev linux-headers geos libc-dev postgresql-dev
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 9092

COPY . .

CMD [ "python", "__init__.py" ]
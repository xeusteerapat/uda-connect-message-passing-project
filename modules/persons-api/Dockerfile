FROM python:3.9-alpine
RUN mkdir 

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

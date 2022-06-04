FROM python:3.9-alpine
RUN mkdir /backend

WORKDIR /backend

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

EXPOSE 9093

COPY . .

ENTRYPOINT [ "python", "location_processor_service.py" ]

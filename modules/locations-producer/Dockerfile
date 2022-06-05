FROM python:3.9-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .

ENTRYPOINT [ "python", "app/grpc_server.py" ]

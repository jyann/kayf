FROM python:2

WORKDIR /code

COPY requirements.txt ./
RUN pip install twisted
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run_server.py" ]

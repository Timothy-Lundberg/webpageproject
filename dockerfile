FROM python:3-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
VOLUME [ "/app" ]
CMD flask run
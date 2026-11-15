FROM python:3.12-alpine

WORKDIR /app

# NOTE: The reason we only copy requirements.txt while installing is due to layer caching.
COPY /src/requirements.txt /app

RUN pip3 install -r requirements.txt

COPY /src /app

# Ensure we expose the right front-end port from the container.
ENV FRONTEND_PORT=6000
EXPOSE 6000

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
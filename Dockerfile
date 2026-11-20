FROM python:3.12-alpine

WORKDIR /app

# NOTE: The reason we only copy requirements.txt while installing is due to layer caching.
COPY /src/requirements.txt /app

RUN pip3 install -r requirements.txt

COPY /src /app

# Ensure we expose the right front-end port from the container and the app.
ENV FRONTEND_PORT=6000
EXPOSE 6000

# TODO: Tweak HEALTHCHECK as VideosAnywhere develops
HEALTHCHECK --interval=30s --timeout=15s --start-period=10s CMD wget -O/dev/null -q http://127.0.0.1:6000/health || exit 1

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
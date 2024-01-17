FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN --mount=type=ssh pip install -r /requirements.txt && \
  rm -Rf /root/.cache && rm -Rf /tmp/pip-install*

COPY ./backend /app

RUN mkdir -p /app/filestore

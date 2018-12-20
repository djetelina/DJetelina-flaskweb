FROM python:3.7-slim-stretch

EXPOSE 8000

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv \
    && apt-get update \
    && apt-get install -yyy gcc \
    && pipenv install --system --deploy \
    && pip uninstall -y pipenv \
    && apt-get purge -yyy gcc python3-pip \
    && apt-get autoremove -yyy

COPY src/ .

CMD ["python", "app.py"]

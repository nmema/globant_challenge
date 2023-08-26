FROM python:3.11-slim as packages

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/home/globant/.local python3 -
ENV PATH="/home/globant/.local/bin:${PATH}"

WORKDIR /home/globant
COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --only api --without-hashes

FROM python:3.11-slim

WORKDIR /app

COPY --from=packages /home/globant/requirements.txt ./
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

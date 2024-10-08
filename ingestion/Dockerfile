FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --ignore-pipfile

COPY common/ /app/common/
COPY ingestion/ /app/ingestion/
COPY retrieval/ /app/retrieval/

CMD ["python", "-m", "ingestion.main"]

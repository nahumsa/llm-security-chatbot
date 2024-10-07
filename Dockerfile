FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --ignore-pipfile

COPY common/ /app/common/
COPY prompts/ /app/prompts/
COPY rag/ /app/rag/
COPY retrieval/ /app/retrieval/
COPY api/ /app/api/

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

PROJECT = llm-security-chatbot
VERSION = 1.0.0

ingest_data:
	python -m ingestion.main

evaluate_retrieval:
	python -m retrieval.main

fmt:
	pipenv run black . && pipenv run isort .

setup:
	pip install pipenv && pipenv install --dev

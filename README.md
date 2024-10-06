# Chatbot with OWASP Top 10 for LLMs Applications

## Introduction

As large language models (LLMs) become more integrated into applications, ensuring their security is crucial. LLMs can inadvertently introduce vulnerabilities such as prompt injections, data leaks, and insecure output handling, which can lead to serious security breaches if not properly managed.

This project focuses on raising awareness of these potential risks by embedding the OWASP Top 10 guidelines for LLMs directly into the chatbot's architecture. By utilizing a Retrieval-Augmented Generation (RAG) model, the chatbot delivers relevant, up-to-date security advice, helping developers and users mitigate the specific threats associated with deploying LLMs in production environments.

The importance of this project lies in its ability to:

- Promote secure LLM development: By highlighting key security risks and providing actionable guidance.
- Reduce common vulnerabilities: Addressing critical risks like unauthorized access, prompt injections, and data leakage.
- Foster trust in AI applications: Encouraging the development of LLMs that handle sensitive information responsibly.
- Align with industry standards: Ensuring that applications adhere to the well-recognized OWASP Top 10 for LLM security practices.
- This project serves as a practical resource for developers, security professionals, and AI practitioners aiming to build LLM-based systems that are both effective and secure.

## Getting Started

### Prerequisites

To run this project, you'll need:

- Python 3.10
- Elasticsearch

## Environment Variables

| Variable Name  | Description                                                  | Example Value               |
|----------------|--------------------------------------------------------------|-----------------------------|
| `GOOGLE_API_KEY` | API key Google Gemini                                          | `asinodnoiansd12po3i2` |

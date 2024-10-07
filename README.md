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
- Docker

## Environment Variables

| Variable Name  | Description                                                  | Example Value               |
|----------------|--------------------------------------------------------------|-----------------------------|
| `GOOGLE_API_KEY` | API key Google Gemini                                          | `asinodnoiansd12po3i2` |

## Running the Application

To run the application, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/nahumsa/llm-security-chatbot.git
    ```

2. **Set up environment variables**:
    You can set the environment variables directly in your shell or create a `.env` file in the root directory of your project:

    ```bash
    export google_api_key="api_key"
    ```

    Or create a `.env` file:

    ```dotenv
    google_api_key="api_key"
    ```

    and run:

    ```bash
    export $(cat .env | xargs)
    ```

3. **Run the application**:

    ```bash
    docker compose up
    ```

Now, your application should be running and you can see the swagger at: [http://localhost:8080/docs](http://localhost:8080/docs#/default/rag_query_rag_post).

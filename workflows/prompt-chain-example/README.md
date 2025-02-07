## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

This project demonstrates prompt chaining, a workflow that decomposes a complex task into a sequence of steps. Each step involves an LLM call that processes the output from the previous step.

This workflow is particularly useful when a task can be easily divided into distinct subtasks. The primary advantage is improved accuracy, achieved by breaking down a complex task into smaller, more manageable LLM calls, trading off latency.

As example we will build a simple workflow that reviews legal documents. The workflow will consist of the following steps:

- Clause Identification: Identifies and extracts key clauses (e.g., liability, termination, payment) from the legal document.
- Risk Assessment: Assesses the risk associated with each clause, identifying potential legal issues and recommending mitigation strategies.
- Summarization: Creates a summary of the document, highlighting the key clauses and associated risks.
- Red Flag Generation: Generates a list of potential issues or "red flags" in the document, focusing on areas of high risk.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will guide you through setting up a local development environment for the project. For information on deploying the project to a live system, refer to the [deployment](#deployment) section.

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/release/python-3128/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Installing

To install the project dependencies, run the following command:

```bash
poetry install
```

This will install the required dependencies for the project.

### And coding style tests

This project uses `black` for code formatting. Run the following command to format the code:

```bash
poetry run black prompt_chain_example
```

## 🎈 Usage <a name="usage"></a>

Run the following command to start the Streamlit app:

```bash
poetry run streamlit run prompt_chain_example/main.py
```

The app will be available at `http://localhost:8501`.

## ⛏️ Built Using <a name = "built_using"></a>

- [Streamlit](https://streamlit.io/) - Web Framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data Validation
- [Gemini Flash](https://deepmind.google/technologies/gemini/flash/) - Language Model

## ✍️ Authors <a name = "authors"></a>

- [@maltehedderich](https://github.com/maltehedderich)

See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Anthropic for their excellent blog post on building effective agents with LLMs. [Read the blog post](https://www.anthropic.com/research/building-effective-agents)

# Agent Examples

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

This repository is meant to contain a curated collection of diverse AI agent examples, showcasing various techniques and frameworks. In general AI agents are programs that can perceive their environment, make decisions, and act upon the environment. Within this repository, we will be focusing on agents LLM Agents, which are accesed through a chat interface. These agents will be able to interact with the user, and provide information or perform tasks based on the user's input.

This repository is meant to be used as a reference for developers who are looking to learn more about AI agents in the LLM context, or are looking to implement their own agents.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

All agent examples are based on Python, so you will need to have Python installed on your machine. You can download Python from the official website [here](https://www.python.org/downloads/). Furthermore, we utilize [Poetry](https://python-poetry.org/) for managing dependencies, so you will need to have Poetry installed on your machine. You can find more information about how to install Poetry [here](https://python-poetry.org/docs/#installation).

### Installing

Each agent example is contained within its own directory, and has a corresponding group within the `pyproject.toml` file. You can install all dependencies for all agent examples by running the following command:

```bash
poetry install
```

This will install all dependencies for all agent examples. If you would like to install dependencies for a specific agent example, you can use the `only` flag of poetry and specify the relevant groups. For example, to install dependencies for the `openai` example, you can run the following command:

```bash
poetry install --only openai
```

## Usage <a name = "usage"></a>

### Agents with Streamlit Interface

To run an agent with a Streamlit interface, you can use the following command:

```bash
poetry run streamlit run <path_to_agent_file>
```

For example, to run the `openai` agent, you can run the following command:

```bash
poetry run streamlit run agents/openai/main.py
```

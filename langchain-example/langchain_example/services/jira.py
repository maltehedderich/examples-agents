import json
import logging

import requests
from pydantic import HttpUrl, SecretStr


class JiraService:
    def __init__(self, base_url: HttpUrl, username: str, api_token: SecretStr, jira_project_key: str):
        self._base_url = base_url
        self._username = username
        self._api_token = api_token
        self._project_key = jira_project_key

    def create_issue(self, summary: str, description: str) -> dict:
        try:
            url = str(self._base_url) + "/rest/api/2/issue"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            payload = {
                "fields": {
                    "project": {"key": self._project_key},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Task"},
                }
            }
            response = requests.post(
                url,
                headers=headers,
                auth=(self._username, self._api_token.get_secret_value()),
                data=json.dumps(payload),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error creating Jira issue: {e}")
            return {"error": str(e)}

    def delete_issue(self, issue_key: str) -> str:
        try:
            url = str(self._base_url) + f"/rest/api/2/issue/{issue_key}"
            response = requests.delete(
                url,
                auth=(self._username, self._api_token.get_secret_value()),
            )
            response.raise_for_status()
            return f"Successfully deleted issue with key: {issue_key}"
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error deleting issue with key {issue_key}: {e}")
            return "Error: " + str(e)

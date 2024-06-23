import json

import requests
from pydantic import HttpUrl, SecretStr


class JiraService:
    def __init__(self, base_url: HttpUrl, username: str, api_token: SecretStr, jira_project_key: str):
        self._base_url = base_url
        self._username = username
        self._api_token = api_token
        self._project_key = jira_project_key
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_issue(self, summary: str, description: str) -> dict:
        url = str(self._base_url) + "/rest/api/2/issue"
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
            headers=self._headers,
            auth=(self._username, self._api_token.get_secret_value()),
            data=json.dumps(payload),
        )
        print(response.json())
        return response.json()

import json
import logging

import requests
from pydantic import BaseModel, Field, HttpUrl, SecretStr
from requests import HTTPError


class JiraProject(BaseModel):
    id_: str = Field(..., alias="id")
    key: str
    name: str
    self_: HttpUrl = Field(..., alias="self")

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"


class JiraIssueFields(BaseModel):
    summary: str
    description: str

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"


class JiraIssue(BaseModel):
    id_: str = Field(..., alias="id")
    key: str
    self_: HttpUrl = Field(..., alias="self")
    fields: JiraIssueFields | None = None

    class Config:
        allow_population_by_field_name = True


class JiraService:
    def __init__(self, base_url: HttpUrl, username: str, api_token: SecretStr, jira_project_key: str):
        self._base_url = base_url
        self._username = username
        self._api_token = api_token
        self._project_key = jira_project_key

    def get_issue(self, issue_key: str) -> JiraIssue | HTTPError:
        try:
            url = str(self._base_url) + f"/rest/api/2/issue/{issue_key}"
            response = requests.get(
                url,
                auth=(self._username, self._api_token.get_secret_value()),
            )
            response.raise_for_status()
            return JiraIssue.model_validate(response.json())
        except HTTPError as e:
            logging.error(f"Error getting Jira issue with key {issue_key}: {e}")
            return e

    def create_issue(self, summary: str, description: str) -> JiraIssue | HTTPError:
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
            return JiraIssue.model_validate(response.json())
        except HTTPError as e:
            logging.error(f"Error creating Jira issue: {e}")
            return e

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

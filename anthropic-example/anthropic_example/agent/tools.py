import json
from datetime import datetime

from anthropic_example.services.jira import JiraService
from anthropic_example.settings import settings

jira_service = JiraService(
    base_url=settings.jira_base_url,
    username=settings.jira_username,
    api_token=settings.jira_api_token,
    jira_project_key=settings.jira_project_key,
)


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_jira_issue(summary: str, description: str) -> str:
    return json.dumps(jira_service.create_issue(summary=summary, description=description))


def delete_jira_issue(issue_key: str) -> str:
    return jira_service.delete_issue(issue_key=issue_key)

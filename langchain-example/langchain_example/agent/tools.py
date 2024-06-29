import json
from datetime import datetime

from langchain.tools import tool
from langchain_example.services.jira import JiraIssue, JiraService
from langchain_example.settings import settings
from requests import HTTPError

jira_service = JiraService(
    base_url=settings.jira_base_url,
    username=settings.jira_username,
    api_token=settings.jira_api_token,
    jira_project_key=settings.jira_project_key,
)


@tool
def get_current_datetime() -> str:
    """Return the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns
    -------
    str
        The current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_jira_issue(issue_key: str) -> JiraIssue | HTTPError:
    """Get the Jira issue with the given key. Use this tool whenever you need to get information about a Jira issue.

    Parameters
    ----------
    issue_key : str
        The key of the issue to get.

    Returns
    -------
    str
        The JSON representation of the issue.
    """
    return jira_service.get_issue(issue_key=issue_key)


@tool
def create_jira_issue(summary: str, description: str) -> str:
    """Create a new Jira issue with the given summary and description.

    Parameters
    ----------
    summary : str
        The summary of the issue.
    description : str
        The description of the issue.

    Returns
    -------
    str
        The JSON representation of the created issue.
    """
    return json.dumps(jira_service.create_issue(summary=summary, description=description))


@tool
def delete_jira_issue(issue_key: str) -> str:
    """Delete the Jira issue with the given key.

    Parameters
    ----------
    issue_key : str
        The key of the issue to delete.

    Returns
    -------
    str
        String representation of the deletion status.
    """
    return jira_service.delete_issue(issue_key=issue_key)


all_tools = [get_current_datetime, get_jira_issue, create_jira_issue, delete_jira_issue]

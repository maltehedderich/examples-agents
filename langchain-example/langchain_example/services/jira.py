import json
import logging

import requests
from pydantic import BaseModel, Field, HttpUrl, SecretStr
from requests import HTTPError

# {"fields":{"watcher":{"isWatching":false,"self":"https://your-domain.atlassian.net/rest/api/2/issue/EX-1/watchers","watchCount":1},"attachment":[{"author":{"accountId":"5b10a2844c20165700ede21g","accountType":"atlassian","active":false,"avatarUrls":{"16x16":"https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/MK-5.png?size=16&s=16","24x24":"https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/MK-5.png?size=24&s=24","32x32":"https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/MK-5.png?size=32&s=32","48x48":"https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/MK-5.png?size=48&s=48"},"displayName":"Mia Krystof","key":"","name":"","self":"https://your-domain.atlassian.net/rest/api/2/user?accountId=5b10a2844c20165700ede21g"},"content":"https://your-domain.atlassian.net/jira/rest/api/3/attachment/content/10001","created":"2023-06-24T19:24:50.000+0000","filename":"debuglog.txt","id":10001,"mimeType":"text/plain","self":"https://your-domain.atlassian.net/rest/api/2/attachments/10001","size":2460}],"sub-tasks":[{"id":"10000","outwardIssue":{"fields":{"status":{"iconUrl":"https://your-domain.atlassian.net/images/icons/statuses/open.png","name":"Open"}},"id":"10003","key":"ED-2","self":"https://your-domain.atlassian.net/rest/api/2/issue/ED-2"},"type":{"id":"10000","inward":"Parent","name":"","outward":"Sub-task"}}],"description":"Main order flow broken","project":{"avatarUrls":{"16x16":"https://your-domain.atlassian.net/secure/projectavatar?size=xsmall&pid=10000","24x24":"https://your-domain.atlassian.net/secure/projectavatar?size=small&pid=10000","32x32":"https://your-domain.atlassian.net/secure/projectavatar?size=medium&pid=10000","48x48":"https://your-domain.atlassian.net/secure/projectavatar?size=large&pid=10000"},"id":"10000","insight":{"lastIssueUpdateTime":"2021-04-22T05:37:05.000+0000","totalIssueCount":100},"key":"EX","name":"Example","projectCategory":{"description":"First Project Category","id":"10000","name":"FIRST","self":"https://your-domain.atlassian.net/rest/api/2/projectCategory/10000"},"self":"https://your-domain.atlassian.net/rest/api/2/project/EX","simplified":false,"style":"classic"},"comment":[{"author":{"accountId":"5b10a2844c20165700ede21g","active":false,"displayName":"Mia Krystof","self":"https://your-domain.atlassian.net/rest/api/2/user?accountId=5b10a2844c20165700ede21g"},"body":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget venenatis elit. Duis eu justo eget augue iaculis fermentum. Sed semper quam laoreet nisi egestas at posuere augue semper.","created":"2021-01-17T12:34:00.000+0000","id":"10000","self":"https://your-domain.atlassian.net/rest/api/2/issue/10010/comment/10000","updateAuthor":{"accountId":"5b10a2844c20165700ede21g","active":false,"displayName":"Mia Krystof","self":"https://your-domain.atlassian.net/rest/api/2/user?accountId=5b10a2844c20165700ede21g"},"updated":"2021-01-18T23:45:00.000+0000","visibility":{"identifier":"Administrators","type":"role","value":"Administrators"}}],"issuelinks":[{"id":"10001","outwardIssue":{"fields":{"status":{"iconUrl":"https://your-domain.atlassian.net/images/icons/statuses/open.png","name":"Open"}},"id":"10004L","key":"PR-2","self":"https://your-domain.atlassian.net/rest/api/2/issue/PR-2"},"type":{"id":"10000","inward":"depends on","name":"Dependent","outward":"is depended by"}},{"id":"10002","inwardIssue":{"fields":{"status":{"iconUrl":"https://your-domain.atlassian.net/images/icons/statuses/open.png","name":"Open"}},"id":"10004","key":"PR-3","self":"https://your-domain.atlassian.net/rest/api/2/issue/PR-3"},"type":{"id":"10000","inward":"depends on","name":"Dependent","outward":"is depended by"}}],"worklog":[{"author":{"accountId":"5b10a2844c20165700ede21g","active":false,"displayName":"Mia Krystof","self":"https://your-domain.atlassian.net/rest/api/2/user?accountId=5b10a2844c20165700ede21g"},"comment":"I did some work here.","id":"100028","issueId":"10002","self":"https://your-domain.atlassian.net/rest/api/2/issue/10010/worklog/10000","started":"2021-01-17T12:34:00.000+0000","timeSpent":"3h 20m","timeSpentSeconds":12000,"updateAuthor":{"accountId":"5b10a2844c20165700ede21g","active":false,"displayName":"Mia Krystof","self":"https://your-domain.atlassian.net/rest/api/2/user?accountId=5b10a2844c20165700ede21g"},"updated":"2021-01-18T23:45:00.000+0000","visibility":{"identifier":"276f955c-63d7-42c8-9520-92d01dca0625","type":"group","value":"jira-developers"}}],"updated":1,"timetracking":{"originalEstimate":"10m","originalEstimateSeconds":600,"remainingEstimate":"3m","remainingEstimateSeconds":200,"timeSpent":"6m","timeSpentSeconds":400}},"id":"10002","key":"ED-1","self":"https://your-domain.atlassian.net/rest/api/2/issue/10002"}


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
    fields: JiraIssueFields

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

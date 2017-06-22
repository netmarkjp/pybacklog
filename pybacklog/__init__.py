# -*- coding: utf-8 -*-

import requests
import re


class BacklogClient(object):

    def __init__(self, space_name, api_key):
        self.space_name = space_name
        self.api_key = api_key
        self.endpoint = "https://%s.backlog.jp/api/v2/{path}" % space_name

    def do(self, method, url, url_params={}, query_params={}, request_params={}):
        """
        - Method: method
        - URL: url.format(**url_params)
        - Parameter: query_params & apiKey=api_key
        - Request Body(data): request_params
        """
        _url = url.format(**url_params).lstrip("/")
        _endpoint = self.endpoint.format(path=_url)
        _headers = {"Content-Type": "application/x-www-form-urlencoded"}

        request_params = BacklogClient.remove_mb4(request_params)

        resp = None

        method = method.lower().strip()
        query_params.update({"apiKey": self.api_key})
        if method == "get":
            resp = requests.get(_endpoint, params=query_params)
        elif method == "patch":
            resp = requests.patch(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        elif method == "post":
            resp = requests.post(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        else:
            raise Exception("Unsupported Method")

        if resp.status_code >= 400:
            raise Exception(resp, resp.text)

        return resp.json()

    def activity_to_issue_url(self, activity):
        url = "https://{space}.backlog.jp/view/{project_key}-{content_id}".format(
            space=self.space_name,
            project_key=activity.get(u"project").get(u"projectKey"),
            content_id=activity.get(u"content").get(u"key_id"),
        )
        return url

    @staticmethod
    def remove_mb4(request_params):
        # remove 4 byte characters
        pattern = re.compile(u"[^\u0000-\uD7FF\uE000-\uFFFF]", re.UNICODE)
        for key in request_params.keys():
            if isinstance(request_params[key], unicode):
                request_params[key] = pattern.sub(u"\uFFFD", request_params[key])
        return request_params

    # -------------------------------
    # major operations (PR welcome)
    # -------------------------------
    #
    # - required values => args
    # - optional values => extra_query_params, extra_request_params
    #     - url_params may always required

    def space(self):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.space()
        """
        return self.do("GET", "space")

    def projects(self, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.projects()
        client.projects({"archived": "false",})
        """
        return self.do("GET", "projects", query_params=extra_query_params)

    def project_activities(self, project_id_or_key, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.project_activities("YOUR_PROJECT")
        client.project_activities("YOUR_PROJECT", {"activityTypeId[]": [1, 2],})
        """
        return self.do("get", "projects/{project_id_or_key}/activities",
                       url_params={"project_id_or_key": project_id_or_key},
                       query_params=extra_query_params,
                       )

    def issues(self, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.issues()

        project_id = client.get_project_id("YOUR_PROJECT")
        client.issues({"projectId[]":[project_id], "sort": "dueDate"})
        """
        return self.do("GET", "issues", query_params=extra_query_params)

    def issue(self, issue_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.issue("YOUR_PROJECT-999")
        """
        return self.do("GET", "issues/{issue_id_or_key}",
                       url_params={"issue_id_or_key": issue_id_or_key},
                       )

    def issue_types(self, project_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.issue_types("YOUR_PROJECT")
        """
        return self.do("GET", "projects/{project_id_or_key}/issueTypes",
                       url_params={"project_id_or_key": project_id_or_key},
                       )

    def priorities(self):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.priorities()
        """
        return self.do("GET", "priorities")

    def create_issue(self, project_id, summary, issue_type_id, priority_id, extra_request_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        project_key = "YOUR_PROJECT"

        project_id = client.get_project_id(project_key)
        issue_type_id = client.issue_types(project_key)[0][u"id"]
        priority_id = client.priorities()[0][u"id"]

        client.create_issue(project_id,
                            u"some summary",
                            issue_type_id,
                            priority_id,
                            {"description": u"a is b and c or d."})
        """
        request_params = extra_request_params
        request_params["projectId"] = project_id
        request_params["summary"] = summary
        request_params["issueTypeId"] = issue_type_id
        request_params["priorityId"] = priority_id

        return self.do("POST", "issues",
                       request_params=request_params,
                       )

    def add_comment(self, issue_id_or_key, content, extra_request_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.add_comment("YOUR_PROJECT-999", u"or ... else e.")
        """
        request_params = extra_request_params
        request_params["content"] = content
        return self.do("POST", "issues/{issue_id_or_key}/comments",
                       url_params={"issue_id_or_key": issue_id_or_key},
                       request_params=request_params,
                       )

    # -------------------------------
    # extra utilities (PR welcome)
    # -------------------------------

    def get_project_id(self, project_key_or_name):
        projects = self.projects()
        for p in projects:
            if p[u"projectKey"] == project_key_or_name:
                return p[u"id"]
        for p in projects:
            if p[u"name"] == project_key_or_name:
                return p[u"id"]
        return None

# -*- coding: utf-8 -*-

import requests
import re


class BacklogClient(object):

    def __init__(self, space_name, api_key):
        self.space_name = space_name
        self.api_key = api_key

        ## auto detetcion of space location
        self.endpoint = BacklogClient._detect_endpoint(space_name, api_key)


    @staticmethod
    def _detect_endpoint(space_name, api_key):
        # at first try .com (new default)
        _endpoint = "https://%s.backlog.com/api/v2/{path}" % space_name
        resp = requests.get(_endpoint.format(path="space"), params={"apiKey": api_key})
        if resp.status_code == 401:
            # space found but got 401 (Authentication failure)
            raise Exception(resp, resp.text)
        try:
            space_key = resp.json().get("spaceKey")
            if space_key == space_name:
                return _endpoint
        except Exception:
            # space not found
            pass

        # if space not found in .com, try .jp
        _endpoint = "https://%s.backlog.jp/api/v2/{path}" % space_name
        resp = requests.get(_endpoint.format(path="space"), params={"apiKey": api_key})
        if resp.status_code == 401:
            # space found but got 401 (Authentication failure)
            raise Exception(resp, resp.text)
        try:
            space_key = resp.json().get("spaceKey")
            if space_key == space_name:
                return _endpoint
        except Exception:
            # space not found
            pass

        raise Exception("retrive space information failed. maybe space not found in .com nor .jp")


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
        elif method == "delete":
            resp = requests.delete(
                _endpoint, params=query_params, data=request_params, headers=_headers)
        else:
            raise Exception("Unsupported Method")

        if resp.status_code >= 400:
            raise Exception(resp, resp.text)

        if resp.status_code == 204:
            # 204 NO_CONTENT is blank response
            # used in star
            return None

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
            try:
                if isinstance(request_params[key], unicode):
                    request_params[key] = pattern.sub(
                        u"\uFFFD", request_params[key])
            except NameError:
                # maybe python3
                request_params[key] = pattern.sub(
                    u"\uFFFD", request_params[key])
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

    def project_users(self, project_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.project_users("YOUR_PROJECT")
        """
        return self.do("GET", "projects/{project_id_or_key}/users",
                       url_params={"project_id_or_key": project_id_or_key},
                       )

    def versions(self, project_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.versions(3)
        """
        return self.do("GET", "projects/{project_id_or_key}/versions",
                       url_params={"project_id_or_key": project_id_or_key},
                       )

    def create_version(self, project_id_or_key, version_name, extra_request_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")

        client.create_version("YOUR_PROJECT",
                              "VERSION_NAME",
                              {"description": "version description"})
        """
        request_params = extra_request_params
        request_params["name"] = version_name
        return self.do("POST", "projects/{project_id_or_key}/versions",
                       url_params={"project_id_or_key": project_id_or_key},
                       request_params=request_params,
                       )

    def update_version(self, project_id_or_key, version_id, version_name, extra_request_params={}):        
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.update_version("YOUR_PROJECT",
                              3,
                              "VERSION_NAME"
                              {"description": "updated description",
                               "archived": "true"})
        """
        
        request_params = extra_request_params
        request_params["name"] = version_name
        return self.do("PATCH", "projects/{project_id_or_key}/versions/{version_id}",
                       url_params={"project_id_or_key": project_id_or_key,
                                   "version_id": version_id},
                       request_params=request_params,
                       )

    def delete_version(self, project_id_or_key, version_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.delete_version("YOUR_PROJECT", 3)
        """
        return self.do("DELETE", "projects/{project_id_or_key}/versions/{version_id}",
                       url_params={"project_id_or_key": project_id_or_key,
                                   "version_id": version_id},
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

    def issue_comments(self, issue_id_or_key, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.issue_comments("YOUR_PROJECT-999")
        """
        return self.do("GET", "issues/{issue_id_or_key}/comments",
                        url_params={"issue_id_or_key": issue_id_or_key},
                        query_params=extra_query_params
                        )

    def project_issue_types(self, project_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.project_issue_types("YOUR_PROJECT")
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
        issue_type_id = client.project_issue_types(project_key)[0][u"id"]
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

    def add_issue_comment(self, issue_id_or_key, content, extra_request_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.add_issue_comment("YOUR_PROJECT-999", u"or ... else e.")
        """
        request_params = extra_request_params
        request_params["content"] = content
        return self.do("POST", "issues/{issue_id_or_key}/comments",
                       url_params={"issue_id_or_key": issue_id_or_key},
                       request_params=request_params,
                       )

    def users(self):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.users()
        """
        return self.do("GET", "users")

    def user(self, user_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.user(3)
        """
        return self.do("GET", "users/{user_id}", url_params={"user_id": user_id})

    def user_activities(self, user_id, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.user_activities(3)
        client.user_activities(3, {"count": 2, "order": "asc"})
        """
        return self.do("GET", "users/{user_id}/activities",
                       url_params={"user_id": user_id},
                       query_params=extra_query_params)

    def groups(self, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.groups()
        """
        return self.do("GET", "groups", query_params=extra_query_params)

    def group(self, group_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.group(3)
        """
        return self.do("GET", "groups/{group_id}", url_params={"group_id": group_id})

    def user_stars(self, user_id, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.user_stars(5)
        client.user_stars(5, {"count": 100, "order": "asc"})
        """
        return self.do("GET", "users/{user_id}/stars",
                       url_params={"user_id": user_id},
                       query_params=extra_query_params)

    def user_stars_count(self, user_id, extra_query_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.user_stars_count(5)
        client.user_stars_count(5, {"since": "2017-05-01", "until": "2017-05-31"})
        """
        return self.do("GET", "users/{user_id}/stars/count",
                       url_params={"user_id": user_id},
                       query_params=extra_query_params)

    def star(self, query_params):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.star({"issueId": 333})
        """
        return self.do("POST", "stars",
                       query_params=query_params)

    def wikis(self, project_id_or_key):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.wikis(3)
        """
        return self.do("GET", "wikis",
                       query_params={"projectIdOrKey": project_id_or_key})

    def wiki(self, wiki_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.wiki(3)
        """
        return self.do("GET", "wikis/{wiki_id}", url_params={"wiki_id": wiki_id})

    def update_wiki(self, wiki_id, extra_request_params={}):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.update_wiki(3, {"name": "test", "content": "content test", "mailNotify": "true"})
        """
        request_params = extra_request_params
        return self.do("PATCH", "wikis/{wiki_id}", url_params={"wiki_id": wiki_id}, request_params=request_params)
                       
    def wiki_history(self, wiki_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.wiki_history(3)
        """
        return self.do("GET", "wikis/{wiki_id}/history", url_params={"wiki_id": wiki_id})

    def wiki_stars(self, wiki_id):
        """
        client = BacklogClient("your_space_name", "your_api_key")
        client.wiki_stars(3)
        """
        return self.do("GET", "wikis/{wiki_id}/stars", url_params={"wiki_id": wiki_id})

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

    def get_issue_id(self, issue_key):
        issue = self.issue(issue_key)
        if issue:
            return int(issue[u"id"])
        return None

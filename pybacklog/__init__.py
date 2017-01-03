# -*- coding: utf-8 -*-

import requests


class BacklogClient(object):
    endpoint = ""

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

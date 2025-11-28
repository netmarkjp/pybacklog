# -*- coding: utf-8 -*-

from pybacklog import BacklogClient
import os

_space = os.getenv("BACKLOG_SPACE", "")
_api_key = os.getenv("BACKLOG_API_KEY", "")
_project = os.getenv("BACKLOG_PROJECT", "")


client = BacklogClient(_space, _api_key)
activities = client.project_activities(_project, {"activityTypeId[]": [1, 2, 3, 14], "count": 100})

urls = []
items = []
if activities:
    for activity in activities:
        url = client.activity_to_issue_url(activity)
        if url in urls:
            continue
        if "None" in url:
            print(activity)
            continue
        urls.append(url)

        item = (activity.get("created"), url, activity.get("content").get("summary"))
        items.append(item)

for item in items:
    print("{date}\t{url}\t{summary}".format(date=item[0], url=item[1], summary=item[2]))

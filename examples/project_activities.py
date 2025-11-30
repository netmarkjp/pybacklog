# -*- coding: utf-8 -*-

from typing import List, Tuple

from pybacklog import BacklogClient
import os

_space = os.getenv("BACKLOG_SPACE", "")
_api_key = os.getenv("BACKLOG_API_KEY", "")
_project = os.getenv("BACKLOG_PROJECT", "")


client = BacklogClient(_space, _api_key)
activities = client.do(
    "GET",
    "projects/{project_id_or_key}/activities",
    url_params={"project_id_or_key": _project},
    query_params={"activityTypeId[]": [1, 2, 3, 14], "count": 100},
)

urls: List[str] = []
items: List[Tuple[str, str, str]] = []
if activities:
    for activity in activities:
        if not isinstance(activity, dict):
            continue

        created = activity.get("created", "")

        url = client.activity_to_issue_url(activity)
        if url in urls:
            continue
        urls.append(url)

        try:
            summary = activity["content"]["summary"]
        except KeyError:
            summary = ""
        except TypeError:
            summary = ""

        item = (created, url, summary)
        items.append(item)

for item in items:
    print("{date}\t{url}\t{summary}".format(date=item[0], url=item[1], summary=item[2]))

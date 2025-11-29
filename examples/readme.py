from pybacklog import BacklogClient
import os

YOUR_SPACE_NAME = os.getenv("BACKLOG_SPACE_NAME", "")
YOUR_API_KEY = os.getenv("BACKLOG_API_KEY", "")
YOUR_PROJECT = os.getenv("BACKLOG_PROJECT", "")
YOUR_ISSUE_KEY = os.getenv("BACKLOG_ISSUE_KEY", "")

client = BacklogClient(YOUR_SPACE_NAME, YOUR_API_KEY)

# space
space = client.space()
print(space.get("spaceKey"))

# project
projects = client.projects()

# activity
activities = client.project_activities(YOUR_PROJECT, {"activityTypeId[]": [1, 2]})

# list issue
project_id = client.get_project_id(YOUR_PROJECT)
issues = client.issues({"projectId[]": [project_id], "sort": "dueDate"})

# specified issue
issue = client.issue(YOUR_ISSUE_KEY)

# create issue
project_id = client.get_project_id(YOUR_PROJECT)
issue_type_id = client.project_issue_types(YOUR_PROJECT)[0]["id"]
priority_id = client.priorities()[0]["id"]

if project_id and issue_type_id and priority_id:
    client.create_issue(project_id, "some summary", issue_type_id, priority_id, {"description": "a is b and c or d."})

# add comment
client.add_issue_comment(YOUR_ISSUE_KEY, "or ... else e.")

# top 10 star collector
star_collectors = [
    (client.user_stars_count(u["id"], {"since": "2017-06-01", "until": "2017-06-30"})["count"], u["name"])
    for u in client.users()
]
star_collectors.sort()
star_collectors.reverse()

for i, (c, u) in enumerate(star_collectors[:10]):
    print(i + 1, c, u)

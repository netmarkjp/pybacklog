from pybacklog import BacklogClient
import os

YOUR_SPACE_NAME = os.getenv("BACKLOG_SPACE_NAME", "")
YOUR_API_KEY = os.getenv("BACKLOG_API_KEY", "")
YOUR_PROJECT = os.getenv("BACKLOG_PROJECT", "")

client = BacklogClient(YOUR_SPACE_NAME, YOUR_API_KEY)
space = client.do("GET", "space")  # GET /api/v2/space
projects = client.do("GET", "projects", query_params={"archived": False})  # GET /api/v2/projects?archived=false
activities = client.do(
    "GET",
    "projects/{project_id_or_key}/activities",
    url_params={"project_id_or_key": YOUR_PROJECT},
    query_params={"activityTypeId[]": [1, 2]},
)  # GET /api/v2/projects/myproj/activities?activityTypeIds%5B%5D=1&activityTypeIds%5B%5D=2

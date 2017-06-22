pybacklog
=================

Backlog API v2 Client Library for Python

[![Build Status](https://travis-ci.org/netmarkjp/pybacklog.svg?branch=master)](https://travis-ci.org/netmarkjp/pybacklog)

# Requirements

- Python 2.7
- Python 3.5

# Install

```
pip install pybacklog
```

# Usage

```python
from pybacklog import BacklogClient

client = BacklogClient("your_space_name", "your_api_key")

# space
space = client.do("GET", "space")  # GET /api/v2/space
print(space.get(u"spaceKey"))

# project
projects = client.projects()

# activity
activities = client.project_activities("YOUR_PROJECT", {"activityTypeId[]": [1, 2]})

# list issue
project_id = client.get_project_id("YOUR_PROJECT")
issues = client.issues({"projectId[]":[project_id], "sort": "dueDate"})

# specified issue
issue = client.issue("YOUR_PROJECT-999")

# create issue
project_id = client.get_project_id(project_key)
issue_type_id = client.issue_types(project_key)[0][u"id"]
priority_id = client.priorities()[0][u"id"]

client.create_issue(project_id,
                    u"some summary",
                    issue_type_id,
                    priority_id,
                    {"description": u"a is b and c or d."})

# add comment
client.add_comment("YOUR_PROJECT-999", u"or ... else e.")
```

extra parameters are here
=> [Backlog API Overview \| Backlog Developer API \| Nulab](https://developer.nulab-inc.com/docs/backlog/)

# Unsupported operations ?

Use `do` or let's write code and Pull Request.

```python
from pybacklog import BacklogClient

client = BacklogClient("your_space_name", "your_api_key")
space = client.do("GET", "space")  # GET /api/v2/space
projects = client.do("GET", "projects",
          query_params={"archived": false}
          )  # GET /api/v2/projects?archived=false
activities = client.do("GET", "projects/{project_id_or_key}/activities",
          url_params={"project_id_or_key": "myproj"},
          query_params={"activityTypeId[]": [1, 2]}
          )  # GET /api/v2/projects/myproj/activities?activityTypeIds%5B%5D=1&activityTypeIds%5B%5D=2
```

see also [Backlog API Overview \| Backlog Developer API \| Nulab](https://developer.nulab-inc.com/docs/backlog/)

# Development

```
pip install -r requirements.txt
pip install -r requirements_dev.txt

PYTHONPATH=. python -m unittest tests
```

# License

Copyright 2017 Toshiaki Baba

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

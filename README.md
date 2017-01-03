pybacklog
=================

Backlog API v2 Client Library for Python

[![Build Status](https://travis-ci.org/netmarkjp/pybacklog.svg?branch=master)](https://travis-ci.org/netmarkjp/pybacklog)

# Requirements

- Python 2.7
- Python 3.5

# Usage

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

print(space.get(u"spaceKey"))
```

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

# Ace Data Cloud Scaffold

Install:

```
pip install acedatacloud-scaffold
```

Sample:

```python
from acedatacloud_scaffold import BaseController as Controller
from acedatacloud_scaffold import BaseHandler
import json


class Handler(BaseHandler):

    async def get(self, id=None):
        result = {
            'value': id
        }
        self.write(json.dumps(result))


controller = Controller()
controller.add_handler(r'/test/(.*)', Handler)

controller.start()
```

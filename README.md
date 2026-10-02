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

Forwarding logs retain the handler's trace context, request method, response
status, and aggregate response byte/chunk counts. Request URLs, parameters,
headers, bodies, response headers, and individual response chunks are not logged.
Forwarded data and headers are unchanged. The response summary is emitted only
after the stream completes; interrupted streams still propagate their error.

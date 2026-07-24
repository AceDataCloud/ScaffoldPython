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

## Execute-only ownership

Cluster-local resource owners can request execution without PlatformGateway
usage recording. The shared handler recognizes only this contract:

```http
X-Ace-Execution-Owner: x402
```

`BaseHandler.record()` skips its `/record` call for that owner. Missing, empty,
or unknown owner values keep the normal recording path. Workers must still avoid
task persistence and callbacks before publishing asynchronous operations through
an execute-only owner.

This is a reserved cluster-internal header. Every public ingress or gateway must
remove client-supplied `X-Ace-Execution-Owner` before forwarding to a worker.
Only direct cluster-local resource-owner calls may carry it.

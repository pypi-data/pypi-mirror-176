# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zonis', 'zonis.client', 'zonis.server']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'zonis',
    'version': '0.1.0',
    'description': 'Agnostic IPC for Python programs ',
    'long_description': 'Zonis\n---\n\nA coro based callback system for many to one IPC setups.\n\n#### Examples\n\n##### Simple\n\n*Client*\n\n```python\nimport asyncio\n\nfrom zonis.client import Client\n\nasync def main():\n    client = Client()\n    \n    @client.route()\n    async def ping():\n        return "ping"\n    \n    await client.start()\n\nasyncio.run(main())\n```\n\n*Server*\n\n```python\nimport json\nimport asyncio\n\nfrom fastapi import FastAPI\nfrom starlette.websockets import WebSocket, WebSocketDisconnect\n\nfrom zonis import BaseZonisException\nfrom zonis.server import Server\n\napp = FastAPI()\nserver = Server()\n\n@app.get("/")\nasync def index():\n    response = await server.request("ping")\n    return {"data": response} # Returns pong\n\n@app.websocket("/ws")\nasync def websocket_endpoint(websocket: WebSocket):\n    await websocket.accept()\n    d: str = await websocket.receive_text()\n    try:\n        identifier = await server.parse_identify(json.loads(d), websocket)\n    except BaseZonisException:\n        print("WS failed to identify")\n        return\n\n    try:\n        await asyncio.Future()\n    except WebSocketDisconnect:\n        server.disconnect(identifier)\n\n```\n\n---\n\n##### Multiple clients\n\n*Client one*\n\n```python\nimport asyncio\n\nfrom zonis.client import Client\n\nasync def main():\n    client = Client(identifier="one")\n    \n    @client.route()\n    async def ping():\n        return f"ping {client.identifier}"\n    \n    await client.start()\n\nasyncio.run(main())\n```\n\n*Client two*\n\n```python\nimport asyncio\n\nfrom zonis.client import Client\n\nasync def main():\n    client = Client(identifier="two")\n    \n    @client.route()\n    async def ping():\n        return f"ping {client.identifier}"\n    \n    await client.start()\n\nasyncio.run(main())\n```\n\n*Server*\n\n```python\nfrom fastapi import FastAPI\n\nfrom zonis.server import Server\n\napp = FastAPI()\nserver = Server()\n\n@app.on_event("startup")\nasync def startup_event():\n    await server.start()\n\n@app.get("/")\nasync def index():\n    response = await server.request_all("ping")\n    return {"data": response} # Returns {"data": {"one": "pong one", "two": "pong two"}}\n\n@app.get("/one")\nasync def one():\n    response = await server.request("ping", client_identifier="one")\n    return {"data": response} # Returns {"data": "pong one"}\n```',
    'author': 'skelmis',
    'author_email': 'ethan@koldfusion.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

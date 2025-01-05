#!/usr/bin/env python

"""Echo server using the asyncio API."""

import json
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Json
from websockets.asyncio.server import serve

from bot import generate_action

app = FastAPI()


class ActionRequest(BaseModel):
    state: Json[Any]


@app.post("/get-action")
async def get_action(req: ActionRequest):
    state = json.loads(req.state)
    print(state)
    action = generate_action(state)
    print(action)
    # await websocket.send(json.dumps(action))

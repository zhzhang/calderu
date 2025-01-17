#!/usr/bin/env python

"""Echo server using the asyncio API."""

import json
from typing import Any

from fastapi import FastAPI, Request

from bot import generate_action

app = FastAPI()


@app.post("/")
async def get_action(request: Request):
    state = await request.json()
    print(state)
    action = generate_action(state)
    print(action)
    return action

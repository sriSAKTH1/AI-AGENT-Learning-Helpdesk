from contextlib import asynccontextmanager
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langgraph.types import Command

from backend.app_graph import runtime
from agents.human_gateway import human_requests

from backend.response import format_agent_response

from persistence.moderator_db import (
    get_pending_requests,
    complete_request,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await runtime.startup()
    yield
    await runtime.shutdown()


app = FastAPI(
    title="AI Learning Helpdesk",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    user_id: str
    thread_id: str
    message: str


class HumanActionRequest(BaseModel):
    thread_id: str
    action: str


class ModeratorActionRequest(BaseModel):
    thread_id: str
    action: str


@app.get("/")
async def root():
    return {
        "message": "AI Learning Helpdesk API is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = await runtime.graph.ainvoke(
        {
            "user_id": request.user_id,
            "thread_id": request.thread_id,
            "question": request.message,
        },
        config=config,
    )

    if "__interrupt__" in result:
        return result

    return format_agent_response(result)


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    async def event_generator():

        try:

            async for event in runtime.graph.astream(
                {
                    "user_id": request.user_id,
                    "thread_id": request.thread_id,
                    "question": request.message,
                },
                config=config,
                stream_mode="updates",
            ):

                yield json.dumps(
                    {
                        "type": "update",
                        "data": event,
                    },
                    default=str,
                ) + "\n"

            yield json.dumps(
                {
                    "type": "done"
                }
            ) + "\n"

        except Exception as error:

            yield json.dumps(
                {
                    "type": "error",
                    "message": str(error),
                }
            ) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
    )


@app.post("/human/action")
async def human_action(request: HumanActionRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = await runtime.graph.ainvoke(
        Command(resume=request.action),
        config=config,
    )

    return result


@app.post("/moderator/action")
async def moderator_action(
    request: ModeratorActionRequest
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = await runtime.graph.ainvoke(
        Command(resume=request.action),
        config=config,
    )

    complete_request(
        request.thread_id,
        request.action,
    )

    return result

@app.get("/moderator/pending")
async def moderator_pending():

    return {
        "pending": get_pending_requests()
    }
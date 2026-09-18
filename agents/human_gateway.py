from datetime import datetime, timezone
from uuid import uuid4

from persistence.moderator_db import add_moderator_request


human_requests = []


async def create_mentor_request(
    user_id: str,
    question: str,
    reason: str,
    answer: str = "",
):
    request = {
        "request_id": str(uuid4()),
        "type": "mentor",
        "user_id": user_id,
        "question": question,
        "reason": reason,
        "draft_answer": answer,
        "status": "pending",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    human_requests.append(request)

    return request


async def create_moderator_request(
    user_id: str,
    question: str,
    reason: str,
    thread_id: str,
):
    request = {
        "request_id": str(uuid4()),
        "type": "moderator",
        "thread_id": thread_id,
        "user_id": user_id,
        "question": question,
        "reason": reason,
        "status": "pending",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    human_requests.append(request)

    add_moderator_request(
        request_id=request["request_id"],
        thread_id=thread_id,
        user_id=user_id,
        question=question,
        reason=reason,
    )

    print(">>> MODERATOR REQUEST CREATED <<<")
    print(request)

    return request
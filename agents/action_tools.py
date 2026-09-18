from uuid import uuid4


async def create_support_request(
    user_id: str,
    question: str,
):
    """
    Create a support request for a learner.

    This action must only execute after explicit
    human approval.
    """

    return {
        "ticket_id": str(uuid4()),
        "user_id": user_id,
        "question": question,
        "status": "created",
    }
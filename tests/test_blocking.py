from agents.blocking import (
    block_user,
    is_user_blocked,
    get_blocked_until,
    unblock_user,
)


def test_user_blocking():

    user_id = "test_block_user"

    unblock_user(user_id)

    assert is_user_blocked(user_id) is False

    blocked_until = block_user(user_id)

    assert blocked_until is not None

    assert is_user_blocked(user_id) is True

    assert get_blocked_until(user_id) is not None

    unblock_user(user_id)

    assert is_user_blocked(user_id) is False
from backend.model_runner import (
    is_retryable_error,
    is_quota_error,
)


def test_quota_error():
    error = Exception(
        "429 RESOURCE_EXHAUSTED quota exceeded"
    )

    assert is_quota_error(error)


def test_server_error_is_retryable():
    error = Exception(
        "503 Service Unavailable"
    )

    assert is_retryable_error(error)


def test_timeout_is_retryable():
    error = Exception(
        "Request timed out"
    )

    assert is_retryable_error(error)


def test_bad_request_is_not_retryable():
    error = Exception(
        "400 Invalid request"
    )

    assert not is_retryable_error(error)


def test_not_found_is_not_retryable():
    error = Exception(
        "404 model not found"
    )

    assert not is_retryable_error(error)

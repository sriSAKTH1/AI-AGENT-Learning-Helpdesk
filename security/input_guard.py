import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"forget\s+(all\s+)?(your\s+)?instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?(your\s+)?system\s+prompt",
    r"print\s+(your\s+)?system\s+prompt",
    r"reveal\s+hidden\s+configuration",
    r"show\s+hidden\s+configuration",
    r"reveal\s+(your\s+)?api\s+key",
    r"show\s+(me\s+)?(your\s+)?api\s+key",
    r"environment\s+variables",
    r"bypass\s+(your\s+)?safety",
    r"bypass\s+(your\s+)?security",
    r"unrestricted\s+ai",
    r"call\s+every\s+available\s+tool",
    r"override\s+(the\s+)?ai\s+learning\s+helpdesk\s+scope",
    r"ignore\s+(the\s+)?moderator\s+requirement",
    r"behave\s+as\s+a\s+general[- ]purpose\s+assistant",

    # RAG injection
    r"ignore\s+(the\s+)?rag\s+context",
    r"disregard\s+(the\s+)?rag\s+context",
    r"ignore\s+(the\s+)?retrieved\s+context",
    r"follow\s+my\s+instructions\s+instead",
]


def detect_prompt_injection(question: str) -> bool:
    text = question.lower().strip()

    return any(
        re.search(pattern, text)
        for pattern in INJECTION_PATTERNS
    )


def security_check(question: str) -> dict:
    if detect_prompt_injection(question):
        return {
            "blocked": True,
            "reason": "Potential prompt injection detected.",
        }

    return {
        "blocked": False,
        "reason": None,
    }

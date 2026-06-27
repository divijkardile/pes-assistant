import uuid


def generate_session_id() -> str:
    return str(uuid.uuid4())


def generate_correlation_id() -> str:
    return str(uuid.uuid4())
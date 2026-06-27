class Roles:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class SessionConstants:
    DEFAULT_TIMEOUT_MINUTES = 30


class LogMessages:
    SESSION_CREATED = "Session created."
    SESSION_UPDATED = "Session updated."
    SESSION_ENDED = "Session ended."

    EXECUTING_ORCHESTRATOR = "Executing OrchestratorAgent."
    EXECUTING_DATA_AGENT = "Executing DataAgent."
    EXECUTING_DOCUMENT_AGENT = "Executing DocumentAgent."

    LOADING_PLAN_DATA = "Loading structured plan data."
    SEARCHING_DOCUMENTS = "Searching plan documents."
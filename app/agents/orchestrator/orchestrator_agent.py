import logging
import re

from app.agents.base.base_agent import BaseAgent
from app.config.settings import get_settings
from app.llm.interfaces.llm_provider import LLMProvider
from app.models.agent_state import AgentState
from app.prompts.orchestrator_prompt import SYSTEM_PROMPT


class OrchestratorAgent(BaseAgent):

    # Patterns for greeting and casual messages
    GREETING_PATTERNS = [
        r"^\s*(hi|hello|hey|greetings|good\s+(morning|afternoon|evening|day))\s*[!?.]?\s*$",
        r"^\s*(how\s+are\s+you|how's\s+it\s+going|what's\s+up|sup|yo)\s*[!?.]?\s*$",
        r"^\s*(thank\s+you|thanks|thank\s+you\s+so\s+much|appreciate\s+it)\s*[!?.]?\s*$",
        r"^\s*(okay|ok|got\s+it|understood|sure|alright|cool|nice)\s*[!?.]?\s*$",
        r"^\s*(goodbye|bye|see\s+you|farewell|talk\s+soon)\s*[!?.]?\s*$",
        r"^\s*(please|help|assistance)\s*[!?.]?\s*$",
        r"^\s*(yes|no)\s*[!?.]?\s*$",
    ]

    GREETING_RESPONSES = {
        "greeting": (
            "Hello! I'm your retirement planning assistant. "
            "I'm here to help you with questions about your retirement plan. "
            "What would you like to know?"
        ),
        "how_are_you": (
            "I'm doing great, thank you for asking! I'm here and ready to help "
            "you with any questions about your retirement plan. What can I assist you with?"
        ),
        "thanks": (
            "You're welcome! I'm happy to help. Is there anything else you'd like to know "
            "about your retirement plan?"
        ),
        "okay": (
            "Great! Feel free to ask me anything about your retirement plan. I'm here to help."
        ),
        "goodbye": (
            "Thank you for chatting with me! Have a great day, and feel free to reach out anytime "
            "if you have more retirement plan questions."
        ),
        "help": (
            "Of course! I'm here to help. Ask me any questions about your retirement plan, "
            "your benefits, eligibility, investments, or plan policies."
        ),
        "yes_no": (
            "I'm ready to help! Please go ahead and ask your question about your retirement plan."
        ),
    }

    def __init__(
        self,
        *,
        logger: logging.Logger,
        llm_provider: LLMProvider,
        data_agent_tool,
        document_agent_tool,
    ) -> None:

        super().__init__(
            logger=logger,
            llm_provider=llm_provider,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                data_agent_tool,
                document_agent_tool,
            ],
        )

    def _is_greeting_or_casual(self, message: str) -> tuple[bool, str]:
        """
        Detect if the message is a greeting or casual conversation.
        
        Returns:
            tuple: (is_greeting: bool, response_type: str)
        """
        cleaned_message = message.strip().lower()
        
        # Don't process empty messages
        if not cleaned_message or len(cleaned_message) < 2:
            return False, ""
        
        # Remove extra punctuation for matching
        cleaned_message_stripped = re.sub(r'[!?.,;:]+$', '', cleaned_message)
        
        # Check for "how are you" patterns
        if re.search(r"how\s+are\s+you|how's\s+it\s+going|what's\s+up|howdy|how\s+ya", cleaned_message):
            return True, "how_are_you"
        
        # Check for thank you patterns
        if re.search(r"thank\s+you|thanks|thank\s+you\s+so\s+much|appreciate|appreciated", cleaned_message):
            return True, "thanks"
        
        # Check for goodbye patterns
        if re.search(r"goodbye|bye|see\s+you|farewell|talk\s+soon|catch\s+you|take\s+care", cleaned_message):
            return True, "goodbye"
        
        # Check for help request patterns (standalone "help")
        if re.match(r"^\s*(please\s+)?help\s*[!?.]?\s*$", cleaned_message_stripped):
            return True, "help"
        
        # Check for yes/no only
        if re.match(r"^\s*(yes|no|yep|nope|yeah|nah)\s*[!?.]?\s*$", cleaned_message_stripped):
            return True, "yes_no"
        
        # Check for simple greetings (hi, hello, hey)
        if re.match(r"^\s*(hi|hello|hey|greetings|good\s+(morning|afternoon|evening|day|night)|welcome|howdy)\s*[!?.]?\s*$", cleaned_message_stripped):
            return True, "greeting"
        
        # Check for acknowledgments (okay, sure, cool, nice, alright)
        if re.match(r"^\s*(okay|ok|got\s+it|understood|sure|alright|cool|nice|great|awesome|perfect)\s*[!?.]?\s*$", cleaned_message_stripped):
            return True, "okay"
        
        return False, ""

    def _get_greeting_response(self, response_type: str) -> str:
        """Get an appropriate greeting response."""
        return self.GREETING_RESPONSES.get(response_type, self.GREETING_RESPONSES["greeting"])

    def _clean_response(self, response: str) -> str:
        """
        Clean response to remove internal notes and explanations.
        Ensures response is participant-friendly only.
        """
        # Remove lines starting with (Note: or Note: or any internal metadata
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip internal notes and explanations
            if re.match(r'^\s*\(Note:', line, re.IGNORECASE):
                continue
            if re.match(r"^\s*\(I'?ve decided", line, re.IGNORECASE):
                continue
            if re.match(r"^\s*\(The (tool|agent|system)", line, re.IGNORECASE):
                continue
            if re.match(r"^\s*\(Instead,", line, re.IGNORECASE):
                continue
            if line.strip():  # Only add non-empty lines
                cleaned_lines.append(line)
        
        # Join and clean up extra whitespace
        cleaned_response = '\n'.join(cleaned_lines).strip()
        
        # If entire response is now empty, return a friendly default
        if not cleaned_response:
            return "I'm here to help! Please feel free to ask me any questions about your retirement plan."
        
        return cleaned_response

    async def invoke(
        self,
        *,
        state: AgentState,
        user_message: str,
    ) -> str:

        self._logger.info(
            "Executing OrchestratorAgent for session '%s'.",
            state.session_id,
        )

        state.agent_responses.clear()

        # Check if message is a greeting or casual conversation
        is_greeting, response_type = self._is_greeting_or_casual(user_message)
        if is_greeting:
            self._logger.info(
                "Detected greeting/casual message in session '%s'. Type: %s",
                state.session_id,
                response_type,
            )
            greeting_response = self._get_greeting_response(response_type)
            self._logger.info(
                "OrchestratorAgent completed (greeting) for session '%s'.",
                state.session_id,
            )
            return greeting_response

        # Initialize tool call tracking for loop detection
        settings = get_settings()
        tool_call_history: dict[str, int] = {}
        loop_detection_enabled = settings.enable_loop_detection
        loop_threshold = settings.loop_detection_threshold

        prompt = f"""
Session Context
===============

Session Id:
{state.session_id}

Plan Number:
{state.plan_context.plan_num}

User Id:
{state.plan_context.user_id}

Conversation Summary
====================

{state.conversation_summary.summary or "No conversation summary available."}

Recent Conversation
===================

{state.messages}

Current User Question
=====================

{user_message}

Instructions
============

You are the lead retirement assistant.

You have access to two specialist tools:

1. data_agent - Retrieves structured participant and plan information.
2. document_agent - Searches retirement plan documents.

Your Response MUST:
- Answer ONLY the participant's question
- Contain ONLY the participant-facing response
- Have NO internal notes, explanations, or metadata
- Have NO mentions of tools, decisions, or implementation details

Response Rules:

1. Analyze the user's question.
2. Decide which tool(s) are required (data_agent, document_agent, or both).
3. Call the appropriate tool(s).
4. Combine tool responses into one natural answer.
5. Return ONLY the final answer, nothing else.

CRITICAL: Your entire response must be suitable to show directly to the participant.

Do not include:
- "(Note: I decided...)"
- "The tool returned..."
- "I've decided not to use..."
- Any explanations about your decision-making
- Any metadata about tool calls
- Any internal process information

Return ONLY the participant-facing answer.
"""

        answer = await self._execute(
            prompt=prompt,
        )

        # Clean response to remove any internal notes or metadata
        answer = self._clean_response(answer)

        # Log loop detection warnings if enabled
        if loop_detection_enabled and state.agent_responses:
            for response in state.agent_responses:
                agent_name = response.agent_name
                tool_call_history[agent_name] = (
                    tool_call_history.get(agent_name, 0) + 1
                )

                if (
                    tool_call_history[agent_name] > loop_threshold
                ):
                    self._logger.warning(
                        (
                            f"Possible infinite loop detected: "
                            f"'{agent_name}' called "
                            f"{tool_call_history[agent_name]} times in "
                            f"session {state.session_id}"
                        )
                    )

        self._logger.info(
            "OrchestratorAgent completed for session '%s'.",
            state.session_id,
        )

        return answer
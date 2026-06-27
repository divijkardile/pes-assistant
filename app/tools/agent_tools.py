from strands import tool

from app.agents.data.data_agent import DataAgent
from app.agents.document.document_agent import DocumentAgent
from app.models.agent_state import AgentState


def create_data_agent_tool(
    data_agent: DataAgent,
):

    @tool(
        name="data_agent",
        description="""
Use this specialist to answer questions using structured retirement
plan and participant data.

Examples:
- Contributions
- Employer Match
- Investments
- Eligibility
- Vesting
- Loans
- Withdrawals
- Payroll
- Beneficiaries
- Account Balance
- Participant Information
""",
    )
    async def data_agent_tool(
        question: str,
        state: AgentState,
    ) -> str:

        response = await data_agent.invoke(
            state=state,
            user_message=question,
        )

        return response.answer

    return data_agent_tool


def create_document_agent_tool(
    document_agent: DocumentAgent,
):

    @tool(
        name="document_agent",
        description="""
Use this specialist to answer questions using retirement plan
documents.

Examples:
- Summary Plan Description (SPD)
- Plan Rules
- Notices
- Policies
- Legal wording
- PDFs
- Document explanations
""",
    )
    async def document_agent_tool(
        question: str,
        state: AgentState,
    ) -> str:

        response = await document_agent.invoke(
            state=state,
            user_message=question,
        )

        return response.answer

    return document_agent_tool
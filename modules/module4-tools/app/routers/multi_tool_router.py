from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.advanced.multi_tool_agent import multi_tool_agent

router = APIRouter(tags=["Multi-Tool Agent"])

class MultiToolRequest(BaseModel):
    input_data: str = Field(
        ...,
        description=(
            "Input string for the multi-tool agent. "
            "Format: 'num1,num2;text_for_uppercase;message_for_echo'\n\n"
            "Sample: '2,3;hello;world'"
        )
    )

@router.post(
    "/multi-tool",
    summary="Run multi-tool agent",
    description=(
        "Purpose: Executes the multi-tool agent to process input using multiple tools and aggregate results.\n\n"
        "Sample Input: { 'input_data': '2,3;hello;world' }\n"
        "Sample Output: { 'math_result': 5.0, 'uppercase_result': 'HELLO', 'echo_result': 'Echo: world' }"
    )
)
async def multi_tool_endpoint(request: MultiToolRequest, api_key: str = Depends(verify_api_key)):
    result = multi_tool_agent.run(request.input_data)
    return result

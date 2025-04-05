from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.advanced.financial_summary_agent import financial_summary_agent



router = APIRouter(tags=["Financial Summary Agent"])

class FinancialSummaryRequest(BaseModel):
    input_data: str = Field(
        ...,
        description=(
            "Input string for the financial summary agent in the format: "
            "'principal,rate,time;message'.\n\n"
            "For example: '1000,0.05,2;thank you'"
        )
    )

@router.post(
    "/financial_summary",
    summary="Generate Financial Summary",
    description=(
        "Purpose: Calculate simple interest and total amount, and process a message.\n\n"
        "Sample Input: { 'input_data': '1000,0.05,2;thank you' }\n\n"
        "Sample Output: { 'interest': 100.0, 'total': 1100.0, 'message': 'Echo: THANK YOU' }"
    )
)
async def financial_summary_endpoint(request: FinancialSummaryRequest, api_key: str = Depends(verify_api_key)):
    result = financial_summary_agent.run(request.input_data)
    return result

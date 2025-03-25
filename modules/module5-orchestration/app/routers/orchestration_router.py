"""
FastAPI router for orchestration-related endpoints.

This module contains API endpoints for input/output guardrails, handoffs,
and tracing functionality.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from agents.guardrail import InputGuardrailResult, OutputGuardrailResult
from app.agents.orchestration.guardrail_agent import create_guardrail_agent

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/agents/orchestration",
    tags=["Orchestration"],
)

class OrchestrationRequest(BaseModel):
    """Base model for orchestration requests."""
    message: str
    context: Optional[Dict[str, Any]] = None

class GuardrailResponse(BaseModel):
    """Model for guardrail responses."""
    status: str
    response: Optional[str] = None
    guardrail_triggered: bool = False
    tripwire_message: Optional[str] = None
    trace_id: Optional[str] = None

@router.post("/input-guardrails")
async def input_guardrails_endpoint(request: OrchestrationRequest):
    """
    Endpoint for validating user inputs using input guardrails.
    
    Args:
        request: The orchestration request.
        
    Returns:
        A guardrail response.
    """
    logger.info(f"Processing input guardrail request: {request.message[:50]}...")
    
    try:
        # Create a guardrail agent
        agent = create_guardrail_agent()
        
        # Run the agent with the input guardrails
        response = await agent.run(request.message)
        
        return GuardrailResponse(
            status="success",
            response=response,
            guardrail_triggered=False,
            trace_id=f"trace-{id(agent)}"
        )
    except Exception as e:
        logger.error(f"Input guardrail triggered: {str(e)}")
        
        # Extract the tripwire message if available
        tripwire_message = str(e)
        
        return GuardrailResponse(
            status="error",
            guardrail_triggered=True,
            tripwire_message=tripwire_message,
            trace_id=f"trace-error-{id(request)}"
        )

@router.post("/output-guardrails")
async def output_guardrails_endpoint(request: OrchestrationRequest):
    """
    Endpoint for validating agent outputs using output guardrails.
    
    Args:
        request: The orchestration request.
        
    Returns:
        A guardrail response.
    """
    logger.info(f"Processing output guardrail request: {request.message[:50]}...")
    
    try:
        # Create a guardrail agent
        agent = create_guardrail_agent()
        
        # Run the agent to get a response
        response = await agent.run(request.message)
        
        return GuardrailResponse(
            status="success",
            response=response,
            guardrail_triggered=False,
            trace_id=f"trace-{id(agent)}"
        )
    except Exception as e:
        logger.error(f"Output guardrail triggered: {str(e)}")
        
        # Extract the tripwire message if available
        tripwire_message = str(e)
        
        return GuardrailResponse(
            status="error",
            guardrail_triggered=True,
            tripwire_message=tripwire_message,
            trace_id=f"trace-error-{id(request)}"
        )

@router.post("/guardrails/test-input")
async def test_input_guardrail_endpoint(request: OrchestrationRequest):
    """
    Endpoint for testing input guardrails with specific test cases.
    
    Args:
        request: The orchestration request.
        
    Returns:
        A guardrail response.
    """
    logger.info(f"Testing input guardrail with: {request.message[:50]}...")
    
    # Create a guardrail agent with only input guardrails
    from app.agents.orchestration.input_guardrails import (
        validate_empty_input,
        validate_input_length,
        validate_harmful_content,
        validate_inappropriate_language,
    )
    
    agent = create_guardrail_agent(
        input_guardrails=[
            validate_empty_input,
            validate_input_length,
            validate_harmful_content,
            validate_inappropriate_language,
        ],
        output_guardrails=[]
    )
    
    try:
        # Run the agent with the input guardrails
        response = await agent.run(request.message)
        
        return GuardrailResponse(
            status="success",
            response="Input passed all guardrails",
            guardrail_triggered=False,
            trace_id=f"trace-{id(agent)}"
        )
    except Exception as e:
        logger.error(f"Input guardrail triggered during test: {str(e)}")
        
        return GuardrailResponse(
            status="error",
            guardrail_triggered=True,
            tripwire_message=str(e),
            trace_id=f"trace-error-{id(request)}"
        )

@router.post("/guardrails/test-output")
async def test_output_guardrail_endpoint(request: OrchestrationRequest):
    """
    Endpoint for testing output guardrails with specific test cases.
    
    Args:
        request: The orchestration request.
        
    Returns:
        A guardrail response.
    """
    logger.info(f"Testing output guardrail with: {request.message[:50]}...")
    
    # Create a mock output to test the output guardrails
    mock_output = request.message
    
    # Create a guardrail agent with only output guardrails
    from app.agents.orchestration.output_guardrails import (
        validate_output_not_empty,
        validate_output_length,
        validate_no_error_in_output,
        validate_output_format,
    )
    
    # Test each output guardrail individually
    results = []
    
    for guardrail in [
        validate_output_not_empty,
        validate_output_length,
        validate_no_error_in_output,
        validate_output_format,
    ]:
        try:
            # Create a context and agent for testing
            from agents import RunContextWrapper, Agent
            context = RunContextWrapper()
            agent = Agent()
            
            # Run the guardrail on the mock output
            result = await guardrail(context, agent, mock_output)
            
            if result.tripwire_triggered:
                results.append({
                    "guardrail": guardrail.__name__,
                    "triggered": True,
                    "message": result.message
                })
            else:
                results.append({
                    "guardrail": guardrail.__name__,
                    "triggered": False
                })
        except Exception as e:
            results.append({
                "guardrail": guardrail.__name__,
                "triggered": True,
                "message": str(e),
                "error": True
            })
    
    # Check if any guardrails were triggered
    triggered = any(result["triggered"] for result in results)
    
    return GuardrailResponse(
        status="error" if triggered else "success",
        response=str(results),
        guardrail_triggered=triggered,
        tripwire_message=next((result["message"] for result in results if result["triggered"]), None),
        trace_id=f"trace-test-{id(request)}"
    )

@router.post("/handoffs")
async def handoffs_endpoint(request: OrchestrationRequest):
    """
    Endpoint for handling agent-to-agent handoffs.
    
    Args:
        request: The orchestration request.
        
    Returns:
        A guardrail response.
    """
    # Placeholder implementation
    return GuardrailResponse(
        status="success",
        response="Handoffs placeholder",
        guardrail_triggered=False,
        trace_id=f"trace-placeholder-{id(request)}"
    )

@router.get("/trace-status")
async def trace_status_endpoint():
    """
    Endpoint for checking trace status.
    
    Returns:
        A guardrail response.
    """
    # Placeholder implementation
    return GuardrailResponse(
        status="success",
        response="Trace status placeholder",
        guardrail_triggered=False,
        trace_id="trace-placeholder-abc"
    )
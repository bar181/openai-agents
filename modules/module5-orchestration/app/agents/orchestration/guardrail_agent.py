"""
Guardrail agent for validating user inputs and agent outputs.

This module contains an agent that uses input and output guardrails
to ensure safe and compliant interactions.
"""

import logging
from typing import List, Optional
from agents import Agent
from app.agents.orchestration.input_guardrails import (
    validate_empty_input,
    validate_input_length,
    validate_harmful_content,
    validate_inappropriate_language,
)
from app.agents.orchestration.output_guardrails import (
    validate_output_not_empty,
    validate_output_length,
    validate_no_error_in_output,
    validate_output_format,
)

logger = logging.getLogger(__name__)

class GuardrailAgent(Agent):
    """
    Agent with input and output guardrails for safe and compliant interactions.
    
    This agent applies various guardrails to validate user inputs and agent outputs,
    ensuring they meet predefined safety and compliance standards.
    """
    
    def __init__(
        self,
        name: str = "GuardrailAgent",
        instructions: str = "I am an agent with guardrails to ensure safe and compliant interactions.",
        model: str = "gpt-4",
        input_guardrails: Optional[List] = None,
        output_guardrails: Optional[List] = None,
        **kwargs
    ):
        """
        Initialize the GuardrailAgent.
        
        Args:
            name: The name of the agent.
            instructions: The instructions for the agent.
            model: The model to use for the agent.
            input_guardrails: Optional list of input guardrails to use.
            output_guardrails: Optional list of output guardrails to use.
            **kwargs: Additional arguments to pass to the Agent constructor.
        """
        # Default input guardrails if none provided
        if input_guardrails is None:
            input_guardrails = [
                validate_empty_input,
                validate_input_length,
                validate_harmful_content,
                validate_inappropriate_language,
            ]
        
        # Default output guardrails if none provided
        if output_guardrails is None:
            output_guardrails = [
                validate_output_not_empty,
                validate_output_length,
                validate_no_error_in_output,
                validate_output_format,
            ]
        
        super().__init__(
            name=name,
            instructions=instructions,
            model=model,
            input_guardrails=input_guardrails,
            output_guardrails=output_guardrails,
            **kwargs
        )
        
        logger.info(f"Initialized {name} with {len(input_guardrails)} input guardrails and {len(output_guardrails)} output guardrails")

def create_guardrail_agent(
    name: str = "GuardrailAgent",
    instructions: str = "I am an agent with guardrails to ensure safe and compliant interactions.",
    model: str = "gpt-4",
    input_guardrails: Optional[List] = None,
    output_guardrails: Optional[List] = None,
    **kwargs
) -> GuardrailAgent:
    """
    Create a GuardrailAgent with the specified configuration.
    
    Args:
        name: The name of the agent.
        instructions: The instructions for the agent.
        model: The model to use for the agent.
        input_guardrails: Optional list of input guardrails to use.
        output_guardrails: Optional list of output guardrails to use.
        **kwargs: Additional arguments to pass to the Agent constructor.
        
    Returns:
        A GuardrailAgent instance.
    """
    return GuardrailAgent(
        name=name,
        instructions=instructions,
        model=model,
        input_guardrails=input_guardrails,
        output_guardrails=output_guardrails,
        **kwargs
    )
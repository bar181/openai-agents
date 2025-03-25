"""
Input guardrails for validating user inputs before processing.

This module contains functions and decorators for implementing input guardrails
that validate user inputs against predefined criteria.
"""

import logging
from typing import Any
from agents import input_guardrail, RunContextWrapper, Agent
from agents.guardrail import GuardrailFunctionOutput

logger = logging.getLogger(__name__)

@input_guardrail()
async def validate_empty_input(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    """
    Validate that the user input is not empty.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        user_input: The user input to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    logger.info(f"Validating input is not empty: {user_input[:50]}...")
    
    if not user_input or len(user_input.strip()) == 0:
        logger.warning("Input is empty")
        return GuardrailFunctionOutput(
            output_info="Input cannot be empty.",
            tripwire_triggered=True
        )
    
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

@input_guardrail()
async def validate_input_length(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    """
    Validate that the user input is not too long.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        user_input: The user input to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    logger.info(f"Validating input length: {len(user_input)} characters")
    
    max_length = 1000  # Maximum allowed input length
    if len(user_input) > max_length:
        logger.warning(f"Input too long: {len(user_input)} characters")
        return GuardrailFunctionOutput(
            output_info=f"Input is too long ({len(user_input)} characters). Please limit your input to {max_length} characters.",
            tripwire_triggered=True
        )
    
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

@input_guardrail()
async def validate_harmful_content(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    """
    Validate that the user input does not contain harmful content.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        user_input: The user input to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    logger.info(f"Validating input for harmful content: {user_input[:50]}...")
    
    harmful_keywords = ["hack", "exploit", "illegal", "attack", "bypass security"]
    for keyword in harmful_keywords:
        if keyword in user_input.lower():
            logger.warning(f"Potentially harmful content detected: {keyword}")
            return GuardrailFunctionOutput(
                output_info=f"Your request contains potentially inappropriate content ({keyword}). "
                        "Please ensure your request complies with our usage policies.",
                tripwire_triggered=True
            )
    
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

@input_guardrail()
async def validate_inappropriate_language(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    """
    Validate that the user input does not contain inappropriate language.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        user_input: The user input to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    logger.info(f"Validating input for inappropriate language: {user_input[:50]}...")
    
    # In a real implementation, this would be a more comprehensive list
    inappropriate_words = ["profanity1", "profanity2", "slur1", "slur2"]
    for word in inappropriate_words:
        if word in user_input.lower():
            logger.warning(f"Inappropriate language detected: {word}")
            return GuardrailFunctionOutput(
                output_info="Your request contains inappropriate language. "
                        "Please rephrase your request using appropriate language.",
                tripwire_triggered=True
            )
    
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )
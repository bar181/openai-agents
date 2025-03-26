"""
Input guardrails for validating user inputs before processing.

This module contains functions and decorators for implementing input guardrails
that validate user inputs against predefined criteria.
"""

import logging
from typing import Any
from agents import input_guardrail, RunContextWrapper, Agent
from agents.guardrail import GuardrailFunctionOutput
from agents.tracing import get_current_trace

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
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_empty_input") as span:
        span.set_attribute("input_length", len(user_input))
        
        if not user_input or len(user_input.strip()) == 0:
            logger.warning("Input is empty")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", "Input cannot be empty")
            
            return GuardrailFunctionOutput(
                output_info="Input cannot be empty.",
                tripwire_triggered=True
            )
        
        span.set_attribute("tripwire_triggered", False)
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
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_input_length") as span:
        span.set_attribute("input_length", len(user_input))
        
        max_length = 1000  # Maximum allowed input length
        if len(user_input) > max_length:
            logger.warning(f"Input too long: {len(user_input)} characters")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", f"Input too long ({len(user_input)} characters)")
            span.set_attribute("max_length", max_length)
            
            return GuardrailFunctionOutput(
                output_info=f"Input is too long ({len(user_input)} characters). Please limit your input to {max_length} characters.",
                tripwire_triggered=True
            )
        
        span.set_attribute("tripwire_triggered", False)
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
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_harmful_content") as span:
        span.set_attribute("input_preview", user_input[:50])
        
        harmful_keywords = ["hack", "exploit", "illegal", "attack", "bypass security"]
        for keyword in harmful_keywords:
            if keyword in user_input.lower():
                logger.warning(f"Potentially harmful content detected: {keyword}")
                span.set_attribute("tripwire_triggered", True)
                span.set_attribute("reason", f"Harmful content detected: {keyword}")
                span.set_attribute("detected_keyword", keyword)
                
                return GuardrailFunctionOutput(
                    output_info=f"Your request contains potentially inappropriate content ({keyword}). "
                            "Please ensure your request complies with our usage policies.",
                    tripwire_triggered=True
                )
        
        span.set_attribute("tripwire_triggered", False)
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
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_inappropriate_language") as span:
        span.set_attribute("input_preview", user_input[:50])
        
        # In a real implementation, this would be a more comprehensive list
        inappropriate_words = ["profanity1", "profanity2", "slur1", "slur2"]
        for word in inappropriate_words:
            if word in user_input.lower():
                logger.warning(f"Inappropriate language detected: {word}")
                span.set_attribute("tripwire_triggered", True)
                span.set_attribute("reason", f"Inappropriate language detected: {word}")
                span.set_attribute("detected_word", word)
                
                return GuardrailFunctionOutput(
                    output_info="Your request contains inappropriate language. "
                            "Please rephrase your request using appropriate language.",
                    tripwire_triggered=True
                )
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )
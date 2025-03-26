"""
Output guardrails for validating agent responses before delivery.

This module contains functions and decorators for implementing output guardrails
that validate agent responses against business rules or compliance constraints.
"""

import logging
from typing import Any
from agents import output_guardrail, RunContextWrapper, Agent
from agents.guardrail import GuardrailFunctionOutput
from agents.tracing import get_current_trace

logger = logging.getLogger(__name__)

@output_guardrail()
async def validate_output_not_empty(context: RunContextWrapper, agent: Agent, agent_output: Any) -> GuardrailFunctionOutput:
    """
    Validate that the agent output is not empty.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        agent_output: The agent output to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    logger.info(f"Validating output is not empty: {str(agent_output)[:50]}...")
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_output_not_empty") as span:
        span.set_attribute("output_type", str(type(agent_output)))
        
        # Check if output is None, empty string, or empty container
        if agent_output is None or (isinstance(agent_output, (str, list, dict)) and not agent_output):
            logger.warning("Output is empty")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", "Output cannot be empty")
            
            return GuardrailFunctionOutput(
                output_info="Agent output cannot be empty.",
                tripwire_triggered=True
            )
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )

@output_guardrail()
async def validate_output_length(context: RunContextWrapper, agent: Agent, agent_output: Any) -> GuardrailFunctionOutput:
    """
    Validate that the agent output is not too long.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        agent_output: The agent output to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_output_length") as span:
        if not isinstance(agent_output, str):
            # If not a string, convert to string for length check
            output_str = str(agent_output)
        else:
            output_str = agent_output
        
        span.set_attribute("output_length", len(output_str))
        logger.info(f"Validating output length: {len(output_str)} characters")
        
        max_length = 5000  # Maximum allowed output length
        if len(output_str) > max_length:
            logger.warning(f"Output too long: {len(output_str)} characters")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", f"Output too long ({len(output_str)} characters)")
            span.set_attribute("max_length", max_length)
            
            return GuardrailFunctionOutput(
                output_info=f"Agent output is too long ({len(output_str)} characters). "
                        f"Please limit the output to {max_length} characters.",
                tripwire_triggered=True
            )
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )

@output_guardrail()
async def validate_no_error_in_output(context: RunContextWrapper, agent: Agent, agent_output: Any) -> GuardrailFunctionOutput:
    """
    Validate that the agent output does not contain error messages.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        agent_output: The agent output to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_no_error_in_output") as span:
        output_str = str(agent_output).lower()
        span.set_attribute("output_preview", output_str[:50])
        logger.info(f"Validating output for error messages: {output_str[:50]}...")
        
        error_indicators = ["error", "exception", "failed", "unable to", "cannot"]
        
        # If output is a dictionary, check if it has an 'error' key
        if isinstance(agent_output, dict) and "error" in agent_output:
            logger.warning(f"Error found in output dictionary: {agent_output.get('error')}")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", f"Error in output dictionary: {agent_output.get('error')}")
            span.set_attribute("error_key_present", True)
            
            return GuardrailFunctionOutput(
                output_info=f"Agent output contains an error: {agent_output.get('error')}",
                tripwire_triggered=True
            )
        
        # Check for error indicators in the output string
        for indicator in error_indicators:
            if indicator in output_str:
                logger.warning(f"Error indicator found in output: {indicator}")
                span.set_attribute("tripwire_triggered", True)
                span.set_attribute("reason", f"Error indicator in output: {indicator}")
                span.set_attribute("error_indicator", indicator)
                
                return GuardrailFunctionOutput(
                    output_info=f"Agent output contains an error indicator: '{indicator}'. "
                            "Please review the output for errors.",
                    tripwire_triggered=True
                )
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )

@output_guardrail()
async def validate_output_format(context: RunContextWrapper, agent: Agent, agent_output: Any) -> GuardrailFunctionOutput:
    """
    Validate that the agent output has the correct format.
    
    Args:
        context: The run context wrapper.
        agent: The agent instance.
        agent_output: The agent output to validate.
        
    Returns:
        GuardrailFunctionOutput: The result of the guardrail check.
    """
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_output_format") as span:
        span.set_attribute("output_type", str(type(agent_output)))
        logger.info(f"Validating output format: {type(agent_output)}")
        
        # Example: Ensure the output is a dictionary with specific keys
        if isinstance(agent_output, dict):
            required_keys = ["status"]
            missing_keys = [key for key in required_keys if key not in agent_output]
            
            span.set_attribute("is_dict", True)
            span.set_attribute("keys_present", list(agent_output.keys()))
            
            if missing_keys:
                logger.warning(f"Output missing required keys: {missing_keys}")
                span.set_attribute("tripwire_triggered", True)
                span.set_attribute("reason", f"Missing required keys: {missing_keys}")
                span.set_attribute("missing_keys", missing_keys)
                
                return GuardrailFunctionOutput(
                    output_info=f"Agent output is missing required keys: {missing_keys}. "
                            f"Please ensure the output includes all required keys: {required_keys}.",
                    tripwire_triggered=True
                )
        else:
            span.set_attribute("is_dict", False)
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )
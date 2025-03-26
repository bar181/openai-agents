"""
Handoff agent for delegating tasks between specialized agents.

This module contains classes and functions for implementing agent-to-agent handoffs
based on task complexity or specialized requirements.
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from agents import Agent, handoff, RunContextWrapper

logger = logging.getLogger(__name__)

# Define specialized agent class with _run method
class SpecializedAgent(Agent):
    """Specialized agent with run method implementation."""
    
    async def _run(self, message, **kwargs):
        """Run the agent with the given message."""
        # In a real implementation, this would call the LLM
        # For now, we'll return a simple response based on the agent's name
        return f"Response from {self.name}: I'll help with your inquiry about '{message}'."

# Create specialized agents
billing_agent = SpecializedAgent(
    name="Billing Agent",
    instructions="You are a billing specialist. You handle billing inquiries, payment issues, subscription questions, and invoice explanations. Provide clear, concise information about billing processes and resolve payment-related problems."
)

technical_support_agent = SpecializedAgent(
    name="Technical Support Agent",
    instructions="You are a technical support specialist. You handle technical issues, troubleshooting, error messages, and system problems. Provide step-by-step solutions and clear technical explanations to resolve user problems."
)

customer_service_agent = SpecializedAgent(
    name="Customer Service Agent",
    instructions="You are a customer service specialist. You handle general inquiries, account management, product information, and non-technical user assistance. Provide friendly, helpful responses to improve customer satisfaction."
)

# Define message filter functions
def filter_billing_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter messages to include only billing-related content.
    
    Args:
        messages: List of message dictionaries.
        
    Returns:
        Filtered list of messages.
    """
    # Extract only the most recent user message and any billing-related context
    filtered = []
    
    # Add system message for context
    filtered.append({
        "role": "system",
        "content": "You are handling a billing-related inquiry. Focus only on billing, payments, invoices, and subscriptions."
    })
    
    # Find the most recent user message
    for message in reversed(messages):
        if message.get("role") == "user":
            filtered.append(message)
            break
    
    return filtered

def filter_technical_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter messages to include only technical support-related content.
    
    Args:
        messages: List of message dictionaries.
        
    Returns:
        Filtered list of messages.
    """
    # Extract only the most recent user message and any technical-related context
    filtered = []
    
    # Add system message for context
    filtered.append({
        "role": "system",
        "content": "You are handling a technical support inquiry. Focus only on technical issues, troubleshooting, and system problems."
    })
    
    # Find the most recent user message
    for message in reversed(messages):
        if message.get("role") == "user":
            filtered.append(message)
            break
    
    return filtered

def filter_customer_service_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter messages to include only customer service-related content.
    
    Args:
        messages: List of message dictionaries.
        
    Returns:
        Filtered list of messages.
    """
    # Extract only the most recent user message and any customer service-related context
    filtered = []
    
    # Add system message for context
    filtered.append({
        "role": "system",
        "content": "You are handling a general customer service inquiry. Focus on providing helpful, friendly assistance."
    })
    
    # Find the most recent user message
    for message in reversed(messages):
        if message.get("role") == "user":
            filtered.append(message)
            break
    
    return filtered

# Create handoff instances with message filters
billing_handoff = handoff(
    agent=billing_agent,
    input_filter=filter_billing_messages
)

technical_handoff = handoff(
    agent=technical_support_agent,
    input_filter=filter_technical_messages
)

customer_service_handoff = handoff(
    agent=customer_service_agent,
    input_filter=filter_customer_service_messages
)

class HandoffAgent(Agent):
    """
    Agent for handling task delegation between specialized agents.
    
    This agent determines when to hand off tasks to other specialized agents
    based on the nature of the user's request.
    """
    
    def __init__(self, **kwargs):
        """Initialize the HandoffAgent with handoff capabilities."""
        # Set default name and instructions if not provided
        kwargs.setdefault("name", "Triage Agent")
        kwargs.setdefault("instructions", 
            """You are a triage agent responsible for determining the nature of user inquiries and routing them to the appropriate specialized agent.
            
            For billing inquiries (payments, invoices, subscriptions), route to the Billing Agent.
            For technical issues (errors, troubleshooting, system problems), route to the Technical Support Agent.
            For general inquiries (account management, product info), route to the Customer Service Agent.
            
            Analyze the user's message carefully to determine the most appropriate routing.
            """
        )
        
        # Set up handoffs if not provided
        kwargs.setdefault("handoffs", [
            billing_handoff,
            technical_handoff,
            customer_service_handoff
        ])
        
        super().__init__(**kwargs)
        
        # Store specialized agents for direct access
        self.specialized_agents = {
            "billing": billing_agent,
            "technical": technical_support_agent,
            "customer_service": customer_service_agent
        }
    
    async def determine_agent_type(self, message: str) -> str:
        """
        Determine which type of agent should handle the message.
        
        Args:
            message: The user's message.
            
        Returns:
            The type of agent to handle the message: "billing", "technical", or "customer_service".
        """
        # Simple keyword-based routing for demonstration
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["bill", "payment", "invoice", "charge", "subscription", "refund", "price"]):
            return "billing"
        elif any(word in message_lower for word in ["error", "bug", "crash", "not working", "broken", "fix", "problem", "technical"]):
            return "technical"
        else:
            return "customer_service"
    
    async def process_with_specialized_agent(self, message: str, agent_type: str) -> Dict[str, Any]:
        """
        Process a message with a specialized agent.
        
        Args:
            message: The user's message.
            agent_type: The type of agent to use.
            
        Returns:
            The agent's response.
        """
        try:
            agent = self.specialized_agents.get(agent_type)
            if not agent:
                return {
                    "status": "error",
                    "message": f"Unknown agent type: {agent_type}",
                    "agent_type": "unknown"
                }
            
            # Process with the specialized agent
            response = await agent.run(message)
            
            return {
                "status": "success",
                "message": response,
                "agent_type": agent_type
            }
        except Exception as e:
            logger.error(f"Error processing with specialized agent: {str(e)}")
            return {
                "status": "error",
                "message": f"Error processing with specialized agent: {str(e)}",
                "agent_type": agent_type
            }

def create_handoff_agent(**kwargs) -> HandoffAgent:
    """
    Create a handoff agent with the specified configuration.
    
    Args:
        **kwargs: Additional arguments to pass to the HandoffAgent constructor.
        
    Returns:
        A configured HandoffAgent instance.
    """
    return HandoffAgent(**kwargs)
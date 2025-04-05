import pytest
from app.agents.advanced.multi_tool_agent import multi_tool_agent

def test_multi_tool_agent_success():
    """
    Test that the multi-tool agent processes the input correctly.
    Expected input format: "num1,num2;text_for_uppercase;message_for_echo"
    For example: "2,3;hello;world" should return:
      - math_result: 5
      - uppercase_result: "HELLO"
      - echo_result: "Echo: world"
    """
    sample_input = "2,3;hello;world"
    result = multi_tool_agent.run(sample_input)
    assert "math_result" in result
    assert "uppercase_result" in result
    assert "echo_result" in result
    assert result["math_result"] == 5
    assert result["uppercase_result"] == "HELLO"
    assert result["echo_result"] == "Echo: world"

def test_multi_tool_agent_invalid_input():
    """
    Test that the multi-tool agent returns an error for invalid input.
    For example, input with fewer than two parts should trigger an error.
    """
    sample_input = "2,3;hello"  # Only two parts provided; expect error due to missing echo part (if required)
    result = multi_tool_agent.run(sample_input)
    assert "error" in result

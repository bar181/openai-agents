Agents
Agents are the core building block in your apps. An agent is a large language model (LLM), configured with instructions and tools.

Basic configuration
The most common properties of an agent you'll configure are:

instructions: also known as a developer message or system prompt.
model: which LLM to use, and optional model_settings to configure model tuning parameters like temperature, top_p, etc.
tools: Tools that the agent can use to achieve its tasks.

from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
Context
Agents are generic on their context type. Context is a dependency-injection tool: it's an object you create and pass to Runner.run(), that is passed to every agent, tool, handoff etc, and it serves as a grab bag of dependencies and state for the agent run. You can provide any Python object as the context.


@dataclass
class UserContext:
  uid: str
  is_pro_user: bool

  async def fetch_purchases() -> list[Purchase]:
     return ...

agent = Agent[UserContext](
    ...,
)
Output types
By default, agents produce plain text (i.e. str) outputs. If you want the agent to produce a particular type of output, you can use the output_type parameter. A common choice is to use Pydantic objects, but we support any type that can be wrapped in a Pydantic TypeAdapter - dataclasses, lists, TypedDict, etc.


from pydantic import BaseModel
from agents import Agent


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
Note

When you pass an output_type, that tells the model to use structured outputs instead of regular plain text responses.

Handoffs
Handoffs are sub-agents that the agent can delegate to. You provide a list of handoffs, and the agent can choose to delegate to them if relevant. This is a powerful pattern that allows orchestrating modular, specialized agents that excel at a single task. Read more in the handoffs documentation.


from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about booking, handoff to the booking agent."
        "If they ask about refunds, handoff to the refund agent."
    ),
    handoffs=[booking_agent, refund_agent],
)
Dynamic instructions
In most cases, you can provide instructions when you create the agent. However, you can also provide dynamic instructions via a function. The function will receive the agent and context, and must return the prompt. Both regular and async functions are accepted.


def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."


agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
)
Lifecycle events (hooks)
Sometimes, you want to observe the lifecycle of an agent. For example, you may want to log events, or pre-fetch data when certain events occur. You can hook into the agent lifecycle with the hooks property. Subclass the AgentHooks class, and override the methods you're interested in.

Guardrails
Guardrails allow you to run checks/validations on user input, in parallel to the agent running. For example, you could screen the user's input for relevance. Read more in the guardrails documentation.

Cloning/copying agents
By using the clone() method on an agent, you can duplicate an Agent, and optionally change any properties you like.


pirate_agent = Agent(
    name="Pirate",
    instructions="Write like a pirate",
    model="o3-mini",
)

robot_agent = pirate_agent.clone(
    name="Robot",
    instructions="Write like a robot",
)
Forcing tool use
Supplying a list of tools doesn't always mean the LLM will use a tool. You can force tool use by setting ModelSettings.tool_choice. Valid values are:

auto, which allows the LLM to decide whether or not to use a tool.
required, which requires the LLM to use a tool (but it can intelligently decide which tool).
none, which requires the LLM to not use a tool.
Setting a specific string e.g. my_tool, which requires the LLM to use that specific tool.

///

Let's put it all together and run the entire workflow, using handoffs and the input guardrail.


from agents import Agent, InputGuardrail,GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
View your traces
To review what happened during your agent run, navigate to the Trace viewer in the OpenAI Dashboard to view traces of your agent runs.

///

You can run agents via the Runner class. You have 3 options:

Runner.run(), which runs async and returns a RunResult.
Runner.run_sync(), which is a sync method and just runs .run() under the hood.
Runner.run_streamed(), which runs async and returns a RunResultStreaming. It calls the LLM in streaming mode, and streams those events to you as they are received.

from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
Read more in the results guide.

The agent loop
When you use the run method in Runner, you pass in a starting agent and input. The input can either be a string (which is considered a user message), or a list of input items, which are the items in the OpenAI Responses API.

The runner then runs a loop:

We call the LLM for the current agent, with the current input.
The LLM produces its output.
If the LLM returns a final_output, the loop ends and we return the result.
If the LLM does a handoff, we update the current agent and input, and re-run the loop.
If the LLM produces tool calls, we run those tool calls, append the results, and re-run the loop.
If we exceed the max_turns passed, we raise a MaxTurnsExceeded exception.
Note

The rule for whether the LLM output is considered as a "final output" is that it produces text output with the desired type, and there are no tool calls.

Streaming
Streaming allows you to additionally receive streaming events as the LLM runs. Once the stream is done, the RunResultStreaming will contain the complete information about the run, including all the new outputs produces. You can call .stream_events() for the streaming events. Read more in the streaming guide.

Run config
The run_config parameter lets you configure some global settings for the agent run:

model: Allows setting a global LLM model to use, irrespective of what model each Agent has.
model_provider: A model provider for looking up model names, which defaults to OpenAI.
model_settings: Overrides agent-specific settings. For example, you can set a global temperature or top_p.
input_guardrails, output_guardrails: A list of input or output guardrails to include on all runs.
handoff_input_filter: A global input filter to apply to all handoffs, if the handoff doesn't already have one. The input filter allows you to edit the inputs that are sent to the new agent. See the documentation in Handoff.input_filter for more details.
tracing_disabled: Allows you to disable tracing for the entire run.
trace_include_sensitive_data: Configures whether traces will include potentially sensitive data, such as LLM and tool call inputs/outputs.
workflow_name, trace_id, group_id: Sets the tracing workflow name, trace ID and trace group ID for the run. We recommend at least setting workflow_name. The session ID is an optional field that lets you link traces across multiple runs.
trace_metadata: Metadata to include on all traces.
Conversations/chat threads
Calling any of the run methods can result in one or more agents running (and hence one or more LLM calls), but it represents a single logical turn in a chat conversation. For example:

User turn: user enter text
Runner run: first agent calls LLM, runs tools, does a handoff to a second agent, second agent runs more tools, and then produces an output.
At the end of the agent run, you can choose what to show to the user. For example, you might show the user every new item generated by the agents, or just the final output. Either way, the user might then ask a followup question, in which case you can call the run method again.

You can use the base RunResultBase.to_input_list() method to get the inputs for the next turn.


async def main():
    agent = Agent(name="Assistant", instructions="Reply very concisely.")

    with trace(workflow_name="Conversation", group_id=thread_id):
        # First turn
        result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
        print(result.final_output)
        # San Francisco

        # Second turn
        new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
        result = await Runner.run(agent, new_input)
        print(result.final_output)
        # California

//

API keys and clients
By default, the SDK looks for the OPENAI_API_KEY environment variable for LLM requests and tracing, as soon as it is imported. If you are unable to set that environment variable before your app starts, you can use the set_default_openai_key() function to set the key.


from agents import set_default_openai_key

set_default_openai_key("sk-...")
Alternatively, you can also configure an OpenAI client to be used. By default, the SDK creates an AsyncOpenAI instance, using the API key from the environment variable or the default key set above. You can change this by using the set_default_openai_client() function.


from openai import AsyncOpenAI
from agents import set_default_openai_client

custom_client = AsyncOpenAI(base_url="...", api_key="...")
set_default_openai_client(custom_client)
Finally, you can also customize the OpenAI API that is used. By default, we use the OpenAI Responses API. You can override this to use the Chat Completions API by using the set_default_openai_api() function.


from agents import set_default_openai_api

set_default_openai_api("chat_completions")
Tracing
Tracing is enabled by default. It uses the OpenAI API keys from the section above by default (i.e. the environment variable or the default key you set). You can specifically set the API key used for tracing by using the set_tracing_export_api_key function.


from agents import set_tracing_export_api_key

set_tracing_export_api_key("sk-...")
You can also disable tracing entirely by using the set_tracing_disabled() function.


from agents import set_tracing_disabled

set_tracing_disabled(True)
Debug logging
The SDK has two Python loggers without any handlers set. By default, this means that warnings and errors are sent to stdout, but other logs are suppressed.

To enable verbose logging, use the enable_verbose_stdout_logging() function.


from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
Alternatively, you can customize the logs by adding handlers, filters, formatters, etc. You can read more in the Python logging guide.


import logging

logger =  logging.getLogger("openai.agents") # or openai.agents.tracing for the Tracing logger

# To make all logs show up
logger.setLevel(logging.DEBUG)
# To make info and above show up
logger.setLevel(logging.INFO)
# To make warning and above show up
logger.setLevel(logging.WARNING)
# etc

# You can customize this as needed, but this will output to `stderr` by default
logger.addHandler(logging.StreamHandler())
Sensitive data in logs
Certain logs may contain sensitive data (for example, user data). If you want to disable this data from being logged, set the following environment variables.

To disable logging LLM inputs and outputs:


export OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1
To disable logging tool inputs and outputs:


export OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1

//

Model settings
ModelSettings dataclass
Settings to use when calling an LLM.

This class holds optional model configuration parameters (e.g. temperature, top_p, penalties, truncation, etc.).

Not all models/providers support all of these parameters, so please check the API documentation for the specific model and provider you are using.

Source code in src/agents/model_settings.py
temperature class-attribute instance-attribute

temperature: float | None = None
The temperature to use when calling the model.

top_p class-attribute instance-attribute

top_p: float | None = None
The top_p to use when calling the model.

frequency_penalty class-attribute instance-attribute

frequency_penalty: float | None = None
The frequency penalty to use when calling the model.

presence_penalty class-attribute instance-attribute

presence_penalty: float | None = None
The presence penalty to use when calling the model.

tool_choice class-attribute instance-attribute

tool_choice: (
    Literal["auto", "required", "none"] | str | None
) = None
The tool choice to use when calling the model.

parallel_tool_calls class-attribute instance-attribute

parallel_tool_calls: bool | None = False
Whether to use parallel tool calls when calling the model.

truncation class-attribute instance-attribute

truncation: Literal['auto', 'disabled'] | None = None
The truncation strategy to use when calling the model.

max_tokens class-attribute instance-attribute

max_tokens: int | None = None
The maximum number of output tokens to generate.

resolve

resolve(override: ModelSettings | None) -> ModelSettings
Produce a new ModelSettings by overlaying any non-None values from the override on top of this instance.

Source code in src/agents/model_settings.py


Models
The Agents SDK comes with out-of-the-box support for OpenAI models in two flavors:

Recommended: the OpenAIResponsesModel, which calls OpenAI APIs using the new Responses API.
The OpenAIChatCompletionsModel, which calls OpenAI APIs using the Chat Completions API.
Mixing and matching models
Within a single workflow, you may want to use different models for each agent. For example, you could use a smaller, faster model for triage, while using a larger, more capable model for complex tasks. When configuring an Agent, you can select a specific model by either:

Passing the name of an OpenAI model.
Passing any model name + a ModelProvider that can map that name to a Model instance.
Directly providing a Model implementation.
Note

While our SDK supports both the OpenAIResponsesModel and the OpenAIChatCompletionsModel shapes, we recommend using a single model shape for each workflow because the two shapes support a different set of features and tools. If your workflow requires mixing and matching model shapes, make sure that all the features you're using are available on both.


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model="o3-mini", 
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel( 
        model="gpt-4o",
        openai_client=AsyncOpenAI()
    ),
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo",
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
Using other LLM providers
You can use other LLM providers in 3 ways (examples here):

set_default_openai_client is useful in cases where you want to globally use an instance of AsyncOpenAI as the LLM client. This is for cases where the LLM provider has an OpenAI compatible API endpoint, and you can set the base_url and api_key. See a configurable example in examples/model_providers/custom_example_global.py.
ModelProvider is at the Runner.run level. This lets you say "use a custom model provider for all agents in this run". See a configurable example in examples/model_providers/custom_example_provider.py.
Agent.model lets you specify the model on a specific Agent instance. This enables you to mix and match different providers for different agents. See a configurable example in examples/model_providers/custom_example_agent.py.
In cases where you do not have an API key from platform.openai.com, we recommend disabling tracing via set_tracing_disabled(), or setting up a different tracing processor.

Note

In these examples, we use the Chat Completions API/model, because most LLM providers don't yet support the Responses API. If your LLM provider does support it, we recommend using Responses.

Common issues with using other LLM providers
Tracing client error 401
If you get errors related to tracing, this is because traces are uploaded to OpenAI servers, and you don't have an OpenAI API key. You have three options to resolve this:

Disable tracing entirely: set_tracing_disabled(True).
Set an OpenAI key for tracing: set_tracing_export_api_key(...). This API key will only be used for uploading traces, and must be from platform.openai.com.
Use a non-OpenAI trace processor. See the tracing docs.
Responses API support
The SDK uses the Responses API by default, but most other LLM providers don't yet support it. You may see 404s or similar issues as a result. To resolve, you have two options:

Call set_default_openai_api("chat_completions"). This works if you are setting OPENAI_API_KEY and OPENAI_BASE_URL via environment vars.
Use OpenAIChatCompletionsModel. There are examples here.
Structured outputs support
Some model providers don't have support for structured outputs. This sometimes results in an error that looks something like this:


BadRequestError: Error code: 400 - {'error': {'message': "'response_format.type' : value is not one of the allowed values ['text','json_object']", 'type': 'invalid_request_error'}}
This is a shortcoming of some model providers - they support JSON outputs, but don't allow you to specify the json_schema to use for the output. We are working on a fix for this, but we suggest relying on providers that do have support for JSON schema output, because otherwise your app will often break because of malformed JSON.
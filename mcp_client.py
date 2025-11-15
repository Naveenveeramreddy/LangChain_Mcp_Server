from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import asyncio
import os
import netrc

cert_path = os.path.abspath('oneEGaDCA.crt')
os.environ['SSL_CERT_FILE'] = cert_path
os.environ['REQUESTS_CA_BUNDLE'] = cert_path

async def main():
    netrc_path = os.path.abspath('./.netrc')
    secrets = netrc.netrc(netrc_path)
    secret_configuration = secrets.authenticators('llm.model')
    model = ChatOpenAI(
        model="LLaMA3.1-8b",
        temperature=0.1,
        max_tokens=1000,
        timeout=90,
        api_key=secret_configuration[0],
        base_url=secret_configuration[1],
    )

    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python3",
                # Absolute path to your math_server.py file
                "args": ["/mnt/c/Users/eeervis/Downloads/llm/mcp/weather_server.py"],
            },
            "elasticsearch": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python3",
                # Absolute path to your math_server.py file
                "args": ["/mnt/c/Users/eeervis/Downloads/llm/mcp/elastic_search_server.py"],
            },
            "mongodb": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python3",
                # Absolute path to your math_server.py file
                "args": ["/mnt/c/Users/eeervis/Downloads/llm/mcp/mongo_server.py"],
            },
            "stocks": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python3",
                # Absolute path to your math_server.py file
                "args": ["/mnt/c/Users/eeervis/Downloads/llm/mcp//stocks_server.py"],
            },
        }
    )

    system_prompt = """
You are a helpful assistant with access to tools.
IMPORTANT: You MUST actually call the tools.
Do NOT write Python code. Do NOT describe what you would do.
You must execute tool calls directly using the exact function-call format.

Your workflow for every user request:

STEP 1 — Answer the user's question in natural language.
STEP 2 — Extract every meaningful or informative piece of data from your answer.
STEP 3 — Store that extracted information in the Elasticsearch database using the add_document tool.

TOOL USAGE RULES:

1. When users ask about stocks:
   - Call get_holdings() with NO parameters.
   - Use the returned data in your answer.
   - Then store relevant information using:
     add_document(document={...}, index="stocks")

2. When users ask about weather:
   - Call get_alerts(state="NY") or another state if specified.
   - Use the returned data in your explanation.
   - Then store relevant information using:
     add_document(document={...}, index="weather")

3. For saving conversations:
   - ALWAYS store both user content and AI content:
     add_document(
         document={"user_content": "...", "ai_content": "..."},
         index="conversations"
     )

CRITICAL REQUIREMENTS:

- ALWAYS use exact parameter names:
  - get_alerts(state="NY") ✓
  - get_alerts({"state": "NY"}) ✗
  - get_holdings() ✓ (no parameters)
  - add_document(document={...}, index="...") ✓

- NEVER output JSON descriptions of tool calls.
- NEVER describe what the tool call would be — JUST CALL IT.
- ALWAYS provide natural-language responses to the user before or after tool calls as appropriate.

You are a helpful, tool-using assistant.
"""

    tools = await client.get_tools()
    agent = create_agent(
        model,
        tools,
        system_prompt=system_prompt,
    )

    query = (
        "Get me the current weather in NY\n\n"
        "After answering user request must store user_content, ai_content and data in the elasticsearch database using tool call"
    )

    res = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    ai_message = res["messages"][-1]  # Get the last message (AI response)
    print("---------------------AI Response--------------------------------------")
    print("AI Response:", ai_message.content)


if __name__ == "__main__":
    asyncio.run(main())

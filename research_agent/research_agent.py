from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os
from langchain.agents import create_tool_calling_agent, AgentExecutor
from Research_tools import search_tool, save_tool


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(
    openai_api_key="Your Open AI Api key here",
                             base_url ="https://models.github.ai/inference",
                             model_name="openai/gpt-4o",
                             temperature=0.1
)

parser = PydanticOutputParser(pydantic_object = ResearchResponse)

System_prompt = ChatPromptTemplate.from_messages(
    [
        (

    "system",
    """
You are a research assistant that will help generate a research paper.
Answer the user query and use necessary tools.
"You must use the 'save_txt' tool to save the final structured output once it's complete.\n
wrap the output in this format and provide no other text\n{format_instructions}
""",
),

("placeholder", "{chat_history}"),
("human","{query}"),
("placeholder", "{agent_scratchpad}"),

]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, save_tool]
agent = create_tool_calling_agent(
    llm = llm,
    prompt=System_prompt,
    tools=tools

)

agent_executor = AgentExecutor(agent = agent, tools = tools, verbose=True)
query = input("What can I help you with? ")
query1 = "What can I help you with? "
#text_to_speech(query1, rate=170, voice_index=0)
raw_response= agent_executor.invoke({"query": query})
#print(raw_response)
#response = parser.parse(raw_response.get("output"))
response = raw_response.get("output")
#text_to_speech(response, rate=170, voice_index=0)
print(response)
#print(response.summary)
#print(response.sources)
#print(response.tools_used)

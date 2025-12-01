"This is comprehensive format for writing custom tools for AI agent using Langchain"

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import time
from pprint import pformat

"Web-Scraping tool"
wiki_wrapper = WikipediaAPIWrapper()
search_tool = Tool(
    name= "research_tool",
    func= WikipediaQueryRun(api_wrapper=wiki_wrapper).run,
    description= "Search the web for information",
)

def save_file(data: str, filename: str = "research output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = pformat(f"Timestamp: {timestamp}\n\n{data}\n\n{'='*40}\n\n")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    #return f"Data Successfully Saved to {filename}"
"File Saving too"
save_tool = Tool(
    name = "save_txt",
    func = save_file,
    description = "saves structure research data"
)

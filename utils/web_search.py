from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()

"""
references
https://python.langchain.com/docs/integrations/tools/tavily_search/
https://python.langchain.com/docs/integrations/tools/google_serper/
"""

class WebSearch:
    def __init__(self):
        self.search_api = None

    def run(self, query):
        pass
    
class Tavily(WebSearch):
    def __init__(self):
        self.search_api = TavilySearchResults(
            max_results=3,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
        )
    def run(self, query):
        return self.search_api.invoke({"query": query})
        
class Serper(WebSearch):
    def __init__(self):
        self.search_api = GoogleSerperAPIWrapper(
            type="news",
            gl='kr',
            hl='ko',
            k=10
        )
    def run(self, query):
        return self.search_api.results(query)

web_search_tools = {
    "tavily": Tavily(),
    "serper": Serper(),
}
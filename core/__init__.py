from .utils import fetch_naver_news, fetch_google_trends
from .rag import RAGAgent
from .prompt import streamlit_template, chrome_extension_template

st_agent = RAGAgent(prompt_template=streamlit_template)
ce_agent = RAGAgent(prompt_template=chrome_extension_template)

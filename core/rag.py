from .db import word_collection, book_collection

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self, prompt_template):
        retriever = word_collection.as_retriever(search_kwargs={"k": 3})
        # retriever = book_collection.as_retriever(search_kwargs={"k": 2})

        prompt = PromptTemplate(input_variables=["context", "term"], template=prompt_template)

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        self.chain = (
            {
                "context": retriever | self.format_retriever_output,
                "term": RunnablePassthrough(),
            }
            | prompt
            | llm 
            | StrOutputParser()
        )
    def format_retriever_output(self, docs):
        return "\n".join([doc.page_content for doc in docs])
        
    def invoke(self, user_input):
        return self.chain.invoke(user_input)
    
    def stream(self, user_input):
        return self.chain.stream(user_input)

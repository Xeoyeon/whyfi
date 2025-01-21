from db import CustomChroma
from .prompt import prompt_templates
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# 툴(load_tools)이나 메모리 사용(AgentExecutor)해야 하면 langchain.agents도 고려해보기

class BasicAgent:
    def __init__(self):
        self.prompt = PromptTemplate.from_template(prompt_templates['basic_template'])
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

        self.rag_chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, question):
        return self.rag_chain.invoke(question)   
    async def a_invoke(self, question):
        return await self.rag_chain.ainvoke(question)
    
    def stream(self, question):
        return self.rag_chain.stream(question)
    async def a_stream(self, question):
        return await self.rag_chain.astream(question)
    
class RAGAgent(BasicAgent):
    def __init__(self):
        super().__init__()
        chroma = CustomChroma()
        vectorstore = chroma.vector_store
        self.retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        self.prompt = PromptTemplate.from_template(prompt_templates['context_template'])

        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def format_docs(self, docs):
        return "\n\n### ".join(doc.page_content for doc in docs).replace("-----", "")
    
agents = {
    "basic": BasicAgent(),
    "RAG": RAGAgent()
}
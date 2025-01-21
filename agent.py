from db.chromadb import CustomChroma
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self, prompt_template):
        chroma = CustomChroma()
        vectorstore = chroma.vector_store
        self.retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def invoke(self, question):
        return self.rag_chain.invoke(question)
    
    def stream(self, question):
        return self.rag_chain.stream(question)


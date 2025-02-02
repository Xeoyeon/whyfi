from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

os.chdir('C:\\Users\\seoyounglee\\workspace\\Euron\\Whyfi')

def load_split(docs):  # docs를 인자로 받는 형태로 수정
    # 텍스트 분할기 설정
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
    )
    split_docs = text_splitter.split_documents(docs)
    return split_docs

def emb(split_docs):
    # 임베딩 모델 설정
    embedding_model = HuggingFaceEmbeddings(
                model_name="dragonkue/BGE-m3-ko",
                multi_process=False,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},  
            )

    # Chroma 벡터 저장소 생성
    vector_store = Chroma(
        persist_directory="chroma_db", embedding_function=embedding_model
    )        
    # 문서 추가
    vector_store.add_documents(split_docs)
    return vector_store

# PDF 파일 로딩
pdf_loader = PyPDFLoader("./pre/2024 한권으로 OK 주식과 세금.pdf")
pdf_docs = pdf_loader.load()  # load()로 PDF 문서 로딩
pdf_split_docs = load_split(pdf_docs)  # 로드된 문서를 분할

# CSV 파일 로딩
csv_loader = CSVLoader("./pre/cleaned_word_dict.csv", encoding='utf-8') 
csv_docs = csv_loader.load()  # CSV 문서 로딩
csv_split_docs = load_split(csv_docs)  # CSV 문서를 분할

# PDF 문서와 CSV 문서를 모두 결합하여 벡터 저장소에 추가
all_split_docs = pdf_split_docs + csv_split_docs
vector_store = emb(all_split_docs)

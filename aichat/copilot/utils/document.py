from  langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def process_pdf_and_get_retriever(file_path:str):
    docs = PyPDFLoader(file_path=file_path).load()    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    splits = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(
    openai_api_base="https://api.siliconflow.cn/v1",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3"
    )
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})



    


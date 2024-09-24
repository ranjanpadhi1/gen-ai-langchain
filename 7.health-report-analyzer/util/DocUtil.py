import os
from pathlib import PureWindowsPath, PurePosixPath
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def doc_to_chunks(path: str):
    if not is_file_exists(path):
        return
    if path.lower().endswith('.pdf'):
        return load_pdf(path)
    else:
        print('Unsupported file format!')

def load_pdf(path):
    try:
        loader = PyPDFLoader(path)
        documents = loader.load()
        sp = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return sp.split_documents(documents)
    except:
        print(f'File "{path}" not found!')

def is_file_exists(path): 
    print("Current Working Directory:", os.getcwd())
    print("File Exists:", os.path.exists(path))
    return os.path.exists(path)
import os
from pathlib import PureWindowsPath, PurePosixPath
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def doc_to_chunks(path: str):
    if not files_exist(path):
        return
    
    chunks = load_pdf(path)
    if not chunks:
        print('Error while processing the reports !')
        
    return chunks

def load_pdf(path):
    try:
        loader = PyPDFDirectoryLoader(path)
        documents = loader.load()
        sp = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return sp.split_documents(documents)
    except:
        print('Invalid file format !')

def files_exist(path): 
    print("Reading files from: ", os.getcwd() + path[1::].replace('/', '\\'))
    files = os.listdir(path)
    
    if not files or len(files) == 0:
        print("No reports found !")
        return False
    
    # for file in files:
    #     print(file)

    return True
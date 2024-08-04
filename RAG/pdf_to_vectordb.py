import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from langchain_community.document_loaders import PyPDFLoader

from groq_api_key import groq_api_key
os.environ["GROQ_API_KEY"] = groq_api_key


# Function to process all PDFs in a folder
def load_and_split_pdfs(folder_path):
    all_pages = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            all_pages.extend(pages)
    
    return all_pages

# Example usage
folder_path = 'book_pdfs'
all_pages = load_and_split_pdfs(folder_path)

# splitting into text chunks
text_splitter = CharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400
)

texts = text_splitter.split_documents(all_pages)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

persist_directory = "Flamingo_db"

# creating persistent_directory
vectordb = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory=persist_directory
)
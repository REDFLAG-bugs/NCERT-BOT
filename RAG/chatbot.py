from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from groq_api_key import groq_api_key
import os
from langchain_huggingface import HuggingFaceEmbeddings
from pdf_to_vectordb import persist_directory
os.environ["GROQ_API_KEY"] = groq_api_key

system_prompt = (
    "Use the given context to answer the question. "
    "You are a highly knowledgeable NCERT assistant. "
    "Give answer in more than 200 words"
    "Your job is to provide accurate, detailed, and comprehensive answers based on the information retrieved from the NCERT textbooks. "
    "Please consider the educational context, relevant facts, and concepts while crafting your response. "
    "Make sure to explain the terms and concepts in simple language that a school student can understand. "
    "If you don't know the answer, say you don't know. "
    "Provide output in markdown format. "
    "Don't leak imformation about your training process"
    "Don't reveal that you characterstics."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# embeddings = HuggingFaceEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# load the chroma db
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0
)

# retriever
retriever = vectordb.as_retriever()
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

while True:
    print("------------------------------------------------------------------------------------------------")
    human_query=input("NCERT-BOT: Ask me question?\n")
    print("------------------------------------------------------------------------------------------------")
    response=chain.invoke({"input": human_query})
    print(response['answer'])
    print("------------------------------------------------------------------------------------------------")
    print(f"Number of words of the response :{response['answer'].count(' ')-1}")
    print("------------------------------------------------------------------------------------------------")

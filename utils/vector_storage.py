# === Bibliotecas ===
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def load():

    load_dotenv(find_dotenv())
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FAISS_INDEX_PATH = "db"
    
    try:
        asyncio.get_running_loop()

    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)

    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
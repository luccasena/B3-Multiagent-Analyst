from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

load_dotenv(find_dotenv())

FAISS_INDEX_PATH = "db"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)

try:
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    print("Banco vetorial FAISS carregado com sucesso!")

except Exception as e:
    print(f"Erro ao carregar o banco de dados FAISS: {e}")
    exit()

question = "Qual desses ativos possue o maior P/L?"

retriever = vector_store.as_retriever()

docs_scores = vector_store.similarity_search_with_score(question, k=4)
for doc, score in docs_scores:
    print(f"\n📄 Score: {score:.4f}")
    print(doc.page_content[:300])
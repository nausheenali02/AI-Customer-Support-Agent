from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import GOOGLE_API_KEY


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"


def get_relevant_faqs(question: str) -> str:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vector_store = Chroma(
        collection_name="customer_support_faq",
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
    )

    results = vector_store.similarity_search(question, k=2)

    if not results:
        return "No relevant FAQ information found."

    return "\n\n".join(document.page_content for document in results)

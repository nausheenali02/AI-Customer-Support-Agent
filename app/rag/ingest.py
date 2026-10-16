from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import GOOGLE_API_KEY


BASE_DIR = Path(__file__).resolve().parents[2]
FAQ_PATH = BASE_DIR / "data" / "faq.txt"
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"


def build_faq_database():
    if not FAQ_PATH.exists():
        raise FileNotFoundError(f"FAQ file not found: {FAQ_PATH}")

    text = FAQ_PATH.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH),
        collection_name="customer_support_faq",
    )

    print(f"FAQ database created with {len(chunks)} text chunks.")


if __name__ == "__main__":
    build_faq_database()

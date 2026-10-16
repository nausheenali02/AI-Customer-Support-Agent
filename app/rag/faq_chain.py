from app.llm import llm
from app.rag.retriever import get_relevant_faqs


def answer_faq(question: str) -> str:
    context = get_relevant_faqs(question)

    prompt = f"""
You are a helpful customer support assistant.

Answer the customer's question using only the FAQ context below.
If the context does not contain enough information, say that you
don't have enough information and suggest contacting human support.
Do not invent store policies.

FAQ Context:
{context}

Customer Question:
{question}

Answer:
"""

    result = llm.invoke(prompt)
    content = result.content

    if isinstance(content, list):
        content = " ".join(
            item["text"] if isinstance(item, dict) and "text" in item
            else str(item)
            for item in content
        )

    return content.strip()

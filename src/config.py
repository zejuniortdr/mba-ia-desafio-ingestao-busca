import os

from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

POSTGRES_USER = os.getenv("POSTGRES_USER", "raguser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ragpassword")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ragdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_documents")

CONNECTION_STRING = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

PDF_PATH = "pdfs/document-short.pdf"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def get_embeddings():
    if LLM_PROVIDER == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY,
    )


def get_llm():
    if LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=GOOGLE_API_KEY,
            temperature=0,
        )
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=OPENAI_API_KEY,
        temperature=0,
    )


def get_vector_store(embeddings):
    from langchain_postgres import PGVector

    return PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

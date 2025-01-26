import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client

import wrapper.supabase as sb

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

st.header("RAG管理")


supabase = create_client(os.getenv("EXPO_PUBLIC_SUPABASE_URL"), os.getenv("EXPO_PUBLIC_R2_BASE_URL"))

embeddings = OpenAIEmbeddings()

from langchain_community.document_loaders import UnstructuredURLLoader

urls = [ "https://supabase.com/blog/openai-embeddings-postgres-vector" ]

loader = UnstructuredURLLoader(urls=urls)
docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
splits = text_splitter.split_documents(docs)

vectorstore = SupabaseVectorStore.from_documents(
    splits,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)
     

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
retrieved_docs = retriever.invoke("How to store embeddings with pgvector?")

print(retrieved_docs)
     

# loader = TextLoader("../../how_to/state_of_the_union.txt")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# vector_store = SupabaseVectorStore.from_documents(
#     docs,
#     embeddings,
#     client=supabase,
#     table_name="documents",
#     query_name="match_documents",
#     chunk_size=500,
# )

# query = "What did the president say about Ketanji Brown Jackson"
# matched_docs = vector_store.similarity_search(query)


# print(matched_docs[0].page_content)


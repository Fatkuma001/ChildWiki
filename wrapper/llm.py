import logging
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from .prompt import SYSTEM_PROMPT_CLASSIFY, USER_PROMPT_CLASSIFY, SYSTEM_PROMPT_ANSWER, USER_PROMPT_ANSWER


def need_web_search(question: str) -> bool:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_CLASSIFY),
            ("user", USER_PROMPT_CLASSIFY),
        ]
    )

    model = get_llm_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.invoke({"question": question}) == "yes"


def llm_answer(question: str, chat_history: str,
               search_result: str = "",
               username: str = "Unknown") -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_ANSWER),
            ("user", USER_PROMPT_ANSWER),
        ]
    )

    model = get_llm_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.stream(
        {
            "question": question,
            "chat_history": chat_history,
            "search_result": search_result,
            "username": username,
        }
    )


def get_llm_model():
    groq_llm = get_groq_model()
    deepseek_llm = get_deepseek_model()

    return groq_llm.with_fallbacks([deepseek_llm])


def get_groq_model() -> ChatGroq:
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0.3, 
        max_tokens=1024,
        api_key=os.getenv("GROQ_KEY")
    )


def get_deepseek_model() -> ChatOpenAI:
    return ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com",
        temperature=0.3,
        max_tokens=1024,
        api_key=os.getenv("DEEPSEEK_KEY")
    )


# def get_openai_model() -> ChatOpenAI:
#     return ChatOpenAI(model="gpt-4o", temperature=0.3, max_tokens=512)

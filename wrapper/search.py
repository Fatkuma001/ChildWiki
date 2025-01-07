import logging
import pprint

import sentry_sdk
from duckduckgo_search import DDGS
from googlesearch import search


def search_web(query_text: str) -> str:
    try:
        return search_by_duckduckgo(query_text)
    except Exception:
        return search_by_google(query_text)


def search_by_duckduckgo(query_text: str) -> str:
    try:
        results = DDGS(timeout=5).text(query_text, max_results=5)
        return "\n\n".join(
            [
                f"{result['title']}\n{result['body']}\n{result['href']}"
                for result in results
            ]
        )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logging.exception(e)
        raise e


def search_by_google(query_text: str) -> str:
    try:
        results = search(query_text, num_results=5, advanced=True)
        return "\n\n".join(
            [
                f"{result.title}\n{result.description}\n{result.url}"
                for result in results
            ]
        )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logging.exception(e)
        return ""

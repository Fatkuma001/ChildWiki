import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import sentry_sdk
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv("EXPO_PUBLIC_SUPABASE_URL"), os.getenv("EXPO_PUBLIC_R2_BASE_URL"))


def add_chat_data(session_id: str, question: str, answer: str, uid: int = 0):
    # Insert the data into the 'chat_history' table
    data = {
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "uid": uid,
        "created_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
    }

    # Use Supabase's insert method
    try:
        supabase.table("chat_history").insert(data).execute()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logging.exception(e)


# @st.cache_data(ttl=60 * 60 * 24)
# def find_stories(book_title: list[str] = []):
#     try:
#         # Use Supabase's select method
#         response = supabase.table("stories").select(
#             "*").in_("book_title", book_title).order("book_title").order("title").execute()
#         return response.data
#     except Exception as e:
#         sentry_sdk.capture_exception(e)
#         logging.exception(e)
#         return []


# @st.cache_data(ttl=60 * 60 * 24)
# def find_books():
#     try:
#         response = supabase.table("view_books").select("*").execute()
#         return response.data
#     except Exception as e:
#         sentry_sdk.capture_exception(e)
#         logging.exception(e)
#         return []


# @st.cache_data(ttl=60 * 60 * 24)
# def find_students():
#     try:
#         # Use Supabase's select method
#         response = supabase.table("students").select(
#             "*").order("id").execute()
#         return response.data
#     except Exception as e:
#         sentry_sdk.capture_exception(e)
#         logging.exception(e)
#         return []


# def get_student_by_id(id: int = 0):
#     for student in find_students():
#         if student['id'] == id:
#             return student
#     return None


# def update_story_for_audio(id: str, mp3_url: str, mp3_duration: float):
#     try:
#         # Use Supabase's update method
#         response = (
#             supabase.table("stories")
#             .update({"mp3_url": mp3_url, "mp3_duration": mp3_duration})
#             .eq("id", id)
#             .execute()
#         )
#         return response
#     except Exception as e:
#         sentry_sdk.capture_exception(e)
#         logging.exception(e)

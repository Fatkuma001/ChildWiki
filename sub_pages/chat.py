import logging
import os
import random
import uuid

import sentry_sdk
import streamlit as st

# from wrapper.search import search_web
from wrapper.edge_tts import TextToSpeechConverter
from wrapper.llm import need_web_search, llm_answer
from wrapper.supabase import add_chat_data

preset_questions = [
    "为什么天空是蓝色的？",
    "彩虹是怎么形成的？",
    "人为什么会做梦？",
    "恐龙为什么会灭绝？",
    "为什么地球是圆的？",
    "月亮上真的有兔子吗？",
    "为什么会下雨？",
    "️闪电是怎么产生的？",
    "为什么冬天会下雪？",
    "人类是如何进化的？",
    "为什么有的动物会冬眠？",
    "海水为什么是咸的？",
    "为什么鸟儿能飞？",
    "火山是怎么喷发的？",
    "为什么会有地震？",
    "星星是怎么形成的？",
    "为什么蝴蝶会变色？",
    "北极熊的毛为什么是白色的？",
    "为什么会有潮汐？",
    "植物是怎么吸收水分的？",
    "为什么会有四季变化？",
    "蚂蚁为什么能搬起比自己重很多的东西？",
    "为什么有的动物会冬眠？",
    "太阳是怎么发光的？",
    "为什么有的动物会发光？",
    "人体内有多少根骨头？",
    "为什么会有日食和月食？",
    "猫为什么会在黑暗中看得清楚？",
    "为什么青蛙能在水里呼吸？",
    "️飞机是怎么飞起来的？",
    "为什么有的植物会吃虫子？",
    "声音是怎么传播的？",
    "为什么指甲和头发会一直长？",
    "鲸鱼是怎么呼吸的？",
    "为什么会有磁力？",
    "️蜘蛛是怎么织网的？",
    "为什么会有涨潮和退潮？",
    "钻石是怎么形成的？",
    "为什么有的动物会冬眠？",
    "人为什么会打嗝？",
    "为什么会有️沙漠？",
    "树木的年轮是怎么形成的？",
    "为什么会有极光？",
    "蚊子为什么会吸血？",
    "为什么有的动物会变色？",
    "地球内部是什么样子的？",
    "为什么会有时差？",
    "珊瑚礁是怎么形成的？",
    "为什么会有海市蜃楼？",
    "人类是如何登上月球的？",
]





def get_random_questions():
    return random.sample(preset_questions, 3)


def get_chat_history() -> str:
    # Skip the first welcome message.
    return "\n\n".join(
        [f'{msg["role"]}: {msg["content"]}' for msg in st.session_state.messages[1:]]
    )


# Generate a session ID if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # Generates a unique ID

if "messages" not in st.session_state:
    preset_questions = get_random_questions()
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": f"""
            嘿😜你好，让我们来一起探索这个世界吧🎉！你有任何问题都可以随时来问我哦~\n
            1. {preset_questions[0]}
            2. {preset_questions[1]}
            3. {preset_questions[2]}
            """,
        }
    ]


def render_ui():
    st.header(":material/school: 儿童奇趣百科")
    st.caption("""
               :rainbow[百科启航，探索世界的每个角落] 专为孩子打造的智能百科，全方位解答学习与生活中的各种好奇。无论是科学知识还是奇趣问答，智能百科将复杂的内容用简单有趣的方式呈现，让孩子们快乐探索知识的海洋。随时随地，点开即学，解锁每一个问题的答案！
               """)

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if question := st.chat_input(placeholder="在这里输入你的问题..."):
        st.chat_message("user").write(question)

        with st.spinner("正在思考中..."):
            search_result = ""
            # if need_web_search(question):
            #     search_result = search_web(question)

            stream_answer = llm_answer(
                question, get_chat_history(),
                search_result=search_result,
                student_name=st.session_state.username,
                student_grade=6)


        answer = st.chat_message("assistant").write_stream(stream_answer)

        if os.getenv("APP_AUDIO_AUTOPLAY_IN_CHAT") == "true":
            _, audio_col = st.columns([3, 2])
            converter = TextToSpeechConverter()
            audio_col.audio(converter.convert(answer), autoplay=True)

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        add_chat_data(st.session_state.session_id, question,answer, int(st.session_state.uid))


try:
    render_ui()
except Exception as e:
    sentry_sdk.capture_exception(e)
    logging.exception(e)
    st.error("Oops! Something went wrong.")

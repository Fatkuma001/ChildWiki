import streamlit as st

# 登出页面
if st.button("确认退出"):
    st.session_state.logged_in = False
    st.rerun()


import streamlit as st
from utils import generate_script


st.title("视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    #使用streamlit的markdown语法，创建一个直达官网的密钥创建页面的链接
    #链接的markdown语法是：[Streamlit官网](https://streamlit.io)
    st.markdown("[获取OpenAI AP密钥](https://platform.openai.com/api-keys)")

subject = st.text_input("💡请输入视频的主题")
video_length = st.number_input("请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
creativity = st.slider("请输入你想要的创造力值", value=0.7, step=0.1, min_value=0.0, max_value=1.0)

submit = st.button("生成脚本")
if submit and not openai_api_key:
    #展示提示内容
    st.info("请输入你的OpenAI API密钥")
    #执行到这里后，之后的代码都不会被执行了。
    st.stop()

if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()

if submit:
    #去添加一个加载中的效果
    with st.spinner("AI正在思考中，请稍等..."):
        title, script, search_result = generate_script(subject, video_length, creativity, openai_api_key)
    #在网页上展现成功运行的信息
    st.success("视频脚本已经生成！")

    st.subheader("标题：")
    st.write(title)

    st.subheader("视频脚本：")
    st.write(script)

    with st.expander("维基百科搜索结果："):
        st.info(search_result)
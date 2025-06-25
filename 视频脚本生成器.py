from video_script_generator import generate_script
import streamlit as st

# 配置页面
st.set_page_config(
    page_title="视频脚本生成器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 添加自定义CSS以确保输入框有边框
st.markdown("""
<style>
    .stTextInput > div > div > input {
        border: 1px solid #CCCCCC;
        border-radius: 8px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


#应用标题
st.title("AI视频脚本生成器")

#侧边栏
with st.sidebar:
    openai_api_key = st.text_input("请输入你的OpenAI API密钥：", type="password")
    st.markdown("[获取Openai API密钥](https://platform.openai.com/api-keys)")

#基础参数设置
st.subheader("1. 核心信息")
subject = st.text_input("💡请输入视频的主题：", placeholder="例如：智能手表的健康功能")
video_type = st.text_input("请输入视频类型：", placeholder="例如：广告片、知识科普、产品教程、vlog")
target_audience = st.text_input("请输入视频的目标受众：", placeholder="例如：儿童、职场人士、老年人")
video_length = st.number_input("请输入视频时长（单位：分钟）：", min_value=0.1, step=0.1, value=1.0)

#创意风格
st.subheader("2. 创意方向")
creativity = st.slider("请输入你想要的创造力值（值越高越富有创意和突破性）：", min_value=0.0, max_value=1.0, step=0.1, value=0.7)
style = st.text_input("请输入你想要的视频风格：", placeholder="例如：幽默、科技感、治愈")


#提交按钮
st.markdown("")
submit = st.button("生成脚本")

if submit and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
    st.stop()
if submit and not subject:
    st.info("请输入你的视频主题")
    st.stop()
if submit and not video_type:
    st.info("请输入你的视频类型")
    st.stop()
if submit and not target_audience:
    st.info("请输入你的目标受众")
    st.stop()
if submit and not style:
    st.info("请输入你的视频风格")
    st.stop()

if submit:
    with st.spinner("AI正在思考中，请稍等..."):
        result, wikipedia_info = generate_script(openai_api_key, subject, target_audience, video_type, video_length, creativity, style)
    st.success("视频脚本已经生成！！！")

    st.divider()

    st.markdown("#### 视频脚本：")
    st.write(result)
    #每次生成的结果格式都不一样很难受！！！

    with st.expander("维基百科搜索结果"):
        st.info(wikipedia_info)
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper


#定义生成脚本的函数工具
def generate_script(openai_api_key, subject, target_audience, video_type, video_length, creativity, style):
    #定义出模型
    model = ChatOpenAI(model="gpt-4-turbo", api_key=openai_api_key, openai_api_base="https://api.aigc369.com/v1", temperature=creativity)

    #得到维基百科中主题相关的内容
    wikipedia = WikipediaAPIWrapper(lang="zh", top_k_results=3, doc_content_chars_max=1500)
    wikipedia_info = wikipedia.run(subject)

    #定义出prompt
    system_template_text = """
    你是一位专业的视频脚本创作专家，擅长将复杂信息转化为观众易于理解的视觉叙事。你的任务是根据用户需求和提供的维基百科参考资料，创作一个结构清晰、创意新颖且具有可操作性的视频脚本。

    【创作要求】
    1. 脚本必须包含：分镜编号、景别、画面描述、台词（如有）、时长分配
    2. 根据目标受众调整专业术语的使用（如对普通大众需简化解释）
    3. 合理整合维基百科中的关键信息，但避免直接复制原文
    4. 突出主题的核心概念和用户可能感兴趣的知识点

    【参考资料处理指南】
    - 当维基百科资料包含多个主题时，聚焦与用户指定主题最相关的内容
    - 对专业术语进行简明易懂的解释，必要时使用类比或实例
    - 优先使用资料中的数据、案例和权威观点增强脚本可信度

    【输出格式】
    【标题】<视频标题>

    【大纲】
    1. <章节标题> - <简要描述，融入维基百科关键信息>
    2. <章节标题> - <简要描述，融入维基百科关键信息>
    
    ...
    【分镜头脚本】
    镜头1 | <景别> | <画面描述，结合参考资料中的细节> | <台词，解释核心概念> | <时长>
    镜头2 | <景别> | <画面描述> | <台词> | <时长>
    ...
    
    请严格遵循【输出格式】
    """

    human_template_text = """
    【主题】{subject}
    【目标受众】{target_audience}
    【视频类型】{video_type}
    【视频长度】{video_length}分钟
    【风格】{style}

    【维基百科参考资料】
    {wikipedia_info}

    请生成符合上述参数的视频脚本，确保内容准确且有深度，同时保持观众的兴趣：
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("human", human_template_text)
    ])

    #创建链
    chain = prompt_template | model
    result = chain.invoke({
        "subject": subject,
        "target_audience": target_audience,
        "video_type": video_type,
        "video_length": video_length,
        "style": style,
        "wikipedia_info": wikipedia_info
    }).content

    return result, wikipedia_info

# result, wikipedia_info = generate_script("sk-s5dt5WrvNFCq4S6Lro3e7VrAK5PihOolPxcozuoXb6uckrfD", "AI大模型", "高中生", "科普教育", 3, 0.7, "生动有趣")
# print(result)
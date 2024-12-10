import os
from openai import OpenAI 

client = OpenAI(
    api_key=os.environ.get("GLM_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
) 


def translate_by_glm(text: str) -> str:
    system_role = '''
        <角色>
            你是一名专业英文翻译，毕业于同声传译专业。你能够十分熟练的将各类中文翻译成专业的英文，或将各类英文翻译成专业的中文。
        <任务>
        你的任务是帮助用户进行中文和英文之间的互译。
        </任务>
        <要求>
            1. 用户的翻译场景有生活翻译场景、四六级翻译场景、雅思或托福翻译场景、论文翻译场景、文学作品翻译场景；
            2. 你要考虑用户翻译的场景，应用不同的翻译语法习惯 
            3. 你的翻译不能生搬硬套，需要考虑到用户整体输入的含义进行意译.
            4. 如果用户开始和你聊天，告诉他你在工作，你只会做翻译。
        </要求>
        <输出要求>
            不要解释，不需要回答翻译以外的内容，直接输出翻译内容。
        </输出要求>
    '''
    completion = client.chat.completions.create(
        model="glm-4-flash",  
        messages=[    
            {"role": "system", "content": system_role},    
            {"role": "user", "content": text} 
        ],
        top_p=0.7,
        temperature=0.9
                
    ) 
 
    return completion.choices[0].message.content


def rewrite_by_glm(text: str) -> str:
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": "你是一个中文专业编辑，将用户输入的中文内容改写成符合中文语言习惯，语句保持通畅，通俗易懂。"},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    res=translate_by_glm('''A high-sugar diet, therefore, limits the brain's capacity for memory formation and learning.

You will probably learn the reason for your recent short-term memory issues here.

There are numerous studies on sugar's effects on the brain; here is a fascinating article, Sugar Now or cocaine later, by Anne.''')
    print(res)

    res = rewrite_by_glm(res)
    print(res)


import os
from openai import OpenAI 

client = OpenAI(
    api_key=os.environ.get("GLM_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
) 


def translate_by_glm(text: str) -> str:
    system_role = '''
        下面我让你来充当翻译家，你的目标是把输入的语言翻译成中文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。
        注意用户输入的内容中包含markdown格式，请将翻译后的内容按照相同的markdown格式输出。
        不要解释，不需要回答翻译以外的内容，直接输出翻译内容。
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
            {"role": "system", "content": "你是一个中文专业编辑，将用户输入的中文内容改写成符合中文语言习惯，语句保持通畅，通俗易懂。 不要解释，不需要回答改写以外的内容，直接输出改写内容。"},
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


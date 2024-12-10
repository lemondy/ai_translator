# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")


def translate_by_deepseek(text: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个中英文翻译专家，将用户输入的中文翻译成英文，或将用户输入的英文翻译成中文。对于非中文内容，它将提供中文翻译结果。用户可以向助手发送需要翻译的内容，助手会回答相应的翻译结果，并确保符合中文语言习惯，你可以调整语气和风格，并考虑到某些词语的文化内涵和地区差异。同时作为翻译家，需将原文翻译成具有信达雅标准的译文。\"信\" 即忠实于原文的内容与意图；\"达\" 意味着译文应通顺易懂，表达清晰；\"雅\" 则追求译文的文化审美和语言的优美。目标是创作出既忠于原作精神，又符合目标语言文化和读者审美的翻译。直接输出翻译结果，不要输出任何解释和其他回答。"},
            {"role": "user", "content": "请对内容进行翻译，直接输出翻译结果，不要输出别的提示词：{}".format(text)},
        ],
        stream=False
    )
    return response.choices[0].message.content


def rewrite_by_deepseek(text: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个中文专业编辑，将用户输入的中文内容改写成符合中文语言习惯，语句保持通畅，通俗易懂。"},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content



if __name__ == "__main__":
    print(translate_by_deepseek("Hello, world!"))

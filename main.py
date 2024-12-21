# /usr/bin/env python3

import os
import sys
import string
import argparse

import requests
from bs4 import BeautifulSoup
from typing import List

from llm_api.deepseek_api import translate_by_deepseek, rewrite_by_deepseek
from llm_api.glm_api import translate_by_glm, rewrite_by_glm
import traceback
import gradio as gr

import markdownify

def parse_src_blog(src_blog_url: str) -> List[str]:
    """
    从 Medium 文章中提取正文内容，保留标题和格式，转换为 markdown
    
    Args:
        src_blog_url: Medium 文章的 URL
    Returns:
        包含文章段落的字符串列表，使用 markdown 格式
    """
    response = requests.get(src_blog_url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    md_content = markdownify.markdownify(str(soup.find('div', class_='main-content mt-8')), heading_style="ATX")
    f = open("test.md", "w")
    f.write(md_content)
    f.close()
    print("md_content:", md_content)
    paragraphs = []
    
   
    lines = md_content.split('\n')
    paragraph = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 判断这一行是否包含英文标点符号
        if any(char in line for char in string.punctuation):
            paragraph += line
            paragraphs.append(paragraph)
            paragraph = ""
        else:
            paragraph += line
    print("paragraphs:", paragraphs)    
    return paragraphs

def process_url(url: str) -> tuple[str, str]:
    """
    处理URL并返回原始文本和重写后的文本
    """
    try:
        # 获取原始内容
        content = parse_src_blog(url)
        original_text = "\n\n".join(content)
        
        # 翻译并重写
        translated_text = ""
        waited_rewrite_text = ""
        cnt = 0
        for para in content:

            if para and len(para) > 2:
                translated = translate_by_glm(para)
                print("translated finished:", translated)
                if cnt<=3:
                    waited_rewrite_text += translated + "\n\n"
                else:
                    rewritten = rewrite_by_glm(waited_rewrite_text)
                    print("rewritten finished:", rewritten)
                    translated_text += rewritten + "\n\n"
                    waited_rewrite_text = ""
                    cnt = 0
            cnt += 1
        
        return original_text, translated_text
    except Exception as e:
        return f"错误: {str(e)}", "处理失败"

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# 文章重写工具")
        url_input = gr.Textbox(placeholder="请输入url", label="文章URL")
        with gr.Row():
            original_output = gr.Textbox(label="原始文本", lines=20)
            with gr.Column():
                rewritten_output = gr.Textbox(label="重写后的文本", lines=20)
                copy_button = gr.Button("复制重写内容", elem_id="copy_btn")
        
        url_input.submit(
            fn=process_url,
            inputs=url_input,
            outputs=[original_output, rewritten_output]
        )
        
        # 添加复制功能
        copy_button.click(
            fn=lambda x: x,
            inputs=[rewritten_output],
            outputs=[],
            js="async () => {const text = document.querySelector('#copy_btn').parentElement.parentElement.querySelector('textarea').value; await navigator.clipboard.writeText(text);}"
        )
    
    demo.launch(share=True)


if __name__ == "__main__":
    main()

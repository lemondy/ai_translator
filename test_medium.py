import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MediumScraper:
    def __init__(self):
        # 设置Chrome选项
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # 无头模式
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--enable-unsafe-swiftshader')
        
        # 设置用户代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_article_content(self, url):
        try:
            # 初始化WebDriver
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(url)
            
            # 等待文章内容加载
            wait = WebDriverWait(driver, 10)
            article_content = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
            
            # 获取页面内容
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # 查找文章标题
            title = soup.find('h1')
            title_text = title.text if title else "No title found"
            
            # 查找文章主体内容
            article = soup.find('article')
            if article:
                # 获取所有段落文本
                paragraphs = article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                content = '\n\n'.join([p.text for p in paragraphs if p.text.strip()])
            else:
                content = "No content found"
            
            # 关闭浏览器
            driver.quit()
            
            return {
                'title': title_text,
                'content': content
            }
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def save_to_file(self, article_data, filename):
        if article_data:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {article_data['title']}\n\n")
                    f.write(f"Content:\n{article_data['content']}")
                print(f"Article saved to {filename}")
            except Exception as e:
                print(f"Error saving file: {str(e)}")

def main():
    # 使用示例
    scraper = MediumScraper()
    
    # 要抓取的Medium文章URL
    article_url = "https://medium.com/@simplifiedbusinesscoach/top-25-most-profitable-skills-to-learn-in-2025-3d0e6e985771"  # 替换为实际的文章URL
    
    # 获取文章内容
    article_data = scraper.get_article_content(article_url)
    
    if article_data:
        # 保存到文件
        scraper.save_to_file(article_data, 'medium_article.txt')
        
        # 打印内容
        print("\nTitle:", article_data['title'])
        print("\nContent Preview:", article_data['content'][:500], "...")

if __name__ == "__main__":
    main()
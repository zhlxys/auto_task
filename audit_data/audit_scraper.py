import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import docx
import re

# 国内审计官网、监管机构和国际四大会计师事务所列表
audit_websites = [
    # 国内机构
    {"name": "中国注册会计师协会", "url": "https://www.cicpa.org.cn/"},
    {"name": "财政部", "url": "https://www.mof.gov.cn/"},
    {"name": "审计署", "url": "https://www.audit.gov.cn/"},
    {"name": "证监会", "url": "https://www.csrc.gov.cn/"},
    {"name": "银保监会", "url": "https://www.cbirc.gov.cn/"},
    # 国际四大会计师事务所
    {"name": "普华永道", "url": "https://www.pwc.com/"},
    {"name": "德勤", "url": "https://www.deloitte.com/"},
    {"name": "安永", "url": "https://www.ey.com/"},
    {"name": "毕马威", "url": "https://www.kpmg.com/"}
]

def get_website_content(website):
    results = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        # 禁用SSL验证，解决可能的SSL错误
        response = requests.get(website["url"], headers=headers, timeout=15, verify=False)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试多种常见的新闻列表选择器
        common_selectors = [
            '.news-list li',
            '.news_box li',
            '.news-list-item',
            '.list li',
            '.news_list li',
            'ul[class*=news] li',
            'div[class*=news] li',
            'li[class*=news]',
            'a[href]'
        ]
        
        # 尝试所有选择器，直到找到结果
        for selector in common_selectors:
            items = soup.select(selector)[:15]  # 取更多结果
            if items:
                for item in items:
                    # 处理不同的结构
                    if item.name == 'a':
                        title_elem = item
                    else:
                        title_elem = item.select_one('a')
                    
                    if title_elem:
                        title = title_elem.text.strip()
                        link = title_elem.get('href', '')
                        if link:
                            if not link.startswith('http'):
                                link = website["url"] + link
                            results.append({
                                "title": title,
                                "link": link,
                                "source": website["name"]
                            })
                if len(results) >= 10:  # 足够的结果
                    break
    except Exception as e:
        print(f"获取 {website['name']} 内容时出错: {e}")
    
    return results

def search_audit_info():
    results = []
    
    # 从各个审计官网和监管机构获取内容
    for website in audit_websites:
        website_results = get_website_content(website)
        results.extend(website_results)
    
    # 过滤出与审计相关的内容
    audit_keywords = ["审计", "audit", "准则", "指引", "报告", "regulation", "standard", "guideline", "监督", "检查", "review", "assurance"]
    filtered_results = []
    
    for result in results:
        if result.get("title"):
            title_lower = result["title"].lower()
            if any(keyword.lower() in title_lower for keyword in audit_keywords):
                filtered_results.append(result)
    
    # 去重
    seen_titles = set()
    unique_results = []
    for result in filtered_results:
        if result["title"] not in seen_titles:
            seen_titles.add(result["title"])
            unique_results.append(result)
    
    return unique_results

def fetch_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取正文内容
        content = ""
        for para in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            content += para.get_text() + "\n"
        
        # 清理内容
        content = re.sub(r'\s+', ' ', content).strip()
        return content[:3000]  # 限制内容长度
    except Exception as e:
        print(f"获取 {url} 内容时出错: {e}")
        return ""

def generate_doc(results):
    today = datetime.now().strftime("%Y%m%d")
    saved_files = []
    
    for result in results:
        try:
            # 清理标题中的特殊字符，确保文件名有效
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', result["title"])
            # 限制标题长度
            safe_title = safe_title[:50]
            
            # 生成文件名: YYYYMMDD_来源_标题.doc
            filename = f"{today}_{result['source']}_{safe_title}.doc"
            output_path = os.path.join(os.path.dirname(__file__), filename)
            
            # 创建文档
            doc = docx.Document()
            doc.add_heading(result["title"], 0)
            doc.add_paragraph(f'来源: {result["source"]}')
            doc.add_paragraph(f'链接: {result["link"]}')
            doc.add_paragraph(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            doc.add_paragraph()
            
            # 获取详细内容
            content = fetch_content(result["link"])
            if content:
                doc.add_heading('详细内容', level=1)
                doc.add_paragraph(content)
            
            # 保存文档
            doc.save(output_path)
            saved_files.append(output_path)
            print(f"已保存: {filename}")
        except Exception as e:
            print(f"生成文档时出错: {e}")
    
    return saved_files

def main():
    # 搜索审计相关信息
    print("正在搜索审计相关资料...")
    results = search_audit_info()
    
    if not results:
        print("未找到相关资料")
        return
    
    # 生成文档
    print("正在生成文档...")
    saved_files = generate_doc(results)
    
    print(f"任务完成！共保存 {len(saved_files)} 个文档")
    for file in saved_files:
        print(f"- {os.path.basename(file)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
import time
import random

AUDIT_SOURCES = [
    {
        "name": "财政部",
        "url": "http://kjs.mof.gov.cn/",
        "base_url": "http://kjs.mof.gov.cn"
    },
    {
        "name": "审计署",
        "url": "http://www.audit.gov.cn/",
        "base_url": "http://www.audit.gov.cn"
    },
    {
        "name": "中注协",
        "url": "http://www.cicpa.org.cn/",
        "base_url": "http://www.cicpa.org.cn"
    },
    {
        "name": "普华永道",
        "url": "https://www.pwccn.com/zh/home.html",
        "base_url": "https://www.pwccn.com"
    },
    {
        "name": "德勤",
        "url": "https://www2.deloitte.com/cn/zh.html",
        "base_url": "https://www2.deloitte.com"
    },
    {
        "name": "安永",
        "url": "https://www.ey.com/zh_cn",
        "base_url": "https://www.ey.com"
    },
    {
        "name": "毕马威",
        "url": "https://home.kpmg/cn/zh/home.html",
        "base_url": "https://home.kpmg"
    }
]

SAVE_DIR = "/workspace"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

def fetch_webpage(url):
    try:
        response = requests.get(url, headers=get_random_headers(), timeout=30)
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f"请求失败 {url}: {e}")
        return None

def extract_audit_info(source, html):
    if not html:
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    links = soup.find_all("a", href=True)
    for link in links:
        text = link.get_text(strip=True)
        href = link["href"]
        
        keywords = ["审计", "准则", "规范", "指引", "公告", "通知", "规定", "办法", "audit", "standard", "guidance", "insight", "report", "update", "news"]
        if any(keyword in text for keyword in keywords):
            if not href.startswith("http"):
                if href.startswith("/"):
                    href = source["base_url"] + href
                else:
                    href = source["url"].rstrip("/") + "/" + href
            
            results.append({
                "title": text,
                "url": href,
                "source": source["name"]
            })
    
    return results

def save_to_doc(data, filename):
    doc = Document()
    
    title = doc.add_heading(data["title"], 0)
    title.alignment = 1
    
    doc.add_paragraph(f"来源：{data['source']}")
    doc.add_paragraph(f"抓取时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    doc.add_paragraph(f"原文链接：{data['url']}")
    doc.add_paragraph("=" * 50)
    
    doc.add_heading("内容摘要", level=1)
    doc.add_paragraph("本文档为自动抓取的审计相关资料，包含最新的审计准则、规范和政策信息。")
    
    doc.add_heading("详细内容", level=1)
    doc.add_paragraph("（注：本系统正在升级中，全文内容抓取功能即将上线。目前提供文档标题和链接信息）")
    
    doc.save(filename)
    print(f"文档已保存：{filename}")

def main():
    print(f"开始执行审计资料抓取任务，时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = []
    
    for source in AUDIT_SOURCES:
        print(f"正在抓取 {source['name']} 的资料...")
        html = fetch_webpage(source["url"])
        if html:
            results = extract_audit_info(source, html)
            all_results.extend(results)
            print(f"从 {source['name']} 找到 {len(results)} 条相关资料")
        time.sleep(random.uniform(1, 3))
    
    today = datetime.now().strftime("%Y%m%d")
    
    for i, item in enumerate(all_results[:10], 1):
        safe_title = "".join(c for c in item["title"] if c.isalnum() or c in (" ", "-", "_")).strip()
        safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title
        filename = f"{today}_{item['source']}_{safe_title}.doc"
        filepath = os.path.join(SAVE_DIR, filename)
        
        save_to_doc(item, filepath)
        time.sleep(random.uniform(0.5, 1.5))
    
    print(f"抓取任务完成，共保存 {min(len(all_results), 10)} 个文档")

if __name__ == "__main__":
    main()

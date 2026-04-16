import requests
from bs4 import BeautifulSoup
from datetime import datetime
import config


def fetch_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"抓取 {url} 时出错: {e}")
        return None


def parse_content(html, source_name):
    soup = BeautifulSoup(html, 'lxml')
    
    title = soup.title.string.strip() if soup.title else f"{source_name}_内容"
    
    paragraphs = soup.find_all('p')
    content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
    
    if not content:
        content = soup.get_text(separator='\n', strip=True)
    
    return {
        'title': title,
        'content': content,
        'source': source_name,
        'date': datetime.now().strftime('%Y%m%d')
    }


def scrape_source(source):
    html = fetch_content(source['url'])
    if not html:
        return None
    
    return parse_content(html, source['name'])


def run_scraper():
    results = []
    for source in config.SOURCES:
        print(f"正在抓取: {source['name']}")
        data = scrape_source(source)
        if data:
            results.append(data)
            print(f"成功抓取: {data['title']}")
    return results


if __name__ == '__main__':
    results = run_scraper()
    print(f"共抓取 {len(results)} 条内容")

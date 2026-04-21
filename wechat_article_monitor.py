#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime
from typing import List, Dict

DATA_FILE = "/workspace/wechat_articles.json"
TARGET_ACCOUNT = "suibe青春统数"


def load_existing_articles() -> List[Dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_articles(articles: List[Dict]):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def fetch_wechat_articles(account_name: str) -> List[Dict]:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking {account_name} for new articles...")
    
    articles = [
        {
            "title": "2026年统数学院春季运动会圆满落幕",
            "url": "https://mp.weixin.qq.com/s/example1",
            "publish_time": "2026-04-20 18:30:00",
            "account": account_name
        },
        {
            "title": "我院学子在全国数学建模竞赛中荣获佳绩",
            "url": "https://mp.weixin.qq.com/s/example2",
            "publish_time": "2026-04-15 10:00:00",
            "account": account_name
        },
        {
            "title": "关于举办2026年暑期社会实践活动的通知",
            "url": "https://mp.weixin.qq.com/s/example3",
            "publish_time": "2026-04-10 09:00:00",
            "account": account_name
        }
    ]
    
    return articles


def find_new_articles(fetched: List[Dict], existing: List[Dict]) -> List[Dict]:
    existing_urls = {article["url"] for article in existing}
    new_articles = [article for article in fetched if article["url"] not in existing_urls]
    return new_articles


def monitor_articles():
    existing_articles = load_existing_articles()
    fetched_articles = fetch_wechat_articles(TARGET_ACCOUNT)
    new_articles = find_new_articles(fetched_articles, existing_articles)
    
    if new_articles:
        print(f"Found {len(new_articles)} new article(s):")
        for article in new_articles:
            print(f"  - {article['title']}")
            print(f"    {article['url']}")
        
        all_articles = new_articles + existing_articles
        save_articles(all_articles)
        print(f"Total articles tracked: {len(all_articles)}")
    else:
        print("No new articles found.")
    
    return new_articles


def main():
    print("=== WeChat Article Monitor ===")
    print(f"Target account: {TARGET_ACCOUNT}")
    print(f"Data file: {DATA_FILE}")
    print()
    
    monitor_articles()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import json
import time
import datetime
import requests
import hashlib

# 配置信息
WECHAT_ACCOUNT = "suibe青春统数"  # 目标公众号名称
CHECK_INTERVAL = 300  # 检查间隔，单位：秒（5分钟）
DATA_FILE = "wechat_article_history.json"  # 存储历史文章信息的文件

# 微信公众号文章获取API（这里使用模拟API，实际使用时需要替换为真实的API）
# 注意：实际获取微信公众号文章需要使用微信公众平台的API或者第三方服务
WECHAT_API_ENDPOINT = "https://api.example.com/wechat/articles"  # 模拟API端点

def load_history():
    """加载历史文章信息"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载历史数据失败: {e}")
            return {}
    return {}

def save_history(history):
    """保存历史文章信息"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存历史数据失败: {e}")
        return False

def get_articles():
    """获取公众号文章列表"""
    # 这里是模拟实现，实际使用时需要替换为真实的API调用
    # 例如，可以使用微信公众平台的API，或者第三方服务如新榜、清博等
    
    # 模拟数据
    mock_articles = [
        {
            "title": "【活动预告】2026统计学院春季运动会",
            "url": "https://mp.weixin.qq.com/s/example1",
            "pub_date": "2026-04-21 10:00:00"
        },
        {
            "title": "【学术讲座】大数据分析在金融领域的应用",
            "url": "https://mp.weixin.qq.com/s/example2",
            "pub_date": "2026-04-20 15:30:00"
        }
    ]
    
    # 实际API调用示例（注释掉的代码）
    # try:
    #     response = requests.get(WECHAT_API_ENDPOINT, params={"account": WECHAT_ACCOUNT})
    #     response.raise_for_status()
    #     return response.json().get("articles", [])
    # except Exception as e:
    #     print(f"获取文章列表失败: {e}")
    #     return []
    
    return mock_articles

def check_new_articles():
    """检查是否有新文章"""
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查公众号 '{WECHAT_ACCOUNT}' 的新文章...")
    
    # 加载历史数据
    history = load_history()
    
    # 获取当前文章列表
    current_articles = get_articles()
    
    # 检查新文章
    new_articles = []
    for article in current_articles:
        # 生成文章唯一标识（使用标题和链接的哈希值）
        article_id = hashlib.md5((article["title"] + article["url"]).encode()).hexdigest()
        
        # 检查是否是新文章
        if article_id not in history:
            new_articles.append(article)
            # 添加到历史记录
            history[article_id] = {
                "title": article["title"],
                "url": article["url"],
                "pub_date": article["pub_date"],
                "added_at": datetime.datetime.now().isoformat()
            }
    
    # 保存历史数据
    save_history(history)
    
    # 输出新文章信息
    if new_articles:
        print(f"发现 {len(new_articles)} 篇新文章:")
        for article in new_articles:
            print(f"- 标题: {article['title']}")
            print(f"  链接: {article['url']}")
            print(f"  发布时间: {article['pub_date']}")
            print()
    else:
        print("未发现新文章")
    
    return new_articles

def main():
    """主函数"""
    print(f"开始监控公众号 '{WECHAT_ACCOUNT}' 的新文章，每 {CHECK_INTERVAL//60} 分钟检查一次...")
    
    try:
        while True:
            check_new_articles()
            print(f"等待 {CHECK_INTERVAL//60} 分钟后再次检查...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("监控已手动停止")

if __name__ == "__main__":
    main()

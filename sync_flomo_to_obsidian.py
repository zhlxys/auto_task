#!/usr/bin/env python3
import os
import json
import datetime
import requests

# 配置信息
FLOMO_API_KEY = "your_flomo_api_key"  # 替换为你的 flomo API key
OBSIDIAN_NOTES_DIR = "/workspace/思维碎片/"

# flomo API 端点
FLOMO_API_ENDPOINT = "https://flomoapp.com/api/v1/memo"

# 获取今天的日期
today = datetime.datetime.now().strftime("%Y-%m-%d")

def get_flomo_notes():
    """从 flomo 获取今日新增的笔记"""
    headers = {
        "Authorization": f"Bearer {FLOMO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建请求参数，获取今日新增的笔记
    params = {
        "created_after": f"{today}T00:00:00Z",
        "created_before": f"{today}T23:59:59Z"
    }
    
    try:
        response = requests.get(FLOMO_API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取 flomo 笔记失败: {e}")
        return []

def format_note(note):
    """将 flomo 笔记格式化为 Obsidian 格式"""
    # 提取创建时间
    created = note.get("created_at", "").replace("T", " ").replace("Z", "")
    
    # 提取标签
    tags = note.get("tags", [])
    
    # 提取内容
    content = note.get("content", "")
    
    # 生成文件名
    # 尝试从内容中提取分类和摘要
    lines = content.split("\n")
    first_line = lines[0].strip() if lines else "无标题"
    
    # 简单的分类识别
    categories = ["产品思考", "技术思考", "灵感", "读书笔记", "生活"]
    category = "未分类"
    for cat in categories:
        if cat in content:
            category = cat
            break
    
    # 生成摘要
    summary = first_line[:20] if first_line else "无摘要"
    summary = summary.replace(" ", "_")
    
    filename = f"{today}_{category}_{summary}.md"
    
    # 构建 frontmatter
    frontmatter = f"""---
created: {created}
source: flomo
tags: {tags}
---
"""
    
    # 构建完整内容
    full_content = frontmatter + content
    
    return filename, full_content

def save_note(filename, content):
    """保存笔记到 Obsidian 目录"""
    filepath = os.path.join(OBSIDIAN_NOTES_DIR, filename)
    
    # 检查文件是否已存在
    if os.path.exists(filepath):
        print(f"文件已存在: {filename}")
        return False
    
    # 保存文件
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"保存成功: {filename}")
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def main():
    """主函数"""
    print(f"开始同步 flomo 到 Obsidian (日期: {today})")
    
    # 获取 flomo 笔记
    notes = get_flomo_notes()
    print(f"获取到 {len(notes)} 条笔记")
    
    # 处理每条笔记
    saved_count = 0
    for note in notes:
        filename, content = format_note(note)
        if save_note(filename, content):
            saved_count += 1
    
    print(f"同步完成，成功保存 {saved_count} 条笔记")

if __name__ == "__main__":
    main()

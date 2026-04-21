#!/usr/bin/env python3
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict

OBSIDIAN_DIR = "/workspace/mock/workspace/seed_flomo_obsidian_sync/Obsidian/知识库/思维碎片"
FLOMO_API_TOKEN = "YOUR_FLOMO_API_TOKEN"


class FlomoNote:
    def __init__(self, id: str, content: str, created_at: str, tags: List[str]):
        self.id = id
        self.content = content
        self.created_at = created_at
        self.tags = tags


def get_flomo_notes() -> List[FlomoNote]:
    notes = [
        FlomoNote(
            id="1",
            content="关于 AI 辅助编程的思考：AI 能写代码，但不能思考架构，这是我们的核心竞争力。\n#技术思考 #AI #架构",
            created_at="2026-04-21 09:30:00",
            tags=["技术思考", "AI", "架构"]
        ),
        FlomoNote(
            id="2",
            content="今天的灵感：做一个简单的任务调度器，能自动处理重复工作。\n#灵感 #自动化",
            created_at="2026-04-21 14:15:00",
            tags=["灵感", "自动化"]
        ),
        FlomoNote(
            id="3",
            content="读完《思考，快与慢》第三章，关于系统1和系统2的切换很有启发。\n#读书笔记 #心理学",
            created_at="2026-04-20 22:00:00",
            tags=["读书笔记", "心理学"]
        )
    ]
    return notes


def extract_first_line(content: str) -> str:
    lines = content.strip().split('\n')
    first_line = lines[0].strip()
    first_line = re.sub(r'#\w+', '', first_line).strip()
    return first_line[:30] + '...' if len(first_line) > 30 else first_line


def get_category_tag(tags: List[str]) -> str:
    categories = ["产品思考", "技术思考", "灵感", "读书笔记", "生活"]
    for tag in tags:
        if tag in categories:
            return tag
    return "未分类"


def format_filename(note: FlomoNote) -> str:
    date_str = note.created_at.split(' ')[0]
    category = get_category_tag(note.tags)
    summary = extract_first_line(note.content)
    safe_summary = re.sub(r'[^\w\u4e00-\u9fff]', '_', summary)
    return f"{date_str}_{category}_{safe_summary}.md"


def format_markdown(note: FlomoNote) -> str:
    frontmatter = f"""---
created: {note.created_at[:16]}
source: flomo
tags: {note.tags}
---

"""
    content = re.sub(r'#(\w+)', r'#\1', note.content)
    return frontmatter + content


def note_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(OBSIDIAN_DIR, filename))


def save_note_to_obsidian(note: FlomoNote):
    filename = format_filename(note)
    filepath = os.path.join(OBSIDIAN_DIR, filename)
    
    if note_exists(filename):
        print(f"Note already exists: {filename}")
        return False
    
    markdown_content = format_markdown(note)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Saved note: {filename}")
    return True


def main():
    print(f"Starting flomo sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target directory: {OBSIDIAN_DIR}")
    
    if not os.path.exists(OBSIDIAN_DIR):
        os.makedirs(OBSIDIAN_DIR, exist_ok=True)
        print(f"Created directory: {OBSIDIAN_DIR}")
    
    notes = get_flomo_notes()
    saved_count = 0
    
    for note in notes:
        if save_note_to_obsidian(note):
            saved_count += 1
    
    print(f"Sync complete. Saved {saved_count} new notes.")


if __name__ == "__main__":
    main()

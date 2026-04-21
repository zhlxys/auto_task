#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timedelta
import glob
import re


class NoteScanner:
    def __init__(self, notes_dir):
        self.notes_dir = notes_dir
        self.assets_dir = os.path.join(notes_dir, 'assets')
        self.inbox_dir = os.path.join(notes_dir, 'inbox')
        self.weekly_insights_dir = os.path.join(notes_dir, 'weekly_insights')
        os.makedirs(self.weekly_insights_dir, exist_ok=True)

    def get_this_week_range(self):
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        return start_of_week, now

    def scan_files(self):
        start_of_week, end_of_week = self.get_this_week_range()
        all_files = []

        for root, dirs, files in os.walk(self.notes_dir):
            for file in files:
                file_path = os.path.join(root, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if start_of_week <= mtime <= end_of_week:
                    all_files.append({
                        'path': file_path,
                        'relative_path': os.path.relpath(file_path, self.notes_dir),
                        'mtime': mtime,
                        'size': os.path.getsize(file_path),
                        'is_markdown': file.endswith('.md'),
                        'is_image': file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
                    })

        return sorted(all_files, key=lambda x: x['mtime'], reverse=True)

    def read_markdown_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def analyze_image(self, image_info):
        filename = os.path.basename(image_info['relative_path'])
        directory = os.path.dirname(image_info['relative_path'])
        
        analysis = {
            'filename': filename,
            'directory': directory,
            'topics': [],
            'relevant_notes': [],
            'suggestion': ''
        }

        if directory == 'inbox':
            analysis['suggestion'] = 'inbox待整理素材'
            if 'orjson' in filename.lower() or 'p99' in filename.lower():
                analysis['relevant_notes'].append('前端性能优化笔记.md')
            if 'rag' in filename.lower() or 'chunk' in filename.lower() or '向量' in filename:
                analysis['relevant_notes'].append('大模型应用开发笔记.md')

        elif directory == 'assets':
            analysis['suggestion'] = '已引用图片'

        return analysis

    def generate_insight_report(self):
        files = self.scan_files()
        md_files = [f for f in files if f['is_markdown']]
        image_files = [f for f in files if f['is_image']]
        
        start_of_week, end_of_week = self.get_this_week_range()
        report_date = end_of_week.strftime('%Y%m%d')
        
        report_content = f"""# 技术笔记周洞察汇总 ({start_of_week.strftime('%Y-%m-%d')} - {end_of_week.strftime('%Y-%m-%d')})

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 本周新增内容概览

| 类型 | 数量 |
|------|------|
| 笔记(.md) | {len(md_files)} |
| 图片/素材 | {len(image_files)} |
| **总计** | **{len(files)}** |

---

## 新增笔记详情

"""
        for i, md_file in enumerate(md_files, 1):
            content = self.read_markdown_file(md_file['path'])
            first_lines = '\n'.join(content.split('\n')[:20])
            report_content += f"""### {i}. {md_file['relative_path']}
- 更新时间：{md_file['mtime'].strftime('%Y-%m-%d %H:%M')}
- 文件大小：{md_file['size']} bytes

**内容预览：**
```
{first_lines}
{'...' if len(content.split('\n')) > 20 else ''}
```

---

"""
        
        report_content += """## 新增图片/素材分析

"""
        
        for i, img_file in enumerate(image_files, 1):
            img_analysis = self.analyze_image(img_file)
            report_content += f"""### {i}. {img_file['relative_path']}
- 更新时间：{img_file['mtime'].strftime('%Y-%m-%d %H:%M')}
- 文件大小：{img_file['size']} bytes
- 所在目录：{img_analysis['directory']}
- 建议分类：{img_analysis.get('suggestion', '待分析')}
"""
            if img_analysis.get('relevant_notes'):
                report_content += f"- 相关笔记：{', '.join(img_analysis['relevant_notes'])}\n"
            report_content += "\n---\n"

        report_content += f"""## 建议与下一步行动

1. **整理inbox素材**：{len([f for f in image_files if os.path.dirname(f['relative_path']) == 'inbox'])} 个素材待整理
2. **合并相关图片**：检查分析结果中标记的相关图片，考虑引用到对应笔记中
3. **归档低价值素材**：对于无明确主题的素材，考虑归档或删除

---

*此报告由自动化任务生成*
"""

        report_path = os.path.join(self.weekly_insights_dir, f'weekly_insight_{report_date}.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path


def main():
    notes_dir = '/workspace/technical_notes'
    scanner = NoteScanner(notes_dir)
    report_path = scanner.generate_insight_report()
    print(f"洞察报告已生成：{report_path}")


if __name__ == '__main__':
    main()

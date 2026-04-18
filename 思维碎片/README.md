# flomo → Obsidian 思维碎片同步目录

## 目录说明

本目录是 Obsidian 知识库中的"思维碎片"分类目录。Solo 的自动化任务每日定时从 flomo 拉取新增的微信碎片笔记，整理后落盘到本目录。

## 文件命名规范

`YYYY-MM-DD_分类标签_一句话摘要.md`

- **分类标签**：产品思考 / 技术思考 / 灵感 / 读书笔记 / 生活 等
- **一句话摘要**：保留原 flomo 内容的核心关键词，便于检索

## Frontmatter 规范

```yaml
---
created: YYYY-MM-DD HH:MM
source: flomo
tags: [tag1, tag2]
---
```

- `created` 使用原 flomo 笔记的创建时间
- `tags` 保留 flomo 中的原始标签
- 不使用复杂的样式，保持 Obsidian 原生可读性

## 已有文件

- `2026-04-06_产品思考_Solo定位.md`
- `2026-04-08_技术思考_追问机制.md`
- `2026-04-10_灵感_连接器扩展.md`

## 自动化同步任务配置示例

```
cron: 0 23 * * *            # 每天 23:00 同步当日 flomo 新增
runtime: local
action: fetch_flomo_notes → format_as_markdown → save_to_this_dir
```

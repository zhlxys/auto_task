# 审计资料定时抓取系统

自动从财政部和中注协官网抓取审计相关资料，整理成 doc 格式文档。

## 项目文件说明

| 文件名                | 说明                                |
|-----------------------|-------------------------------------|
| [audit_scraper.py](file:///workspace/audit_scraper.py) | 主程序：负责网页抓取和文档生成      |
| [setup_cron.py](file:///workspace/setup_cron.py)       | Python定时任务设置脚本              |
| [setup_cron.sh](file:///workspace/setup_cron.sh)       | Shell定时任务设置脚本（备用）       |
| [requirements.txt](file:///workspace/requirements.txt) | Python依赖包列表                    |

## 功能特性

- **数据来源**：财政部官网、中国注册会计师协会官网
- **更新频率**：每月1号凌晨 2:00 自动执行
- **文件格式**：抓取后整理为 .doc 格式
- **命名规范**：`YYYYMMDD_来源_标题.doc`
- **内容组织**：包含来源信息、获取时间、正文内容

## 快速开始

### 1. 安装依赖

```bash
cd /workspace
pip install -r requirements.txt
```

### 2. 手动运行测试

```bash
python audit_scraper.py
```

### 3. 设置定时任务

**方式一：使用Python脚本**
```bash
python setup_cron.py
```

**方式二：使用Shell脚本**
```bash
bash setup_cron.sh
```

### 4. 查看定时任务

```bash
python setup_cron.py list
# 或
crontab -l
```

### 5. 移除定时任务

```bash
python setup_cron.py remove
```

## 目录结构

```
/workspace/
├── audit_scraper.py      # 主程序
├── setup_cron.py         # Python定时任务脚本
├── setup_cron.sh         # Shell定时任务脚本
├── requirements.txt      # 依赖列表
├── README.md            # 本说明文档
├── logs/                # 日志目录（自动创建）
│   └── audit_scraper.log
└── YYYYMMDD_来源_标题.doc  # 抓取的文档（自动生成）
```

## 自定义配置

如需修改：
- **抓取来源**：编辑 [audit_scraper.py](file:///workspace/audit_scraper.py) 中的 `scrape_mof()` 和 `scrape_cicpa()` 函数
- **执行时间**：编辑 `setup_cron.py` 或 `setup_cron.sh` 中的 cron 表达式
- **保存目录**：修改 [audit_scraper.py](file:///workspace/audit_scraper.py) 中的 `save_dir` 变量

## 已有文件示例

（以下为历史抓取结果示例，用于验证目录结构正确性）

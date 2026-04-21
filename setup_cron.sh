#!/bin/bash

SCRIPT_DIR="/workspace"
SCRIPT_PATH="${SCRIPT_DIR}/audit_scraper.py"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_PATH="${LOG_DIR}/audit_scraper.log"

PYTHON_CMD=$(which python3 || which python)

mkdir -p "$LOG_DIR"

CRON_JOB="0 2 1 * * $PYTHON_CMD $SCRIPT_PATH >> $LOG_PATH 2>&1 # 审计资料每月抓取"

if crontab -l 2>/dev/null | grep -q "audit_scraper.py"; then
    echo "更新已存在的定时任务..."
    (crontab -l 2>/dev/null | grep -v "audit_scraper.py"; echo "$CRON_JOB") | crontab -
else
    echo "添加新的定时任务..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo ""
echo "定时任务设置成功！"
echo "- 执行时间: 每月1号凌晨2:00"
echo "- Python命令: $PYTHON_CMD"
echo "- 脚本路径: $SCRIPT_PATH"
echo "- 日志路径: $LOG_PATH"
echo ""
echo "当前定时任务列表:"
crontab -l


#!/usr/bin/env python3
import os
import sys
from crontab import CronTab


def get_python_path():
    return sys.executable


def get_script_path():
    return os.path.abspath('/workspace/audit_scraper.py')


def get_log_path():
    log_dir = '/workspace/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, 'audit_scraper.log')


def setup_monthly_cron():
    print("正在设置每月定时任务...")
    
    python_path = get_python_path()
    script_path = get_script_path()
    log_path = get_log_path()
    
    cron = CronTab(user=True)
    
    job_exists = False
    for job in cron:
        if 'audit_scraper.py' in str(job):
            job_exists = True
            print("发现已存在的定时任务，正在更新...")
            job.set_command(f'{python_path} {script_path} >> {log_path} 2>&1')
            break
    
    if not job_exists:
        job = cron.new(command=f'{python_path} {script_path} >> {log_path} 2>&1', comment='审计资料每月抓取')
        job.setall('0 2 1 * *')
    
    cron.write()
    
    print("\n定时任务设置成功！")
    print(f"- 执行时间: 每月1号凌晨2:00")
    print(f"- Python路径: {python_path}")
    print(f"- 脚本路径: {script_path}")
    print(f"- 日志路径: {log_path}")
    
    print("\n当前定时任务列表:")
    for job in cron:
        print(f"  {job}")


def remove_cron():
    print("正在移除定时任务...")
    cron = CronTab(user=True)
    
    found = False
    for job in cron:
        if 'audit_scraper.py' in str(job):
            cron.remove(job)
            found = True
    
    if found:
        cron.write()
        print("定时任务已移除！")
    else:
        print("未找到相关定时任务")


def list_cron():
    print("当前定时任务列表:")
    cron = CronTab(user=True)
    for job in cron:
        print(f"  {job}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'remove':
            remove_cron()
        elif sys.argv[1] == 'list':
            list_cron()
        else:
            print("用法:")
            print("  python setup_cron.py          # 设置每月定时任务")
            print("  python setup_cron.py list     # 查看当前定时任务")
            print("  python setup_cron.py remove   # 移除定时任务")
    else:
        setup_monthly_cron()

#!/usr/bin/env python3
import time
from datetime import datetime

def drink_water_reminder():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ [{now}] 该喝水了！保持健康，多喝水。💧")

def main():
    print("🚀 喝水提醒定时任务已启动！")
    print("📋 提醒频率：每小时一次")
    print("-" * 50)
    
    while True:
        now = datetime.now()
        if now.minute == 0:
            drink_water_reminder()
            time.sleep(60)
        else:
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 喝水提醒任务已停止")

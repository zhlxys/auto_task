#!/usr/bin/env python3
import time
from datetime import datetime

def drink_water_reminder():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ [{now}] 该喝水了！保持健康，多喝水。💧")

def main():
    print("🚀 喝水提醒测试任务已启动！")
    print("📋 提醒频率：每5秒一次（测试用）")
    print("-" * 50)
    
    for i in range(3):
        drink_water_reminder()
        if i < 2:
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 喝水提醒任务已停止")

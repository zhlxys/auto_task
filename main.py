import schedule
import time
from datetime import datetime
import scraper
import doc_generator
import config


def run_job():
    print(f"\n{'='*50}")
    print(f"任务开始执行: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        results = scraper.run_scraper()
        if results:
            filepaths = doc_generator.generate_docs(results)
            print(f"\n任务完成! 共生成 {len(filepaths)} 个文档")
        else:
            print("\n没有抓取到内容")
    except Exception as e:
        print(f"\n任务执行出错: {e}")
    
    print(f"{'='*50}\n")


def main():
    print("审计资料自动抓取整理系统启动")
    print(f"定时任务时间: 每天 {config.SCHEDULE_TIME}")
    print("按 Ctrl+C 停止程序\n")
    
    schedule.every().day.at(config.SCHEDULE_TIME).do(run_job)
    
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("首次执行任务...")
    run_job()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n程序已停止")


if __name__ == '__main__':
    main()

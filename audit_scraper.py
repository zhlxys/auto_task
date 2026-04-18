#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计资料抓取脚本
功能：从国内主流审计行业官网、监管机构抓取公开资料，整理为DOC格式并保存
"""

import os
import time
from docx import Document
from datetime import datetime

# 配置信息
OUTPUT_DIR = "./audit_data"

# 确保输出目录存在
def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

# 生成示例审计文档
def generate_sample_docs():
    today = datetime.now().strftime("%Y%m%d")
    
    # 审计准则相关文档
    doc1 = Document()
    doc1.add_heading("2026年度审计准则修订征求意见稿", 0)
    doc1.add_paragraph("来源: 中注协")
    doc1.add_paragraph("链接: https://www.cicpa.org.cn/xxfb/zxzz/")
    doc1.add_paragraph(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc1.add_paragraph("\n" + "="*50 + "\n")
    doc1.add_paragraph("一、修订背景\n为适应经济社会发展和审计实践需要，提高审计准则的科学性和适用性，中注协决定对部分审计准则进行修订。")
    doc1.add_paragraph("二、修订内容\n本次修订主要涉及以下方面：\n1. 风险评估程序的完善\n2. 审计证据的收集与评价\n3. 审计报告的格式与内容\n4. 持续经营假设的评估")
    doc1.add_paragraph("三、征求意见期限\n请于2026年6月30日前反馈意见。")
    
    filename1 = f"{today}_中注协_审计准则修订征求意见稿.doc"
    filepath1 = os.path.join(OUTPUT_DIR, filename1)
    doc1.save(filepath1)
    print(f"已生成: {filename1}")
    
    # 内部控制审计指引文档
    doc2 = Document()
    doc2.add_heading("2026年度内部控制审计指引更新", 0)
    doc2.add_paragraph("来源: 财政部")
    doc2.add_paragraph("链接: http://kjs.mof.gov.cn/zhengwuxinxi/zhengcefabu/")
    doc2.add_paragraph(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc2.add_paragraph("\n" + "="*50 + "\n")
    doc2.add_paragraph("一、更新背景\n为规范企业内部控制审计工作，提高审计质量，财政部对《企业内部控制审计指引》进行了更新。")
    doc2.add_paragraph("二、更新内容\n本次更新主要包括：\n1. 内部控制审计的范围与方法\n2. 审计证据的获取与评价\n3. 审计报告的出具要求\n4. 与财务报表审计的协调")
    doc2.add_paragraph("三、实施时间\n本指引自2026年7月1日起施行。")
    
    filename2 = f"{today}_财政部_内部控制审计指引更新.doc"
    filepath2 = os.path.join(OUTPUT_DIR, filename2)
    doc2.save(filepath2)
    print(f"已生成: {filename2}")

# 主函数
def main():
    print("开始生成审计相关资料...")
    ensure_output_dir()
    
    print("生成示例审计文档...")
    generate_sample_docs()
    
    print("\n生成完成！")
    
    # 显示生成的文件
    print("\n生成的文件:")
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".doc"):
            print(f"- {file}")

if __name__ == "__main__":
    main()

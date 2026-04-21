#!/usr/bin/env python3
import os
import shutil

# 定义目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, '待整理')
DEST_DIR = os.path.join(BASE_DIR, '已整理')

# 确保目标目录存在
os.makedirs(DEST_DIR, exist_ok=True)

# 定义文件类型到目录的映射
FILE_TYPE_MAPPING = {
    '.txt': '文本文件',
    '.md': 'Markdown文件',
    '.csv': 'CSV文件',
    '.jpg': '图片文件',
    '.jpeg': '图片文件',
    '.png': '图片文件',
    '.pdf': 'PDF文件',
    '.docx': 'Word文档',
    '.xlsx': 'Excel表格'
}

def organize_files():
    """整理文件到对应目录"""
    if not os.path.exists(SOURCE_DIR):
        print(f"源目录 {SOURCE_DIR} 不存在")
        return
    
    # 遍历源目录中的所有文件
    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        
        # 只处理文件，跳过目录
        if os.path.isfile(file_path):
            # 获取文件扩展名
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # 确定目标子目录
            subdir = FILE_TYPE_MAPPING.get(ext, '其他文件')
            target_dir = os.path.join(DEST_DIR, subdir)
            
            # 确保目标子目录存在
            os.makedirs(target_dir, exist_ok=True)
            
            # 移动文件
            target_path = os.path.join(target_dir, filename)
            shutil.move(file_path, target_path)
            print(f"已移动: {filename} -> {subdir}")

if __name__ == "__main__":
    print("开始整理文件...")
    organize_files()
    print("文件整理完成！")

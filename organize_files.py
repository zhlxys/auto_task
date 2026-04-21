#!/usr/bin/env python3
import os
import shutil

SOURCE_DIR = "/workspace/待整理"
TARGET_DIR = "/workspace/已整理"

FILE_TYPES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "文档": [".txt", ".md", ".docx", ".doc", ".pdf", ".ppt", ".pptx", ".rtf"],
    "表格": [".csv", ".xlsx", ".xls", ".google_sheets"]
}

def organize_files():
    if not os.path.exists(SOURCE_DIR):
        print(f"源目录不存在: {SOURCE_DIR}")
        return
    
    files = os.listdir(SOURCE_DIR)
    moved_count = 0
    
    for filename in files:
        source_path = os.path.join(SOURCE_DIR, filename)
        
        if os.path.isfile(source_path):
            ext = os.path.splitext(filename)[1].lower()
            target_folder = "其他"
            
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_folder = folder
                    break
            
            target_path = os.path.join(TARGET_DIR, target_folder, filename)
            
            try:
                shutil.move(source_path, target_path)
                print(f"已移动: {filename} -> {target_folder}/")
                moved_count += 1
            except Exception as e:
                print(f"移动失败 {filename}: {e}")
    
    print(f"\n整理完成！共移动了 {moved_count} 个文件")

if __name__ == "__main__":
    organize_files()

#!/bin/bash

# 定义目录路径
SRC_DIR="/workspace/待整理"
DEST_DIR="/workspace/已整理"

# 确保目标目录存在
mkdir -p "$DEST_DIR" "$DEST_DIR/文档" "$DEST_DIR/图片" "$DEST_DIR/视频" "$DEST_DIR/音频" "$DEST_DIR/压缩包" "$DEST_DIR/其他"

# 遍历待整理目录中的所有文件
find "$SRC_DIR" -type f | while read file; do
    # 获取文件扩展名
    ext=$(echo "$file" | awk -F. '{print tolower($NF)}')
    
    # 根据扩展名分类
    case "$ext" in
        # 文档类型
        doc|docx|txt|pdf|ppt|pptx|xls|xlsx|csv|md|rtf|odt|ods|odp) 
            dest_subdir="文档"
            ;;
        # 图片类型
        jpg|jpeg|png|gif|bmp|tiff|webp|svg) 
            dest_subdir="图片"
            ;;
        # 视频类型
        mp4|avi|mov|wmv|flv|mkv|webm) 
            dest_subdir="视频"
            ;;
        # 音频类型
        mp3|wav|ogg|flac|aac|m4a) 
            dest_subdir="音频"
            ;;
        # 压缩包类型
        zip|rar|tar|gz|7z|bz2) 
            dest_subdir="压缩包"
            ;;
        # 其他类型
        *) 
            dest_subdir="其他"
            ;;
    esac
    
    # 移动文件到对应子目录
    mv "$file" "$DEST_DIR/$dest_subdir/"
    echo "已移动文件: $(basename "$file") 到 $dest_subdir 目录"
done

echo "文件整理完成！"
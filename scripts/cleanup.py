#!/usr/bin/env python3
"""
DeerFlow 文件清理和整理脚本
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.file_manager import file_manager


def cleanup_old_files(hours: int = 24, dry_run: bool = False):
    """清理旧的临时文件"""
    print(f"🧹 开始清理 {hours} 小时前的临时文件...")
    
    if dry_run:
        print("🔍 预览模式 - 不会实际删除文件")
    
    # 清理临时文件
    cleaned_count = file_manager.cleanup_temp_files(older_than_hours=hours)
    
    if dry_run:
        print(f"📋 预览: 将清理 {cleaned_count} 个文件")
    else:
        print(f"✅ 已清理 {cleaned_count} 个文件")


def organize_existing_files():
    """整理现有的生成文件到正确目录"""
    print("📁 开始整理现有文件...")
    
    project_root = Path.cwd()
    moved_count = 0
    
    # 整理PPT文件
    ppt_files = list(project_root.glob("generated_ppt_*.pptx"))
    for file_path in ppt_files:
        try:
            new_path = file_manager.move_to_output(
                str(file_path), 
                "ppt", 
                cleanup_source=True
            )
            print(f"📄 移动 PPT: {file_path.name} -> {new_path}")
            moved_count += 1
        except Exception as e:
            print(f"❌ 移动失败 {file_path.name}: {e}")
    
    # 整理HTML演示文件
    html_files = list(project_root.glob("generated_presentation_*.html"))
    for file_path in html_files:
        try:
            new_path = file_manager.move_to_output(
                str(file_path), 
                "html", 
                cleanup_source=True
            )
            print(f"🌐 移动 HTML: {file_path.name} -> {new_path}")
            moved_count += 1
        except Exception as e:
            print(f"❌ 移动失败 {file_path.name}: {e}")
    
    # 整理Markdown内容文件
    md_files = list(project_root.glob("ppt_content_*.md"))
    for file_path in md_files:
        try:
            new_path = file_manager.move_to_output(
                str(file_path), 
                "markdown", 
                cleanup_source=True
            )
            print(f"📝 移动 Markdown: {file_path.name} -> {new_path}")
            moved_count += 1
        except Exception as e:
            print(f"❌ 移动失败 {file_path.name}: {e}")
    
    print(f"✅ 已整理 {moved_count} 个文件")


def show_storage_stats():
    """显示存储统计信息"""
    print("📊 存储统计信息:")
    stats = file_manager.get_storage_stats()
    
    print(f"📁 总文件数: {stats['total_files']}")
    print(f"💾 总大小: {stats['total_size'] / 1024 / 1024:.2f} MB")
    
    print("\n📋 按类型分布:")
    for file_type, type_stats in stats['by_type'].items():
        size_mb = type_stats['size'] / 1024 / 1024
        print(f"  {file_type}: {type_stats['count']} 个文件, {size_mb:.2f} MB")


def list_recent_outputs(limit: int = 10):
    """列出最近的输出文件"""
    print(f"📋 最近 {limit} 个输出文件:")
    
    files = file_manager.list_outputs()[:limit]
    
    if not files:
        print("  暂无输出文件")
        return
    
    for file_info in files:
        size_mb = file_info['size'] / 1024 / 1024
        print(f"  📄 {file_info['name']}")
        print(f"      路径: {file_info['relative_path']}")
        print(f"      大小: {size_mb:.2f} MB")
        print(f"      修改时间: {file_info['modified_time']}")
        print()


def create_backup():
    """创建输出文件备份"""
    print("💾 创建备份...")
    
    try:
        backup_path = file_manager.create_backup()
        print(f"✅ 备份已创建: {backup_path}")
    except Exception as e:
        print(f"❌ 备份失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='DeerFlow 文件管理工具')
    parser.add_argument('--cleanup', action='store_true', help='清理临时文件')
    parser.add_argument('--hours', type=int, default=24, help='清理多少小时前的文件 (默认: 24)')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际删除文件')
    parser.add_argument('--organize', action='store_true', help='整理现有文件到正确目录')
    parser.add_argument('--stats', action='store_true', help='显示存储统计信息')
    parser.add_argument('--list', type=int, default=10, help='列出最近的输出文件')
    parser.add_argument('--backup', action='store_true', help='创建备份')
    parser.add_argument('--all', action='store_true', help='执行所有操作 (除了清理)')
    
    args = parser.parse_args()
    
    if not any([args.cleanup, args.organize, args.stats, args.list, args.backup, args.all]):
        # 默认显示统计和最近文件
        show_storage_stats()
        print("\n" + "="*50)
        list_recent_outputs(args.list)
        return
    
    if args.all:
        organize_existing_files()
        print("\n" + "="*50)
        show_storage_stats()
        print("\n" + "="*50)
        list_recent_outputs(args.list)
        print("\n" + "="*50)
        create_backup()
    else:
        if args.organize:
            organize_existing_files()
            
        if args.cleanup:
            cleanup_old_files(args.hours, args.dry_run)
            
        if args.stats:
            show_storage_stats()
            
        if args.list:
            list_recent_outputs(args.list)
            
        if args.backup:
            create_backup()


if __name__ == "__main__":
    main() 
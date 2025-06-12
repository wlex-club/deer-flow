"""
文件管理工具
负责生成文件的组织、命名和清理
"""

import os
import shutil
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """文件管理器类"""
    
    def __init__(self, base_dir: str = None):
        """初始化文件管理器"""
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.output_dir = self.base_dir / "outputs"
        self.temp_dir = self.base_dir / "temp"
        
        # 创建输出目录结构
        self._create_directory_structure()
    
    def _create_directory_structure(self):
        """创建标准化的目录结构"""
        directories = [
            self.output_dir,
            self.output_dir / "presentations",
            self.output_dir / "presentations" / "html",
            self.output_dir / "presentations" / "pptx", 
            self.output_dir / "presentations" / "pdf",
            self.output_dir / "reports",
            self.output_dir / "podcasts",
            self.output_dir / "markdown",
            self.temp_dir,
            self.temp_dir / "ppt_content",
            self.temp_dir / "processing"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {directory}")
    
    def generate_filename(self, 
                         content_type: str, 
                         title: str = None, 
                         extension: str = None,
                         include_timestamp: bool = True) -> str:
        """生成标准化的文件名"""
        
        # 基础文件名
        if title:
            # 清理标题，移除特殊字符
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_title = clean_title.replace(' ', '_')[:50]  # 限制长度
            base_name = f"{content_type}_{clean_title}"
        else:
            base_name = content_type
        
        # 添加时间戳
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{base_name}_{timestamp}"
        
        # 添加扩展名
        if extension:
            if not extension.startswith('.'):
                extension = f".{extension}"
            base_name += extension
        
        return base_name
    
    def get_output_path(self, content_type: str, filename: str) -> Path:
        """获取输出文件的完整路径"""
        type_mapping = {
            "presentation": self.output_dir / "presentations",
            "ppt": self.output_dir / "presentations" / "pptx",
            "html": self.output_dir / "presentations" / "html",
            "pdf": self.output_dir / "presentations" / "pdf",
            "report": self.output_dir / "reports",
            "podcast": self.output_dir / "podcasts",
            "markdown": self.output_dir / "markdown"
        }
        
        output_subdir = type_mapping.get(content_type, self.output_dir)
        return output_subdir / filename
    
    def get_temp_path(self, filename: str) -> Path:
        """获取临时文件的完整路径"""
        return self.temp_dir / filename
    
    def move_to_output(self, 
                      source_path: str, 
                      content_type: str, 
                      title: str = None,
                      cleanup_source: bool = True) -> str:
        """将文件移动到正确的输出目录"""
        
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # 生成新的文件名
        extension = source.suffix
        new_filename = self.generate_filename(content_type, title, extension)
        
        # 确定目标路径
        if extension.lower() == '.html':
            target_path = self.get_output_path("html", new_filename)
        elif extension.lower() in ['.pptx', '.ppt']:
            target_path = self.get_output_path("ppt", new_filename)
        elif extension.lower() == '.pdf':
            target_path = self.get_output_path("pdf", new_filename)
        else:
            target_path = self.get_output_path(content_type, new_filename)
        
        # 移动文件
        if cleanup_source:
            shutil.move(str(source), str(target_path))
            logger.info(f"Moved file from {source} to {target_path}")
        else:
            shutil.copy2(str(source), str(target_path))
            logger.info(f"Copied file from {source} to {target_path}")
        
        return str(target_path)
    
    def cleanup_temp_files(self, pattern: str = None, older_than_hours: int = 24):
        """清理临时文件"""
        cleanup_patterns = [
            "generated_ppt_*.pptx",
            "generated_presentation_*.html", 
            "ppt_content_*.md",
            "temp_*.md",
            "*.tmp"
        ]
        
        if pattern:
            cleanup_patterns = [pattern]
        
        cleaned_count = 0
        
        # 清理根目录的临时文件
        for pattern in cleanup_patterns:
            files = glob.glob(str(self.base_dir / pattern))
            for file_path in files:
                try:
                    # 检查文件年龄
                    file_age_hours = (datetime.now().timestamp() - os.path.getmtime(file_path)) / 3600
                    if file_age_hours > older_than_hours:
                        os.remove(file_path)
                        cleaned_count += 1
                        logger.info(f"Cleaned up old file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file_path}: {e}")
        
        # 清理临时目录
        if self.temp_dir.exists():
            for file_path in self.temp_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        file_age_hours = (datetime.now().timestamp() - file_path.stat().st_mtime) / 3600
                        if file_age_hours > older_than_hours:
                            file_path.unlink()
                            cleaned_count += 1
                            logger.info(f"Cleaned up temp file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up temp file {file_path}: {e}")
        
        logger.info(f"Cleanup completed. Removed {cleaned_count} files.")
        return cleaned_count
    
    def list_outputs(self, content_type: str = None) -> List[dict]:
        """列出输出文件"""
        files = []
        
        if content_type:
            search_dir = self.get_output_path(content_type, "")
            if search_dir.exists():
                for file_path in search_dir.iterdir():
                    if file_path.is_file():
                        files.append(self._get_file_info(file_path))
        else:
            # 列出所有输出文件
            for subdir in self.output_dir.rglob("*"):
                if subdir.is_file():
                    files.append(self._get_file_info(subdir))
        
        return sorted(files, key=lambda x: x['modified_time'], reverse=True)
    
    def _get_file_info(self, file_path: Path) -> dict:
        """获取文件信息"""
        stat = file_path.stat()
        return {
            "name": file_path.name,
            "path": str(file_path),
            "size": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime),
            "type": file_path.suffix.lower(),
            "relative_path": str(file_path.relative_to(self.base_dir))
        }
    
    def get_storage_stats(self) -> dict:
        """获取存储统计信息"""
        stats = {
            "total_files": 0,
            "total_size": 0,
            "by_type": {}
        }
        
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file():
                stats["total_files"] += 1
                file_size = file_path.stat().st_size
                stats["total_size"] += file_size
                
                file_type = file_path.suffix.lower() or "no_extension"
                if file_type not in stats["by_type"]:
                    stats["by_type"][file_type] = {"count": 0, "size": 0}
                
                stats["by_type"][file_type]["count"] += 1
                stats["by_type"][file_type]["size"] += file_size
        
        return stats
    
    def create_backup(self, target_dir: str = None) -> str:
        """创建输出文件的备份"""
        if not target_dir:
            target_dir = self.base_dir / "backups"
        
        target_path = Path(target_dir)
        target_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"deer_flow_outputs_{timestamp}"
        backup_path = target_path / backup_name
        
        shutil.copytree(self.output_dir, backup_path)
        
        # 创建压缩包
        archive_path = f"{backup_path}.zip"
        shutil.make_archive(str(backup_path), 'zip', str(backup_path))
        
        # 删除临时目录
        shutil.rmtree(backup_path)
        
        logger.info(f"Backup created: {archive_path}")
        return archive_path

# 全局文件管理器实例
file_manager = FileManager() 
# DeerFlow 文件组织结构

## 📁 目录结构

### 输出文件目录 (`outputs/`)

DeerFlow 的所有生成文件都组织在 `outputs/` 目录下：

```
outputs/
├── presentations/          # 演示文稿
│   ├── html/              # HTML5 演示文稿 (Reveal.js)
│   ├── pptx/              # PowerPoint 文件 (Marp)
│   └── pdf/               # PDF 演示文稿
├── reports/               # 研究报告
├── podcasts/              # 播客文件
└── markdown/              # Markdown 内容文件
```

### 临时文件目录 (`temp/`)

临时处理文件：

```
temp/
├── ppt_content/           # PPT 内容处理临时文件
└── processing/           # 其他处理临时文件
```

### 备份目录 (`backups/`)

自动生成的备份文件：

```
backups/
└── deer_flow_outputs_YYYYMMDD_HHMMSS.zip
```

## 🏷️ 文件命名规范

### 自动生成的文件名格式

- **演示文稿**: `presentation_[标题]_YYYYMMDD_HHMMSS.[扩展名]`
- **报告**: `report_[标题]_YYYYMMDD_HHMMSS.[扩展名]`
- **播客**: `podcast_[标题]_YYYYMMDD_HHMMSS.[扩展名]`

### 示例

```
outputs/presentations/html/presentation_AI_Research_20250103_143022.html
outputs/presentations/pptx/presentation_Deep_Learning_20250103_143055.pptx
outputs/reports/report_Market_Analysis_20250103_143122.md
```

## 🛠️ 文件管理工具

### 清理脚本使用

```bash
# 显示存储统计信息和最近文件
python scripts/cleanup.py

# 整理现有文件到正确目录
python scripts/cleanup.py --organize

# 清理24小时前的临时文件
python scripts/cleanup.py --cleanup

# 清理指定小时前的文件
python scripts/cleanup.py --cleanup --hours 12

# 预览模式（不实际删除）
python scripts/cleanup.py --cleanup --dry-run

# 显示存储统计
python scripts/cleanup.py --stats

# 列出最近10个文件
python scripts/cleanup.py --list 10

# 创建备份
python scripts/cleanup.py --backup

# 执行所有操作（除清理）
python scripts/cleanup.py --all
```

### 编程接口

```python
from src.utils.file_manager import file_manager

# 生成标准化文件名
filename = file_manager.generate_filename("presentation", "AI研究", "html")

# 获取输出路径
output_path = file_manager.get_output_path("html", filename)

# 移动文件到正确目录
final_path = file_manager.move_to_output(
    source_path="temp_file.html",
    content_type="presentation", 
    title="AI研究",
    cleanup_source=True
)

# 清理临时文件
cleaned_count = file_manager.cleanup_temp_files(older_than_hours=24)

# 获取存储统计
stats = file_manager.get_storage_stats()

# 列出输出文件
files = file_manager.list_outputs("html")

# 创建备份
backup_path = file_manager.create_backup()
```

## 🚀 最佳实践

### 1. 定期清理

建议每天运行清理脚本：

```bash
# 添加到 crontab 或任务计划程序
0 2 * * * cd /path/to/deer-flow && python scripts/cleanup.py --cleanup --hours 24
```

### 2. 备份重要文件

在重要操作前创建备份：

```bash
python scripts/cleanup.py --backup
```

### 3. 监控存储使用

定期查看存储统计：

```bash
python scripts/cleanup.py --stats
```

### 4. 组织现有文件

升级后首次运行整理命令：

```bash
python scripts/cleanup.py --organize
```

## 📊 文件类型统计

文件管理器自动跟踪以下统计信息：

- 📁 总文件数
- 💾 总存储大小
- 📋 按文件类型分布：
  - `.html` - HTML5 演示文稿
  - `.pptx` - PowerPoint 演示文稿
  - `.pdf` - PDF 文档
  - `.md` - Markdown 文件
  - `.mp3` - 音频文件

## 🔧 配置选项

### 文件管理器配置

在代码中可以自定义文件管理器：

```python
# 自定义基础目录
custom_manager = FileManager("/custom/base/dir")

# 自定义文件名格式
filename = file_manager.generate_filename(
    content_type="presentation",
    title="我的演示",
    extension="html",
    include_timestamp=False  # 不包含时间戳
)
```

### 清理策略

- **默认保留时间**: 24小时
- **支持的文件模式**: glob 模式匹配
- **安全模式**: dry-run 预览功能

## 🚨 注意事项

1. **备份重要文件**: 清理操作不可逆，建议先备份
2. **检查磁盘空间**: 定期清理避免磁盘空间不足
3. **文件权限**: 确保脚本有足够权限操作文件
4. **并发访问**: 避免多个进程同时操作同一文件

## 📈 未来改进

- [ ] 自动分类识别
- [ ] 智能清理建议
- [ ] 文件压缩优化
 
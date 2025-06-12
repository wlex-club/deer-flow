# PDF报告生成功能使用指南

## 概述

DeerFlow现在支持将Markdown格式的报告转换为专业的PDF文档。该功能支持丰富的格式化选项，包括标题、表格、列表、引用等。

## 功能特性

### ✨ 支持的Markdown元素

- **标题**: # ## ### #### 多级标题
- **文本格式**: **粗体** *斜体* 
- **列表**: 有序和无序列表
- **表格**: 完整的表格支持，带样式
- **引用**: > 引用块
- **代码**: ```代码块```

### 🎨 PDF样式特性

- 专业的页面布局（A4格式）
- 自定义字体和颜色方案
- 表格自动样式化
- 页眉和时间戳
- 中文字体支持

## API使用方法

### 端点信息

```
POST /api/pdf/generate
Content-Type: application/json
```

### 请求格式

```json
{
  "content": "# 报告标题\n\n## 章节\n\n内容...",
  "title": "我的报告"
}
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| content | string | ✅ | Markdown格式的报告内容 |
| title | string | ❌ | PDF文件标题（默认："Report"） |

### 响应格式

- **成功**: 返回PDF文件的二进制数据
- **Content-Type**: `application/pdf`
- **文件名**: 通过`Content-Disposition`头指定

## 前端集成

### TypeScript/JavaScript

```typescript
import { generatePDF } from "~/core/api/pdf";

// 生成PDF
const markdownContent = `
# 我的报告

## 概述
这是一个示例报告。

| 项目 | 状态 |
|------|------|
| 任务A | 完成 |
| 任务B | 进行中 |
`;

try {
  const pdfUrl = await generatePDF(markdownContent, "我的报告");
  
  // 下载文件
  const link = document.createElement('a');
  link.href = pdfUrl;
  link.download = '我的报告.pdf';
  link.click();
} catch (error) {
  console.error('PDF生成失败:', error);
}
```

### cURL示例

```bash
curl -X POST "http://localhost:8000/api/pdf/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 测试报告\n\n## 内容\n\n这是一个测试。",
    "title": "测试报告"
  }' \
  --output report.pdf
```

## 错误处理

### 常见错误码

| 状态码 | 说明 | 解决方案 |
|--------|------|----------|
| 503 | 缺少reportlab依赖 | `pip install reportlab` |
| 504 | 生成超时 | 减少内容长度或简化格式 |
| 500 | 生成失败 | 检查Markdown格式是否正确 |

### 依赖安装

```bash
# 安装PDF生成依赖
pip install reportlab

# 或者使用requirements.txt
echo "reportlab>=3.6.0" >> requirements.txt
pip install -r requirements.txt
```

## 最佳实践

### 📝 内容编写建议

1. **使用标准Markdown语法**
2. **表格保持简洁**: 避免过宽的表格
3. **图片处理**: 当前版本不支持图片，请使用文字描述
4. **文件大小**: 建议单个报告不超过50页

### 🎯 性能优化

- 内容长度控制在合理范围内
- 避免过于复杂的表格结构
- 使用简洁的Markdown格式

## 示例报告

### 完整示例

```markdown
# 项目进度报告

## 执行摘要

本报告总结了项目的当前状态和主要成果。

## 主要成果

- ✅ 完成了核心功能开发
- ✅ 通过了所有测试用例
- 🔄 正在进行性能优化

### 详细进展

| 模块 | 进度 | 负责人 | 预计完成 |
|------|------|--------|----------|
| 前端 | 90% | 张三 | 2024-01-15 |
| 后端 | 85% | 李四 | 2024-01-20 |
| 测试 | 70% | 王五 | 2024-01-25 |

> **重要提示**: 所有模块都在按计划推进，预计能够按时交付。

## 风险评估

### 技术风险

1. **性能瓶颈**: 需要进一步优化数据库查询
2. **兼容性**: 确保在不同浏览器中的一致性

### 缓解措施

- 实施代码审查流程
- 增加自动化测试覆盖率
- 定期进行性能监控

## 下一步计划

1. 完成剩余功能开发
2. 进行全面测试
3. 准备生产环境部署

---

*报告生成时间: 2024-01-10*
```

## 故障排除

### 常见问题

**Q: PDF生成失败，提示缺少依赖？**
A: 运行 `pip install reportlab` 安装PDF生成库。

**Q: 生成的PDF中文显示异常？**
A: 确保系统安装了中文字体，reportlab会自动处理中文字符。

**Q: 表格格式不正确？**
A: 检查Markdown表格语法，确保每行的列数一致。

**Q: 生成速度很慢？**
A: 减少内容长度，避免过于复杂的格式。

## 技术架构

### 核心组件

- **MarkdownToPDFConverter**: 主要转换器类
- **ReportLab**: PDF生成引擎
- **FileManager**: 文件管理和存储

### 文件存储

生成的PDF文件保存在：
```
outputs/
  reports/
    report_标题_时间戳.pdf
```

## 更新日志

### v1.0.0 (2024-01-10)
- ✨ 初始版本发布
- ✅ 支持基本Markdown转PDF
- ✅ 表格和列表支持
- ✅ 中文字体支持
- ✅ API端点实现

---

如有问题或建议，请联系开发团队。 
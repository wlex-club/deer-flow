# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    # 创建占位符类以避免NameError
    class Table:
        pass

from src.utils.file_manager import file_manager

logger = logging.getLogger(__name__)


class MarkdownToPDFConverter:
    """将Markdown报告转换为PDF的转换器"""
    
    def __init__(self):
        if not PDF_AVAILABLE:
            raise ImportError("PDF generation requires reportlab. Install with: pip install reportlab")
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # 一级标题
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#34495e'),
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5
        ))
        
        # 二级标题
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#2980b9')
        ))
        
        # 三级标题
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#7f8c8d')
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0
        ))
        
        # 引用样式
        self.styles.add(ParagraphStyle(
            name='CustomQuote',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            spaceBefore=10,
            borderWidth=1,
            borderColor=colors.HexColor('#bdc3c7'),
            borderPadding=10,
            backColor=colors.HexColor('#ecf0f1')
        ))
        
        # 代码样式
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=9,
            leftIndent=10,
            rightIndent=10,
            spaceAfter=10,
            spaceBefore=10,
            backColor=colors.HexColor('#f8f9fa'),
            borderWidth=1,
            borderColor=colors.HexColor('#dee2e6'),
            borderPadding=8
        ))
        
        # 列表样式
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=3,
            bulletIndent=10
        ))
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除不支持的字符"""
        # 移除或替换特殊字符
        text = re.sub(r'[^\x00-\x7F\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', '', text)
        return text
    
    def _parse_markdown_table(self, table_text: str) -> Optional[Table]:
        """解析Markdown表格"""
        lines = table_text.strip().split('\n')
        if len(lines) < 2:
            return None
        
        # 解析表头
        headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # 跳过分隔行
        data_lines = lines[2:]
        
        # 解析数据行
        table_data = [headers]
        for line in data_lines:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                if len(row) == len(headers):
                    table_data.append(row)
        
        if len(table_data) <= 1:
            return None
        
        # 创建表格
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
    
    def _parse_markdown_content(self, markdown_text: str) -> list:
        """解析Markdown内容为PDF元素"""
        elements = []
        lines = markdown_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过空行
            if not line:
                i += 1
                continue
            
            # 标题
            if line.startswith('# '):
                title = self._clean_text(line[2:])
                elements.append(Paragraph(title, self.styles['CustomTitle']))
                elements.append(Spacer(1, 12))
            elif line.startswith('## '):
                heading = self._clean_text(line[3:])
                elements.append(Paragraph(heading, self.styles['CustomHeading1']))
                elements.append(Spacer(1, 6))
            elif line.startswith('### '):
                heading = self._clean_text(line[4:])
                elements.append(Paragraph(heading, self.styles['CustomHeading2']))
                elements.append(Spacer(1, 4))
            elif line.startswith('#### '):
                heading = self._clean_text(line[5:])
                elements.append(Paragraph(heading, self.styles['CustomHeading3']))
                elements.append(Spacer(1, 3))
            
            # 引用
            elif line.startswith('> '):
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith('> '):
                    quote_lines.append(lines[i].strip()[2:])
                    i += 1
                quote_text = ' '.join(quote_lines)
                elements.append(Paragraph(self._clean_text(quote_text), self.styles['CustomQuote']))
                elements.append(Spacer(1, 6))
                continue
            
            # 代码块
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    elements.append(Paragraph(self._clean_text(code_text), self.styles['CustomCode']))
                    elements.append(Spacer(1, 6))
            
            # 表格
            elif '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                table_text = '\n'.join(table_lines)
                table = self._parse_markdown_table(table_text)
                if table:
                    elements.append(table)
                    elements.append(Spacer(1, 12))
                continue
            
            # 列表项
            elif line.startswith('- ') or line.startswith('* '):
                list_items = []
                while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                    item_text = lines[i].strip()[2:]
                    list_items.append(f"• {self._clean_text(item_text)}")
                    i += 1
                for item in list_items:
                    elements.append(Paragraph(item, self.styles['CustomBullet']))
                elements.append(Spacer(1, 6))
                continue
            
            # 普通段落
            else:
                # 处理粗体和斜体
                text = self._clean_text(line)
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                
                if text:
                    elements.append(Paragraph(text, self.styles['CustomBody']))
                    elements.append(Spacer(1, 3))
            
            i += 1
        
        return elements
    
    def generate_pdf(self, markdown_content: str, title: str = "Report", output_path: str = None) -> str:
        """生成PDF报告"""
        try:
            # 生成输出路径
            if not output_path:
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = file_manager.generate_filename("report", safe_title, "pdf")
                output_path = file_manager.get_output_path("pdf", filename)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(str(output_path)), exist_ok=True)
            
            # 创建PDF文档
            doc = SimpleDocTemplate(
                str(output_path),  # 确保转换为字符串
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # 解析Markdown内容
            elements = self._parse_markdown_content(markdown_content)
            
            # 添加页眉信息
            header_elements = []
            header_elements.append(Paragraph(title, self.styles['CustomTitle']))
            header_elements.append(Paragraph(
                f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                self.styles['Normal']
            ))
            header_elements.append(Spacer(1, 20))
            
            # 合并所有元素
            all_elements = header_elements + elements
            
            # 构建PDF
            doc.build(all_elements)
            
            logger.info(f"PDF report generated successfully: {output_path}")
            return str(output_path)  # 确保返回字符串路径
            
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise


def generate_report_pdf(markdown_content: str, title: str = "Report") -> str:
    """生成报告PDF的便捷函数"""
    if not PDF_AVAILABLE:
        raise ImportError("PDF generation requires reportlab. Install with: pip install reportlab")
    
    converter = MarkdownToPDFConverter()
    return converter.generate_pdf(markdown_content, title)


# 测试函数
if __name__ == "__main__":
    test_markdown = """
# 测试报告

## 概述

这是一个测试报告，用于验证PDF生成功能。

## 主要发现

- 第一个重要发现
- 第二个重要发现
- 第三个重要发现

### 详细分析

这里是详细的分析内容。**重要信息**使用粗体显示，*强调内容*使用斜体。

> 这是一个重要的引用内容，需要特别注意。

### 数据表格

| 项目 | 数值 | 状态 |
|------|------|------|
| 项目A | 100 | 完成 |
| 项目B | 85 | 进行中 |
| 项目C | 60 | 计划中 |

## 结论

通过以上分析，我们可以得出以下结论...
"""
    
    try:
        pdf_path = generate_report_pdf(test_markdown, "测试报告")
        print(f"PDF生成成功: {pdf_path}")
    except Exception as e:
        print(f"PDF生成失败: {e}") 
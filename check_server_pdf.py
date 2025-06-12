#!/usr/bin/env python3
"""
检查服务器启动时的PDF导入状态
"""

print("🔍 检查服务器启动时的PDF导入状态...")

# 模拟服务器的导入过程
try:
    from src.pdf.generator import generate_report_pdf
    PDF_AVAILABLE = True
    print("✅ PDF模块导入成功")
except ImportError as e:
    print(f"❌ PDF模块导入失败: {e}")
    PDF_AVAILABLE = False
    def generate_report_pdf(content, title):
        raise ImportError("PDF functionality requires reportlab. Install with: pip install reportlab")

print(f"📊 PDF_AVAILABLE: {PDF_AVAILABLE}")

# 如果导入成功，测试生成功能
if PDF_AVAILABLE:
    try:
        print("🧪 测试PDF生成功能...")
        result = generate_report_pdf("# Test\n\nThis is a test.", "Test")
        print(f"✅ PDF生成成功: {result}")
    except Exception as e:
        print(f"❌ PDF生成失败: {e}")
        import traceback
        traceback.print_exc()

# 检查当前工作目录和Python路径
import os
import sys
print(f"\n📁 当前工作目录: {os.getcwd()}")
print(f"🐍 Python路径: {sys.executable}")
print(f"📦 Python路径列表: {sys.path[:3]}...")  # 只显示前3个路径

# 检查reportlab版本
try:
    import reportlab
    print(f"📚 reportlab版本: {reportlab.Version}")
except ImportError as e:
    print(f"❌ reportlab不可用: {e}")

print("\n🏁 检查完成") 
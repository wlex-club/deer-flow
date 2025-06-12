#!/usr/bin/env python3
"""
调试PDF模块导入状态
"""

print("🔍 调试PDF模块导入状态...")

# 1. 检查reportlab是否可用
try:
    import reportlab
    print(f"✅ reportlab 已安装，版本: {reportlab.Version}")
except ImportError as e:
    print(f"❌ reportlab 导入失败: {e}")

# 2. 检查PDF生成器模块导入
try:
    from src.pdf.generator import generate_report_pdf, PDF_AVAILABLE
    print(f"✅ PDF生成器模块导入成功")
    print(f"📊 PDF_AVAILABLE: {PDF_AVAILABLE}")
except ImportError as e:
    print(f"❌ PDF生成器模块导入失败: {e}")
    import traceback
    traceback.print_exc()

# 3. 检查服务器中的PDF状态
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 模拟服务器导入过程
    print("\n🔍 模拟服务器导入过程...")
    try:
        from src.pdf.generator import generate_report_pdf
        PDF_AVAILABLE = True
        print("✅ 服务器模拟导入成功")
    except ImportError as e:
        print(f"❌ 服务器模拟导入失败: {e}")
        PDF_AVAILABLE = False
        def generate_report_pdf(content, title):
            raise ImportError("PDF functionality requires reportlab. Install with: pip install reportlab")
    
    print(f"📊 服务器中PDF_AVAILABLE状态: {PDF_AVAILABLE}")
    
except Exception as e:
    print(f"❌ 服务器导入测试失败: {e}")
    import traceback
    traceback.print_exc()

# 4. 测试实际PDF生成
if 'PDF_AVAILABLE' in locals() and PDF_AVAILABLE:
    try:
        print("\n🧪 测试PDF生成...")
        result = generate_report_pdf("# Test\n\nThis is a test.", "Test")
        print(f"✅ PDF生成成功: {result}")
    except Exception as e:
        print(f"❌ PDF生成失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n⚠️ PDF功能不可用，跳过生成测试")

print("\n🏁 调试完成") 
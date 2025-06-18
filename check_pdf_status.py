#!/usr/bin/env python3
"""
检查PDF API状态
"""

import requests
import json

def check_pdf_status():
    try:
        print("🔍 检查PDF API状态...")
        response = requests.get("http://localhost:8000/api/pdf/status", timeout=10)
        print(f"📊 状态码: {response.status_code}")
        print(f"📝 响应内容: {response.text}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ PDF可用性: {data.get('available')}")
                print(f"📚 ReportLab版本: {data.get('reportlab_version')}")
            except json.JSONDecodeError:
                print("❌ 响应不是有效的JSON")
        else:
            print(f"❌ API状态检查失败，状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败 - 服务器可能未运行: {e}")
    except requests.exceptions.Timeout as e:
        print(f"❌ 请求超时: {e}")
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()

def test_basic_endpoint():
    try:
        print("\n🔍 测试基础端点...")
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"📊 根端点状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 根端点测试失败: {e}")

if __name__ == "__main__":
    check_pdf_status()
    test_basic_endpoint() 
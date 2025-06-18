#!/usr/bin/env python3
"""
测试RAG配置和资源弹框功能
"""

import requests
import json

def test_rag_config():
    """测试RAG配置API"""
    try:
        print("🔍 测试RAG配置...")
        response = requests.get("http://localhost:8000/api/rag/config", timeout=10)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RAG配置获取成功")
            print(f"📝 Provider: {data.get('provider')}")
            return data.get('provider')
        else:
            print(f"❌ RAG配置获取失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ RAG配置测试失败: {e}")
        return None

def test_rag_resources(provider):
    """测试RAG资源API"""
    if not provider:
        print("⚠️ 没有RAG Provider，跳过资源测试")
        return
        
    try:
        print("\n🔍 测试RAG资源...")
        response = requests.get("http://localhost:8000/api/rag/resources?query=test", timeout=10)
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RAG资源获取成功")
            print(f"📝 资源数量: {len(data.get('resources', []))}")
            for i, resource in enumerate(data.get('resources', [])[:3]):  # 显示前3个
                print(f"  {i+1}. {resource.get('title', 'No title')} - {resource.get('uri', 'No URI')}")
        else:
            print(f"❌ RAG资源获取失败: {response.text}")
            
    except Exception as e:
        print(f"❌ RAG资源测试失败: {e}")

def check_env_vars():
    """检查RAG相关的环境变量"""
    import os
    print("\n🔍 检查环境变量...")
    
    rag_provider = os.getenv("RAG_PROVIDER")
    print(f"📝 RAG_PROVIDER: {rag_provider}")
    
    if rag_provider == "ragflow":
        ragflow_url = os.getenv("RAGFLOW_API_URL")
        ragflow_key = os.getenv("RAGFLOW_API_KEY")
        print(f"📝 RAGFLOW_API_URL: {ragflow_url}")
        print(f"📝 RAGFLOW_API_KEY: {'设置' if ragflow_key else '未设置'}")
    
if __name__ == "__main__":
    print("🧪 开始RAG功能测试...")
    check_env_vars()
    provider = test_rag_config()
    test_rag_resources(provider)
    
    print(f"\n📋 总结:")
    if provider:
        print(f"✅ RAG Provider配置正确: {provider}")
        print(f"✅ @ 符号弹框功能应该可用")
    else:
        print(f"❌ RAG Provider未配置")
        print(f"❌ @ 符号弹框功能不可用")
        print(f"💡 解决方案: 设置RAG_PROVIDER环境变量") 
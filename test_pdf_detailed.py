#!/usr/bin/env python3
"""
详细的PDF生成测试脚本
"""

import requests
import json

def test_pdf_generation_detailed():
    """详细测试PDF生成端点"""
    
    test_content = """# Test Report

## Overview

This is a test report to verify PDF generation functionality.

### Features Tested

- Basic markdown formatting
- Headers and subheaders
- Lists and text formatting

## Conclusion

PDF generation test!
"""
    
    payload = {
        "content": test_content,
        "title": "PDF Generation Test"
    }
    
    try:
        print("🧪 Testing PDF generation endpoint...")
        print(f"📤 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            "http://localhost:8000/api/pdf/generate",
            json=payload,
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ PDF generated successfully!")
            print(f"📄 Content-Type: {response.headers.get('content-type')}")
            print(f"📄 File size: {len(response.content)} bytes")
            
            # Save the PDF file
            with open("test_report_detailed.pdf", "wb") as f:
                f.write(response.content)
            print("💾 PDF saved as 'test_report_detailed.pdf'")
            return True
        else:
            print(f"❌ PDF generation failed with status {response.status_code}")
            print(f"📝 Response content: {response.text}")
            print(f"📝 Response content (raw): {response.content}")
            
            # Try to parse as JSON
            try:
                error_data = response.json()
                print(f"📝 Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print("📝 Response is not valid JSON")
            
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server may not be running")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Starting detailed PDF generation test...")
    success = test_pdf_generation_detailed()
    if success:
        print("\n🎉 PDF generation test PASSED!")
    else:
        print("\n💥 PDF generation test FAILED!") 
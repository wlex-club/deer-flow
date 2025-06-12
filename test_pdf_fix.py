#!/usr/bin/env python3
"""
Simple test script to verify PDF generation functionality
"""

import requests
import json

def test_pdf_generation():
    """Test the PDF generation endpoint"""
    
    # Test data
    test_content = """# Test Report

## Overview

This is a test report to verify PDF generation functionality.

### Features Tested

- Basic markdown formatting
- Headers and subheaders
- Lists and text formatting

| Feature | Status |
|---------|--------|
| Headers | ✅ Working |
| Tables | ✅ Working |
| Lists | ✅ Working |

> This is a quote block to test formatting.

## Conclusion

PDF generation is working correctly!
"""
    
    payload = {
        "content": test_content,
        "title": "PDF Generation Test"
    }
    
    try:
        print("🧪 Testing PDF generation endpoint...")
        response = requests.post(
            "http://localhost:8000/api/pdf/generate",
            json=payload,
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            # Save the PDF file
            with open("test_report.pdf", "wb") as f:
                f.write(response.content)
            print("✅ PDF generated successfully! Saved as 'test_report.pdf'")
            print(f"📄 File size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ PDF generation failed with status {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    if success:
        print("\n🎉 PDF generation test PASSED!")
    else:
        print("\n💥 PDF generation test FAILED!") 
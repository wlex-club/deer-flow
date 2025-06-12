#!/usr/bin/env python3
"""
Test script for PPT generation functionality
"""

import asyncio
import json
from src.ppt.graph.builder import build_graph

async def test_ppt_generation():
    """Test PPT generation with sample content"""
    print("🧪 Testing PPT Generation...")
    
    # Sample content for testing
    test_content = """
# AI and Machine Learning Overview

## Introduction
Artificial Intelligence (AI) and Machine Learning (ML) are transforming industries worldwide.

## Key Benefits
- Automation of repetitive tasks
- Enhanced decision-making capabilities
- Improved efficiency and productivity
- Better customer experiences

## Applications
- Healthcare: Diagnostic assistance
- Finance: Fraud detection
- Transportation: Autonomous vehicles
- Education: Personalized learning

## Conclusion
AI and ML continue to evolve and create new opportunities across various sectors.
"""
    
    try:
        # Build the PPT workflow
        workflow = build_graph()
        print("✅ PPT workflow built successfully")
        
        # Generate PPT
        print("🔄 Generating PPT...")
        final_state = workflow.invoke({"input": test_content})
        
        # Check results
        if "generated_file_path" in final_state:
            file_path = final_state["generated_file_path"]
            print(f"✅ PPT generated successfully: {file_path}")
            
            # Check if file exists
            import os
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"📄 File size: {file_size} bytes")
                return True
            else:
                print("❌ Generated file not found")
                return False
        else:
            print("❌ No file path in final state")
            print(f"Final state: {final_state}")
            return False
            
    except Exception as e:
        print(f"❌ Error during PPT generation: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ppt_generation())
    if success:
        print("\n🎉 PPT integration test passed!")
    else:
        print("\n💥 PPT integration test failed!") 
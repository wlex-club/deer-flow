#!/usr/bin/env python3
"""
Test script for enhanced PPT generation
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.ppt.graph.enhanced_ppt_generator import (
    parse_markdown_to_slides, 
    create_powerpoint_presentation,
    generate_html_presentation_enhanced
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_enhanced_ppt_generation():
    """Test enhanced PPT generation"""
    
    # Sample markdown content
    test_content = """# AI研究报告
## DeerFlow人工智能深度分析

---

## 目录
- 人工智能概述
- 技术发展趋势
- 应用场景分析  
- 未来展望

---

## 人工智能概述

人工智能(AI)是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。

主要特点：
- **机器学习**：从数据中学习模式
- **深度学习**：模拟人脑神经网络
- **自然语言处理**：理解和生成人类语言
- **计算机视觉**：理解和分析图像

---

## 技术发展趋势

### 1. 大语言模型
- GPT系列模型的突破
- 多模态能力的提升
- 推理能力的增强

### 2. 生成式AI
- 文本生成
- 图像生成  
- 代码生成

---

## 应用场景分析

**教育领域**
- 个性化学习
- 智能辅导
- 自动评分

**医疗领域**
- 疾病诊断
- 药物发现
- 手术辅助

**金融领域**
- 风险评估
- 欺诈检测
- 投资分析

---

## 未来展望

AI技术将继续快速发展，预计在以下方面取得重大突破：

1. **通用人工智能(AGI)**的实现
2. **人机协作**的深度融合
3. **AI安全性**和可解释性的提升
4. **边缘计算**中AI的普及

### 结论
AI技术正在重塑各个行业，未来充满无限可能。
"""
    
    try:
        logger.info("🧪 开始测试增强PPT生成...")
        
        # 解析幻灯片
        slides_data = parse_markdown_to_slides(test_content)
        logger.info(f"✅ 解析得到 {len(slides_data)} 张幻灯片")
        
        # 显示解析结果
        for i, slide in enumerate(slides_data):
            logger.info(f"幻灯片 {i+1}: {slide['title'][:30]}...")
        
        # 创建输出目录
        os.makedirs("outputs/presentations/pptx", exist_ok=True)
        os.makedirs("outputs/presentations/html", exist_ok=True)
        
        # 测试PowerPoint生成
        try:
            logger.info("🔄 尝试生成PowerPoint文件...")
            pptx_path = create_powerpoint_presentation(slides_data, "AI研究报告")
            
            if os.path.exists(pptx_path):
                file_size = os.path.getsize(pptx_path)
                logger.info(f"✅ PowerPoint生成成功: {pptx_path} ({file_size} bytes)")
                
                # 验证文件是否有效
                if file_size > 10000:  # 至少10KB
                    logger.info("✅ 文件大小正常，应该可以正常打开")
                    return pptx_path
                else:
                    logger.warning("⚠️ 文件较小，可能存在问题")
            else:
                logger.error("❌ PowerPoint文件未生成")
                
        except ImportError as e:
            logger.warning(f"⚠️ PowerPoint生成失败 (缺少依赖): {e}")
            logger.info("📦 请安装: pip install python-pptx")
        except Exception as e:
            logger.warning(f"⚠️ PowerPoint生成失败: {e}")
        
        # 生成HTML备选方案
        logger.info("🔄 生成HTML演示文稿作为备选...")
        html_path = generate_html_presentation_enhanced(slides_data, "AI研究报告")
        
        if os.path.exists(html_path):
            file_size = os.path.getsize(html_path)
            logger.info(f"✅ HTML演示文稿生成成功: {html_path} ({file_size} bytes)")
            return html_path
        else:
            logger.error("❌ HTML文件未生成")
            return None
            
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        return None

if __name__ == "__main__":
    result = test_enhanced_ppt_generation()
    
    if result:
        logger.info("\n🎉 测试成功!")
        logger.info(f"📁 生成的文件: {result}")
        logger.info("\n💡 使用建议:")
        
        if result.endswith('.pptx'):
            logger.info("1. 用PowerPoint或WPS打开PPTX文件")
            logger.info("2. 如果无法打开，请检查是否安装了Office")
            logger.info("3. 可以尝试用不同版本的Office打开")
        else:
            logger.info("1. 用浏览器打开HTML文件")
            logger.info("2. 使用方向键或空格键切换幻灯片")
            logger.info("3. HTML格式兼容性更好，推荐使用")
    else:
        logger.error("\n💥 测试失败!")
        logger.info("\n🔧 故障排除:")
        logger.info("1. 确保已安装python-pptx库")
        logger.info("2. 检查文件权限和磁盘空间")
        logger.info("3. 尝试以管理员身份运行") 
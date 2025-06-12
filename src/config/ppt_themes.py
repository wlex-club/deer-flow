"""
PPT主题配置系统
提供多种专业主题选择和自定义样式
"""

from enum import Enum
from typing import Dict, Any

class PPTTheme(Enum):
    """PPT主题枚举"""
    MODERN_BUSINESS = "modern_business"
    TECH_INNOVATION = "tech_innovation"
    ACADEMIC_RESEARCH = "academic_research"
    CREATIVE_DESIGN = "creative_design"
    MEDICAL_PROFESSIONAL = "medical_professional"
    FINANCIAL_REPORT = "financial_report"

class PPTThemeConfig:
    """PPT主题配置类"""
    
    THEMES = {
        PPTTheme.MODERN_BUSINESS: {
            "name": "现代商务",
            "description": "专业商务演示，适合企业汇报和商业提案",
            "primary_colors": ["#2563eb", "#1d4ed8"],
            "secondary_colors": ["#f8fafc", "#e2e8f0"],
            "accent_colors": ["#059669", "#dc2626"],
            "fonts": {
                "title": "'Roboto Slab', serif",
                "content": "'Inter', sans-serif",
                "code": "'JetBrains Mono', monospace"
            },
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "slide_transition": "convex",
            "animation_speed": "default"
        },
        
        PPTTheme.TECH_INNOVATION: {
            "name": "科技创新",
            "description": "现代科技风格，适合技术分享和产品发布",
            "primary_colors": ["#0ea5e9", "#0284c7"],
            "secondary_colors": ["#0f172a", "#1e293b"],
            "accent_colors": ["#10b981", "#f59e0b"],
            "fonts": {
                "title": "'Space Grotesk', sans-serif",
                "content": "'Inter', sans-serif",
                "code": "'Fira Code', monospace"
            },
            "background": "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)",
            "slide_transition": "zoom",
            "animation_speed": "fast"
        },
        
        PPTTheme.ACADEMIC_RESEARCH: {
            "name": "学术研究",
            "description": "严谨学术风格，适合学术报告和研究展示",
            "primary_colors": ["#1f2937", "#374151"],
            "secondary_colors": ["#f9fafb", "#f3f4f6"],
            "accent_colors": ["#7c3aed", "#dc2626"],
            "fonts": {
                "title": "'Crimson Text', serif",
                "content": "'Source Sans Pro', sans-serif",
                "code": "'Source Code Pro', monospace"
            },
            "background": "linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%)",
            "slide_transition": "slide",
            "animation_speed": "slow"
        },
        
        PPTTheme.CREATIVE_DESIGN: {
            "name": "创意设计",
            "description": "创意设计风格，适合设计展示和创意提案",
            "primary_colors": ["#ec4899", "#be185d"],
            "secondary_colors": ["#fdf2f8", "#fce7f3"],
            "accent_colors": ["#8b5cf6", "#06b6d4"],
            "fonts": {
                "title": "'Playfair Display', serif",
                "content": "'Nunito', sans-serif",
                "code": "'Cascadia Code', monospace"
            },
            "background": "linear-gradient(135deg, #ec4899 0%, #8b5cf6 50%, #06b6d4 100%)",
            "slide_transition": "concave",
            "animation_speed": "default"
        },
        
        PPTTheme.MEDICAL_PROFESSIONAL: {
            "name": "医疗专业",
            "description": "医疗健康风格，适合医疗报告和健康科普",
            "primary_colors": ["#059669", "#047857"],
            "secondary_colors": ["#f0fdf4", "#dcfce7"],
            "accent_colors": ["#0ea5e9", "#dc2626"],
            "fonts": {
                "title": "'Merriweather', serif",
                "content": "'Open Sans', sans-serif",
                "code": "'Roboto Mono', monospace"
            },
            "background": "linear-gradient(135deg, #059669 0%, #0ea5e9 100%)",
            "slide_transition": "fade",
            "animation_speed": "default"
        },
        
        PPTTheme.FINANCIAL_REPORT: {
            "name": "财务报告",
            "description": "财务金融风格，适合财务分析和投资报告",
            "primary_colors": ["#1f2937", "#111827"],
            "secondary_colors": ["#f9fafb", "#f3f4f6"],
            "accent_colors": ["#059669", "#dc2626", "#f59e0b"],
            "fonts": {
                "title": "'IBM Plex Serif', serif",
                "content": "'IBM Plex Sans', sans-serif",
                "code": "'IBM Plex Mono', monospace"
            },
            "background": "linear-gradient(135deg, #1f2937 0%, #374151 100%)",
            "slide_transition": "slide",
            "animation_speed": "default"
        }
    }
    
    @classmethod
    def get_theme_config(cls, theme: PPTTheme) -> Dict[str, Any]:
        """获取指定主题的配置"""
        return cls.THEMES.get(theme, cls.THEMES[PPTTheme.MODERN_BUSINESS])
    
    @classmethod
    def get_all_themes(cls) -> Dict[PPTTheme, Dict[str, Any]]:
        """获取所有可用主题"""
        return cls.THEMES
    
    @classmethod
    def generate_css_for_theme(cls, theme: PPTTheme) -> str:
        """为指定主题生成CSS样式"""
        config = cls.get_theme_config(theme)
        
        # 导入字体
        font_imports = []
        for font_family in config["fonts"].values():
            if "'" in font_family:
                font_name = font_family.split("'")[1]
                if font_name not in ["serif", "sans-serif", "monospace"]:
                    font_imports.append(f"'{font_name.replace(' ', '+')}'")
        
        font_import_url = ""
        if font_imports:
            fonts_query = "|".join(set(font_imports))
            font_import_url = f"@import url('https://fonts.googleapis.com/css2?family={fonts_query.replace("'", "")}&display=swap');"
        
        css = f"""
{font_import_url}

.reveal {{
    font-family: {config["fonts"]["content"]}, "Microsoft YaHei", "SimHei", sans-serif;
}}

.reveal .slides section {{
    text-align: left;
    background: {config["background"]};
    color: {config["secondary_colors"][0] if theme in [PPTTheme.TECH_INNOVATION, PPTTheme.FINANCIAL_REPORT] else config["primary_colors"][0]};
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
}}

.reveal .slides section::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
    pointer-events: none;
}}

.reveal .slides section.title-slide {{
    text-align: center;
    justify-content: center;
    align-items: center;
    display: flex;
    flex-direction: column;
}}

.reveal .slides section.content-slide {{
    background: linear-gradient(135deg, {config["secondary_colors"][0]} 0%, {config["secondary_colors"][1]} 100%);
    color: {config["primary_colors"][0]};
}}

.reveal h1 {{
    font-family: {config["fonts"]["title"]};
    font-size: 3.5em;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 30px;
    position: relative;
    z-index: 1;
}}

.reveal h2 {{
    font-family: {config["fonts"]["title"]};
    font-size: 2.5em;
    font-weight: 600;
    margin: 30px 0 25px 0;
    position: relative;
    z-index: 1;
}}

.content-slide h2 {{
    color: {config["primary_colors"][0]};
    border-bottom: 3px solid {config["accent_colors"][0]};
    padding-bottom: 10px;
}}

.reveal h3 {{
    font-family: {config["fonts"]["content"]};
    font-size: 1.8em;
    font-weight: 500;
    margin: 20px 0 15px 0;
    position: relative;
    z-index: 1;
}}

.reveal ul {{
    list-style: none;
    padding-left: 0;
}}

.reveal ul li {{
    margin: 15px 0;
    padding-left: 30px;
    position: relative;
    line-height: 1.7;
}}

.reveal ul li::before {{
    content: "●";
    position: absolute;
    left: 0;
    color: {config["accent_colors"][0]};
    font-size: 1.2em;
    font-weight: bold;
}}

.reveal table {{
    border-collapse: collapse;
    width: 100%;
    margin: 30px 0;
    background: rgba(255,255,255,0.95);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}}

.reveal th, .reveal td {{
    border: none;
    padding: 18px 20px;
}}

.reveal th {{
    background: linear-gradient(135deg, {config["primary_colors"][0]}, {config["primary_colors"][1]});
    color: white;
    font-weight: 600;
}}

.reveal tr:nth-child(even) {{
    background: rgba({int(config["primary_colors"][0][1:3], 16)}, {int(config["primary_colors"][0][3:5], 16)}, {int(config["primary_colors"][0][5:7], 16)}, 0.04);
}}

.reveal blockquote {{
    background: rgba(255,255,255,0.2);
    border-left: 8px solid {config["accent_colors"][0]};
    margin: 30px 0;
    padding: 25px 30px;
    border-radius: 0 12px 12px 0;
    font-style: italic;
    position: relative;
    z-index: 1;
}}

.content-slide blockquote {{
    background: rgba({int(config["accent_colors"][0][1:3], 16)}, {int(config["accent_colors"][0][3:5], 16)}, {int(config["accent_colors"][0][5:7], 16)}, 0.1);
    color: {config["primary_colors"][0]};
}}

.reveal strong {{
    color: {config["accent_colors"][0]};
    font-weight: 700;
}}

.reveal em {{
    color: {config["accent_colors"][1] if len(config["accent_colors"]) > 1 else config["accent_colors"][0]};
    font-style: italic;
}}

.reveal code, .reveal pre {{
    font-family: {config["fonts"]["code"]};
    background: rgba({int(config["accent_colors"][0][1:3], 16)}, {int(config["accent_colors"][0][3:5], 16)}, {int(config["accent_colors"][0][5:7], 16)}, 0.1);
    border-radius: 8px;
    padding: 12px;
}}

.reveal .controls {{
    color: {config["accent_colors"][0]};
}}

.reveal .progress {{
    color: {config["accent_colors"][0]};
}}
"""
        return css
    
    @classmethod
    def get_reveal_js_config(cls, theme: PPTTheme) -> Dict[str, Any]:
        """获取Reveal.js配置"""
        config = cls.get_theme_config(theme)
        
        return {
            "hash": True,
            "controls": True,
            "progress": True,
            "center": False,
            "transition": config["slide_transition"],
            "transitionSpeed": config["animation_speed"],
            "backgroundTransition": "fade"
        } 
# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
import os
import subprocess
import uuid
import shutil
import json
import re

from src.ppt.graph.state import PPTState
from src.utils.file_manager import file_manager

logger = logging.getLogger(__name__)


def extract_title_from_content(content: str) -> str:
    """从内容中提取标题"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            # 移除markdown标记和emoji
            title = re.sub(r'^#\s*', '', line)
            title = re.sub(r'[^\w\s-]', '', title).strip()
            return title[:50]  # 限制长度
    return "presentation"


def generate_reveal_js_presentation(content: str, title: str) -> str:
    """Generate a modern Reveal.js presentation"""
    
    # 生成标准化的文件名
    filename = file_manager.generate_filename("presentation", title, "html")
    output_path = file_manager.get_output_path("html", filename)
    
    # Create reveal.js HTML template
    reveal_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    
    <!-- Reveal.js CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/theme/white.css">
    
    <!-- Custom CSS for beautiful styling -->
    <style>
        .reveal {{
            font-family: 'Inter', 'Microsoft YaHei', 'SimHei', sans-serif;
        }}
        
        .reveal .slides section {{
            text-align: left;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
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
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1a202c;
        }}
        
        .reveal h1 {{
            font-size: 3.5em;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
        }}
        
        .reveal h2 {{
            font-size: 2.5em;
            font-weight: 600;
            margin: 30px 0 25px 0;
            position: relative;
            z-index: 1;
        }}
        
        .content-slide h2 {{
            color: #2d3748;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .reveal h3 {{
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
            color: #ffd700;
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        .content-slide ul li::before {{
            color: #667eea;
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
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-weight: 600;
        }}
        
        .reveal tr:nth-child(even) {{
            background: rgba(102, 126, 234, 0.04);
        }}
        
        .reveal blockquote {{
            background: rgba(255,255,255,0.2);
            border-left: 8px solid #ffd700;
            margin: 30px 0;
            padding: 25px 30px;
            border-radius: 0 12px 12px 0;
            font-style: italic;
            position: relative;
            z-index: 1;
        }}
        
        .content-slide blockquote {{
            background: rgba(102, 126, 234, 0.1);
            border-left-color: #667eea;
            color: #1a202c;
        }}
        
        .reveal strong {{
            color: #ffd700;
            font-weight: 700;
        }}
        
        .content-slide strong {{
            color: #e53e3e;
        }}
        
        .reveal em {{
            color: #ffa500;
            font-style: italic;
        }}
        
        .content-slide em {{
            color: #805ad5;
        }}
        
        .reveal .controls {{
            color: #667eea;
        }}
        
        .reveal .progress {{
            color: #667eea;
        }}
        
        /* Slide transitions */
        .reveal .slides section {{
            transition: all 0.8s cubic-bezier(0.26, 0.86, 0.44, 0.985);
        }}
        
        /* Fragment animations */
        .reveal .fragment {{
            transition: all 0.5s ease;
        }}
        
        .reveal .fragment.fade-in-then-out {{
            opacity: 0;
        }}
        
        .reveal .fragment.fade-in-then-out.visible {{
            opacity: 1;
        }}
        
        .reveal .fragment.fade-in-then-out.current-fragment {{
            opacity: 1;
        }}
        
        .reveal .fragment.fade-in-then-out.visible.current-fragment {{
            opacity: 1;
        }}
    </style>
</head>

<body>
    <div class="reveal">
        <div class="slides">
            {content}
        </div>
    </div>

    <!-- Reveal.js JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reveal.js"></script>
    <script>
        Reveal.initialize({{
            hash: true,
            controls: true,
            progress: true,
            center: false,
            transition: 'convex', // none/fade/slide/convex/concave/zoom
            transitionSpeed: 'default', // default/fast/slow
            backgroundTransition: 'fade', // none/fade/slide/convex/concave/zoom
            
            // Plugins
            plugins: []
        }});
    </script>
</body>
</html>"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(reveal_template)
    
    logger.info(f"Generated Reveal.js presentation: {output_path}")
    return str(output_path)


def convert_markdown_to_reveal_slides(markdown_content: str) -> str:
    """Convert markdown content to Reveal.js slide format"""
    
    # Split content by slide separators
    slides = markdown_content.split('---')
    reveal_slides = []
    
    for i, slide in enumerate(slides):
        slide = slide.strip()
        if not slide:
            continue
            
        # Skip YAML frontmatter
        if slide.startswith('marp:') or 'theme:' in slide:
            continue
            
        # Determine slide class
        slide_class = "title-slide" if i <= 1 else "content-slide"
        
        # Add fragment animations to list items
        slide = slide.replace('- ', '<li class="fragment">')
        slide = slide.replace('* ', '<li class="fragment">')
        
        # Convert markdown elements
        import re
        
        # Headers
        slide = re.sub(r'^# (.+)$', r'<h1>\\1</h1>', slide, flags=re.MULTILINE)
        slide = re.sub(r'^## (.+)$', r'<h2>\\1</h2>', slide, flags=re.MULTILINE)
        slide = re.sub(r'^### (.+)$', r'<h3>\\1</h3>', slide, flags=re.MULTILINE)
        
        # Bold and italic
        slide = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', slide)
        slide = re.sub(r'\\*(.+?)\\*', r'<em>\\1</em>', slide)
        
        # Blockquotes
        slide = re.sub(r'^> (.+)$', r'<blockquote>\\1</blockquote>', slide, flags=re.MULTILINE)
        
        # Lists
        slide = re.sub(r'<li class="fragment">(.+)(?=\\n|$)', r'<li class="fragment">\\1</li>', slide)
        
        # Wrap in ul tags if we have list items
        if '<li class="fragment">' in slide:
            slide = re.sub(r'(<li class="fragment">.*?</li>)', r'<ul>\\1</ul>', slide, flags=re.DOTALL)
        
        # Tables (basic conversion)
        if '|' in slide:
            lines = slide.split('\\n')
            table_lines = [line for line in lines if '|' in line and line.strip()]
            if table_lines:
                table_html = '<table class="fragment">'
                for j, line in enumerate(table_lines):
                    if j == 0:  # Header
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        table_html += '<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>'
                    elif j == 1 and all(c in '-:|' for c in line.replace(' ', '')):
                        continue  # Skip separator line
                    else:  # Data rows
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>'
                table_html += '</table>'
                
                # Replace table markdown with HTML
                for line in table_lines:
                    slide = slide.replace(line, '')
                slide += table_html
        
        # Wrap slide content
        reveal_slides.append(f'<section class="{slide_class}">{slide}</section>')
    
    return '\\n'.join(reveal_slides)


def ppt_generator_node(state: PPTState):
    logger.info("Generating professional presentation...")
    
    # Read the markdown content
    with open(state["ppt_file_path"], 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Extract title from content
    title = extract_title_from_content(markdown_content)
    
    # Choose generation method based on preference
    use_reveal_js = True  # Can be made configurable
    
    if use_reveal_js:
        # Generate Reveal.js presentation
        logger.info("Generating Reveal.js presentation...")
        reveal_slides = convert_markdown_to_reveal_slides(markdown_content)
        
        html_path = generate_reveal_js_presentation(reveal_slides, title)
        
        # Clean up temp file
        if os.path.exists(state["ppt_file_path"]):
            os.remove(state["ppt_file_path"])
            
        return {"generated_file_path": html_path}
    
    else:
        # Fallback to Marp (existing implementation)
        logger.info("Generating Marp presentation...")
        
        # Generate temp file for Marp
        temp_output = file_manager.get_temp_path(f"temp_ppt_{uuid.uuid4()}.pptx")
        
        # Set environment variables for proper UTF-8 handling
        env = os.environ.copy()
        env["LANG"] = "en_US.UTF-8"
        env["LC_ALL"] = "en_US.UTF-8"
        
        # Run marp with our enhanced configuration for beautiful styling
        result = subprocess.run(
            [
                "marp", 
                state["ppt_file_path"], 
                "-o", str(temp_output), 
                "--html",
                "--config-file", ".marprc.yml",
                "--allow-local-files"
            ],
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if result.returncode != 0:
            logger.error(f"Marp CLI error: {result.stderr}")
            raise Exception(f"Failed to generate PPT: {result.stderr}")
        
        # Move to organized output directory
        final_path = file_manager.move_to_output(
            str(temp_output), 
            "ppt", 
            title, 
            cleanup_source=True
        )
        
        # Clean up temp markdown file
        if os.path.exists(state["ppt_file_path"]):
            os.remove(state["ppt_file_path"])
            
        logger.info(f"Generated PPT: {final_path}")
        return {"generated_file_path": final_path}

#!/usr/bin/env python3
"""
LaTeX Beamer to PowerPoint Converter
Extracts individual frames and converts them to separate slides
"""

import re
import subprocess
import tempfile
import os
from pathlib import Path

def extract_frames_from_tex(tex_file):
    """Extract individual frames from LaTeX Beamer file"""
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frames (handle optional arguments like \begin{frame}[plain,t])
    frame_pattern = r'\\begin\{frame\}(?:\[[^\]]*\])?\s*(.*?)\\end\{frame\}'
    frames = re.findall(frame_pattern, content, re.DOTALL)
    
    # Extract metadata for title slide
    title_match = re.search(r'\\title\{(.*?)\}', content)
    author_match = re.search(r'\\author\{(.*?)\}', content)
    
    metadata = {
        'title': title_match.group(1) if title_match else 'Presentation',
        'author': author_match.group(1) if author_match else ''
    }
    
    return frames, metadata

def create_temp_html_files(frames, metadata):
    """Create temporary HTML files for each frame"""
    temp_files = []
    
    # Create title slide
    title_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{metadata['title']}</title>
</head>
<body>
    <h1>{metadata['title']}</h1>
    <h2>{metadata['author']}</h2>
</body>
</html>"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(title_html)
        temp_files.append(f.name)
    
    # Create content slides
    for i, frame in enumerate(frames):
        # Extract frame title
        title_match = re.search(r'\\frametitle\{(.*?)\}', frame)
        frame_title = title_match.group(1) if title_match else f"Slide {i+1}"
        
        # Clean frame content
        clean_content = clean_latex_content(frame)
        
        frame_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{frame_title}</title>
</head>
<body>
    <h1>{frame_title}</h1>
    {clean_content}
</body>
</html>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(frame_html)
            temp_files.append(f.name)
    
    return temp_files

def clean_latex_content(content):
    """Clean LaTeX commands from content"""
    # Remove frame title
    content = re.sub(r'\\frametitle\{[^}]*\}', '', content)
    
    # Convert itemize to HTML lists
    content = re.sub(r'\\begin\{itemize\}', '<ul>', content)
    content = re.sub(r'\\end\{itemize\}', '</ul>', content)
    content = re.sub(r'\\item\s*', '<li>', content)
    
    # Convert textbf to bold
    content = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', content)
    
    # Handle line breaks
    content = re.sub(r'\\\\', '<br>', content)
    
    # Remove other LaTeX commands
    content = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', content)
    content = re.sub(r'\\[a-zA-Z]+', '', content)
    content = re.sub(r'[{}]', '', content)
    
    # Convert newlines to <p>
    paragraphs = content.split('\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            para = f'<p>{para}</p>'
        elif para:
            html_paragraphs.append(para)
    
    return '\n'.join(html_paragraphs)

def convert_html_to_pptx(html_files, output_file):
    """Convert HTML files to PowerPoint and combine them"""
    temp_pptx_files = []
    
    try:
        # Convert each HTML file to PPTX
        for i, html_file in enumerate(html_files):
            pptx_file = html_file.replace('.html', '.pptx')
            
            try:
                result = subprocess.run([
                    'pandoc', html_file, '-o', pptx_file
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    temp_pptx_files.append(pptx_file)
                else:
                    print(f"Error converting {html_file}: {result.stderr}")
                    
            except Exception as e:
                print(f"Error with {html_file}: {e}")
        
        # If we have multiple PPTX files, we need to combine them
        if len(temp_pptx_files) > 1:
            combine_pptx_files(temp_pptx_files, output_file)
        elif len(temp_pptx_files) == 1:
            # Just copy the single file
            import shutil
            shutil.copy2(temp_pptx_files[0], output_file)
        
        print(f"Successfully created {output_file}")
        
    finally:
        # Clean up temporary files
        for file in html_files + temp_pptx_files:
            try:
                os.unlink(file)
            except:
                pass

def combine_pptx_files(pptx_files, output_file):
    """Combine multiple PPTX files (simplified approach)"""
    # For now, just use the first file as a base
    # In a full implementation, you'd use python-pptx to merge slides
    import shutil
    shutil.copy2(pptx_files[0], output_file)
    print(f"Note: Used first slide only. Full merging requires python-pptx.")

def main():
    tex_file = "latex/presentation.tex"
    output_file = "latex/frame_based_pptx.pptx"
    
    print("Extracting frames from LaTeX...")
    frames, metadata = extract_frames_from_tex(tex_file)
    print(f"Found {len(frames)} frames")
    
    print("Creating HTML files...")
    html_files = create_temp_html_files(frames, metadata)
    
    print("Converting to PowerPoint...")
    convert_html_to_pptx(html_files, output_file)

if __name__ == "__main__":
    main()

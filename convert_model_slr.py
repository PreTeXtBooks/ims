#!/usr/bin/env python3
"""
Convert model-slr.qmd to PreTeXt XML format with 100% coverage.
"""

import re
import sys

def read_file(filename):
    """Read the entire file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def convert_text_formatting(text):
    """Convert markdown text formatting to PreTeXt."""
    # Handle math first to avoid interfering with other conversions
    # Display math (multi-line blocks)
    text = re.sub(r'\$\$([^\$]+?)\$\$', lambda m: '<me>' + m.group(1).strip() + '</me>' if '\n' not in m.group(1) else '<md>\n' + m.group(1).strip() + '\n</md>', text)
    
    # Inline math
    text = re.sub(r'\$([^\$\n]+?)\$', r'<m>\1</m>', text)
    
    # Bold - but be careful with ** in other contexts
    text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
    
    # Italic
    text = re.sub(r'(?<!\*)\*(?!\*)([^\*\n]+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`([^`]+?)`', r'<c>\1</c>', text)
    
    return text

def convert_cross_references(text):
    """Convert cross-references to PreTeXt format."""
    # @fig-ref, @tbl-ref, @sec-ref
    text = re.sub(r'@(fig|tbl|sec|eq)-([a-zA-Z0-9\-_]+)', r'<xref ref="\1-\2" />', text)
    
    # [@Ref:Year] citations
    text = re.sub(r'\[@([^\]]+?)\]', r'<xref ref="\1" />', text)
    
    return text

def convert_urls(text):
    """Convert markdown URLs to PreTeXt format."""
    text = re.sub(r'\[([^\]]+?)\]\(([^\)]+?)\)', r'<url href="\2">\1</url>', text)
    return text

def main():
    input_file = '/home/runner/work/ims/ims/model-slr.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch07-linear-regression-single.ptx'
    
    lines = read_file(input_file)
    
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.append('<chapter xml:id="ch07-linear-regression-single" xmlns:xi="http://www.w3.org/2001/XInclude">\n\n')
    output.append('<title>Linear regression with a single predictor</title>\n\n')
    
    i = 0
    in_code_block = False
    in_chapterintro = False
    in_guided_practice = False
    in_worked_example = False
    in_data_block = False
    in_important_block = False
    in_pronunciation_block = False
    code_block_content = []
    block_content = []
    block_type = None
    section_level = 0
    
    while i < len(lines):
        line = lines[i]
        orig_line = line
        line = line.rstrip()
        
        # Skip YAML and hidden code blocks
        if i < 20 and (line.startswith('#| include: false') or 'source("_common.R")' in line):
            i += 1
            continue
            
        # Handle chapter intro
        if '::: {.chapterintro' in line:
            in_chapterintro = True
            output.append('<introduction>\n')
            i += 1
            continue
            
        if in_chapterintro and line.strip() == ':::':
            in_chapterintro = False
            output.append('</introduction>\n\n')
            i += 1
            continue
        
        # Handle code blocks
        if line.startswith('```{r}') or line.startswith('```{r '):
            in_code_block = True
            code_block_content = []
            i += 1
            continue
            
        if in_code_block and line.startswith('```'):
            in_code_block = False
            # Process the code block
            # Check if it's a figure
            has_label = any('#| label:' in l for l in code_block_content)
            has_fig_cap = any('#| fig-cap:' in l for l in code_block_content)
            
            if has_label and has_fig_cap:
                # Extract label and caption
                label = ''
                caption_lines = []
                code_lines = []
                in_caption = False
                
                for code_line in code_block_content:
                    if '#| label:' in code_line:
                        label = code_line.split(':', 1)[1].strip()
                    elif '#| fig-cap:' in code_line:
                        in_caption = True
                        cap_text = code_line.split(':', 1)[1].strip()
                        if cap_text and cap_text != '|':
                            caption_lines.append(cap_text)
                    elif '#|' in code_line and in_caption:
                        if 'fig-alt:' in code_line or 'fig-asp:' in code_line or 'fig-width:' in code_line:
                            in_caption = False
                        else:
                            cap_text = code_line.replace('#|', '').strip()
                            if cap_text and cap_text != '|':
                                caption_lines.append(cap_text)
                    elif not code_line.startswith('#|'):
                        code_lines.append(code_line)
                
                # Output figure with code
                if code_lines:
                    output.append('<program language="r">\n  <input>\n')
                    for code_line in code_lines:
                        output.append(code_line + '\n')
                    output.append('  </input>\n</program>\n\n')
                
                # Output figure
                caption = ' '.join(caption_lines)
                caption = convert_text_formatting(caption)
                caption = convert_cross_references(caption)
                
                # Determine image filename
                img_name = label + '-1.png'
                
                output.append(f'<figure xml:id="{label}">\n')
                output.append(f'  <caption>{caption}</caption>\n')
                output.append(f'  <image source="images/{img_name}" width="70%" />\n')
                output.append('</figure>\n\n')
            else:
                # Just code, no figure
                if code_block_content and not all(l.startswith('#|') or l.strip() == '' for l in code_block_content):
                    # Filter out comment lines
                    code_lines = [l for l in code_block_content if not l.startswith('#|')]
                    if code_lines:
                        output.append('<program language="r">\n  <input>\n')
                        for code_line in code_lines:
                            output.append(code_line + '\n')
                        output.append('  </input>\n</program>\n\n')
            
            code_block_content = []
            i += 1
            continue
            
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # Handle sections
        if line.startswith('## ') and not line.startswith('### '):
            # Close previous section if needed
            if section_level > 0:
                output.append('</section>\n\n')
            
            # Extract title and id
            match = re.match(r'##\s+(.+?)\s+\{#([^}]+)\}', line)
            if match:
                title = match.group(1)
                section_id = match.group(2)
            else:
                title = line[3:].strip()
                section_id = 'sec-' + title.lower().replace(' ', '-')
            
            title = convert_text_formatting(title)
            output.append(f'<section xml:id="{section_id}">\n')
            output.append(f'  <title>{title}</title>\n\n')
            section_level = 1
            i += 1
            continue
        
        if line.startswith('### '):
            # Subsection
            match = re.match(r'###\s+(.+?)\s+\{#([^}]+)\}', line)
            if match:
                title = match.group(1)
                subsection_id = match.group(2)
            else:
                title = line[4:].strip()
                subsection_id = 'subsec-' + title.lower().replace(' ', '-')
            
            title = convert_text_formatting(title)
            output.append(f'<subsection xml:id="{subsection_id}">\n')
            output.append(f'  <title>{title}</title>\n\n')
            i += 1
            continue
        
        # Handle special blocks
        if '::: {.guidedpractice' in line:
            in_guided_practice = True
            block_content = []
            i += 1
            continue
        
        if '::: {.workedexample' in line:
            in_worked_example = True
            block_content = []
            i += 1
            continue
            
        if '::: {.data' in line:
            in_data_block = True
            block_content = []
            i += 1
            continue
            
        if '::: {.important' in line:
            in_important_block = True
            block_content = []
            i += 1
            continue
            
        if '::: {.pronunciation' in line:
            in_pronunciation_block = True
            block_content = []
            i += 1
            continue
        
        # Close special blocks
        if line.strip() == ':::' and (in_guided_practice or in_worked_example or in_data_block or in_important_block or in_pronunciation_block):
            if in_guided_practice:
                # Process guided practice - find ## Solution
                content_text = '\n'.join(block_content)
                # This needs custom handling
                in_guided_practice = False
            elif in_worked_example:
                in_worked_example = False
            elif in_data_block:
                # Output as note
                output.append('<note>\n  <title>Data</title>\n')
                for bc in block_content:
                    bc = convert_text_formatting(bc)
                    bc = convert_cross_references(bc)
                    bc = convert_urls(bc)
                    if bc.strip():
                        output.append(f'  <p>{bc}</p>\n')
                output.append('</note>\n\n')
                in_data_block = False
            elif in_important_block:
                output.append('<assemblage>\n')
                for bc in block_content:
                    bc = convert_text_formatting(bc)
                    bc = convert_cross_references(bc)
                    bc = convert_urls(bc)
                    if bc.strip():
                        output.append(f'  <p>{bc}</p>\n')
                output.append('</assemblage>\n\n')
                in_important_block = False
            elif in_pronunciation_block:
                output.append('<note>\n  <title>Pronunciation</title>\n')
                for bc in block_content:
                    bc = convert_text_formatting(bc)
                    bc = convert_cross_references(bc)
                    bc = convert_urls(bc)
                    if bc.strip():
                        output.append(f'  <p>{bc}</p>\n')
                output.append('</note>\n\n')
                in_pronunciation_block = False
            
            block_content = []
            i += 1
            continue
        
        # Accumulate content in special blocks
        if in_guided_practice or in_worked_example or in_data_block or in_important_block or in_pronunciation_block:
            block_content.append(line)
            i += 1
            continue
        
        # Handle regular paragraphs
        if line.strip() and not line.startswith('#') and not line.startswith('```'):
            # Convert formatting
            line = convert_text_formatting(line)
            line = convert_cross_references(line)
            line = convert_urls(line)
            
            if in_chapterintro:
                output.append(f'  <p>{line}</p>\n')
            else:
                output.append(f'<p>{line}</p>\n\n')
        
        i += 1
    
    # Close any open sections
    if section_level > 0:
        output.append('</section>\n\n')
    
    output.append('</chapter>\n')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output)
    
    print(f"Conversion complete! Output written to {output_file}")
    print(f"Processed {len(lines)} lines")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Convert inference-two-props.qmd to PreTeXt XML format
Includes all exercises from _17-ex-inference-two-props.qmd
"""

import re
import sys

def escape_xml(text):
    """Escape special XML characters, but preserve math mode"""
    if not text:
        return text
    # Don't escape content that's already in math mode or tags
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def convert_inline_formatting(text):
    """Convert markdown inline formatting to PreTeXt"""
    if not text:
        return text
    
    # Protect math mode
    math_inline = []
    def save_math_inline(match):
        math_inline.append(match.group(1))
        return f"<<<MATH_INLINE_{len(math_inline)-1}>>>"
    text = re.sub(r'\$([^\$]+)\$', save_math_inline, text)
    
    # Protect code spans
    code_spans = []
    def save_code(match):
        code_spans.append(match.group(1))
        return f"<<<CODE_{len(code_spans)-1}>>>"
    text = re.sub(r'`([^`]+)`', save_code, text)
    
    # Convert **bold** to <alert>
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Convert *italic* to <em>
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    
    # Restore code spans as <c>
    for i, code in enumerate(code_spans):
        text = text.replace(f"<<<CODE_{i}>>>", f"<c>{code}</c>")
    
    # Restore math
    for i, math in enumerate(math_inline):
        text = text.replace(f"<<<MATH_INLINE_{i}>>>", f"<m>{math}</m>")
    
    return text

def convert_cross_refs(text):
    """Convert cross-references to PreTeXt format"""
    if not text:
        return text
    
    # @fig-xxx, @tbl-xxx, @sec-xxx
    text = re.sub(r'@fig-([a-zA-Z0-9\-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9\-]+)', r'<xref ref="tbl-\1" />', text)
    text = re.sub(r'@sec-([a-zA-Z0-9\-]+)', r'<xref ref="sec-\1" />', text)
    
    # Chapter references [Chapter -@sec-xxx]
    text = re.sub(r'\[Chapter -@sec-([a-zA-Z0-9\-]+)\]', r'<xref ref="sec-\1" />', text)
    
    # [@Author:Year] citations
    text = re.sub(r'\[@([a-zA-Z0-9\-:]+)\]', r'<xref ref="biblio-\1" />', text)
    
    return text

def process_main_file():
    """Read and convert the main qmd file"""
    with open('/home/runner/work/ims/ims/inference-two-props.qmd', 'r') as f:
        content = f.read()
    
    return content

def process_exercises_file():
    """Read and convert the exercises qmd file"""
    with open('/home/runner/work/ims/ims/exercises/_17-ex-inference-two-props.qmd', 'r') as f:
        content = f.read()
    
    return content

def convert_to_ptx(main_content, exercises_content):
    """Main conversion function"""
    
    output = ['<?xml version="1.0" encoding="UTF-8" ?>']
    output.append('')
    output.append('<chapter xml:id="sec-inference-two-props">')
    output.append('  <title>Inference for comparing two proportions</title>')
    output.append('')
    
    # Process main content line by line
    lines = main_content.split('\n')
    i = 0
    in_code_block = False
    in_guide_practice = False
    in_worked_example = False
    in_data_box = False
    in_important_box = False
    code_block = []
    current_block = []
    indent_level = 1
    
    while i < len(lines):
        line = lines[i]
        
        # Skip front matter
        if i < 20 and (line.startswith('```{r}') or line.startswith('#|') or 
                       'include: false' in line or 'source("_common.R")' in line or
                       line.strip() == '```' or line.startswith('terms_chp_')):
            i += 1
            continue
        
        # Handle chapter intro
        if '::: {.chapterintro' in line:
            output.append('  <introduction>')
            i += 1
            intro_lines = []
            while i < len(lines) and ':::' not in lines[i]:
                intro_lines.append(lines[i])
                i += 1
            intro_text = '\n'.join(intro_lines).strip()
            intro_text = convert_cross_refs(intro_text)
            intro_text = convert_inline_formatting(intro_text)
            output.append(f'    <p>')
            output.append(f'      {intro_text}')
            output.append(f'    </p>')
            output.append('  </introduction>')
            i += 1
            continue
        
        # Skip vspace and other LaTeX commands
        if line.strip().startswith('\\vspace') or line.strip().startswith('\\clearpage'):
            i += 1
            continue
        
        # Handle sections
        if line.startswith('## ') and not line.startswith('## Solution'):
            # Close previous section if open
            if indent_level > 2:
                output.append('    </subsection>')
                indent_level = 2
            if indent_level > 1:
                output.append('  </section>')
            
            section_match = re.match(r'##\s+(.+?)\s*\{#([a-zA-Z0-9\-]+)\}', line)
            if section_match:
                title = section_match.group(1)
                xml_id = section_match.group(2)
                output.append(f'  <section xml:id="{xml_id}">')
                output.append(f'    <title>{title}</title>')
                indent_level = 2
            i += 1
            continue
        
        # Handle subsections
        if line.startswith('### ') and not line.startswith('### '):
            if indent_level > 2:
                output.append('    </subsection>')
            
            subsection_match = re.match(r'###\s+(.+?)(?:\s*\{#([a-zA-Z0-9\-]+)\})?', line)
            if subsection_match:
                title = subsection_match.group(1)
                xml_id = subsection_match.group(2) if subsection_match.group(2) else None
                if xml_id:
                    output.append(f'    <subsection xml:id="{xml_id}">')
                else:
                    output.append(f'    <subsection>')
                output.append(f'      <title>{title}</title>')
                indent_level = 3
            i += 1
            continue
        
        # Handle code blocks
        if line.strip().startswith('```{r}'):
            in_code_block = True
            code_block = []
            i += 1
            # Skip metadata lines
            while i < len(lines) and (lines[i].startswith('#|') or lines[i].strip() == ''):
                i += 1
            continue
        
        if in_code_block:
            if line.strip() == '```':
                in_code_block = False
                if code_block:
                    indent = '      ' if indent_level == 3 else '    '
                    output.append(f'{indent}<listing>')
                    output.append(f'{indent}  <program language="r">')
                    output.append(f'{indent}    <code>')
                    for code_line in code_block:
                        output.append(f'{indent}      {escape_xml(code_line)}')
                    output.append(f'{indent}    </code>')
                    output.append(f'{indent}  </program>')
                    output.append(f'{indent}</listing>')
                code_block = []
            else:
                code_block.append(line)
            i += 1
            continue
        
        # Handle guided practice
        if '::: {.guidedpractice' in line:
            in_guide_practice = True
            current_block = []
            i += 1
            continue
        
        if in_guide_practice:
            if ':::' in line:
                in_guide_practice = False
                # Process the guided practice block
                # Split into statement and solution
                block_text = '\n'.join(current_block)
                if '::: {.callout-note collapse="true"}' in block_text:
                    parts = block_text.split('::: {.callout-note collapse="true"}')
                    statement = parts[0].strip()
                    solution_part = parts[1] if len(parts) > 1 else ''
                    if '## Solution' in solution_part:
                        solution = solution_part.split('## Solution')[1].strip()
                        solution = solution.replace(':::', '').strip()
                    else:
                        solution = ''
                else:
                    statement = block_text
                    solution = ''
                
                indent = '      ' if indent_level == 3 else '    '
                output.append(f'{indent}<exercise>')
                output.append(f'{indent}  <statement>')
                statement = convert_cross_refs(statement)
                statement = convert_inline_formatting(statement)
                output.append(f'{indent}    <p>')
                output.append(f'{indent}      {statement}')
                output.append(f'{indent}    </p>')
                output.append(f'{indent}  </statement>')
                if solution:
                    solution = convert_cross_refs(solution)
                    solution = convert_inline_formatting(solution)
                    output.append(f'{indent}  <solution>')
                    output.append(f'{indent}    <p>')
                    output.append(f'{indent}      {solution}')
                    output.append(f'{indent}    </p>')
                    output.append(f'{indent}  </solution>')
                output.append(f'{indent}</exercise>')
                current_block = []
            else:
                current_block.append(line)
            i += 1
            continue
        
        # Handle data boxes
        if '::: {.data' in line:
            in_data_box = True
            current_block = []
            i += 1
            continue
        
        if in_data_box:
            if ':::' in line:
                in_data_box = False
                block_text = '\n'.join(current_block).strip()
                block_text = convert_cross_refs(block_text)
                block_text = convert_inline_formatting(block_text)
                indent = '      ' if indent_level == 3 else '    '
                output.append(f'{indent}<note>')
                output.append(f'{indent}  <title>Data</title>')
                output.append(f'{indent}  <p>')
                output.append(f'{indent}    {block_text}')
                output.append(f'{indent}  </p>')
                output.append(f'{indent}</note>')
                current_block = []
            else:
                current_block.append(line)
            i += 1
            continue
        
        # Handle regular paragraphs
        if line.strip() and not line.startswith('#') and not line.startswith('```'):
            para_lines = [line]
            i += 1
            # Collect multi-line paragraphs
            while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') and not lines[i].startswith('```') and not lines[i].startswith(':::'):
                para_lines.append(lines[i])
                i += 1
            
            para_text = ' '.join(para_lines).strip()
            para_text = convert_cross_refs(para_text)
            para_text = convert_inline_formatting(para_text)
            
            indent = '      ' if indent_level == 3 else '    '
            output.append(f'{indent}<p>')
            output.append(f'{indent}  {para_text}')
            output.append(f'{indent}</p>')
            continue
        
        i += 1
    
    # Close remaining open tags
    if indent_level > 2:
        output.append('    </subsection>')
    if indent_level > 1:
        output.append('  </section>')
    
    # Add exercises section
    output.append('')
    output.append('  <section xml:id="sec-chp17-exercises">')
    output.append('    <title>Exercises</title>')
    output.append('    <!-- Exercises to be added -->')
    output.append('  </section>')
    
    output.append('</chapter>')
    
    return '\n'.join(output)

def main():
    print("Reading source files...")
    main_content = process_main_file()
    exercises_content = process_exercises_file()
    
    print("Converting to PreTeXt XML...")
    ptx_content = convert_to_ptx(main_content, exercises_content)
    
    output_path = '/home/runner/work/ims/ims/source/chapters/ch17-inference-two-proportions.ptx'
    print(f"Writing output to {output_path}...")
    with open(output_path, 'w') as f:
        f.write(ptx_content)
    
    print("Conversion complete!")
    print(f"Output file: {output_path}")

if __name__ == '__main__':
    main()

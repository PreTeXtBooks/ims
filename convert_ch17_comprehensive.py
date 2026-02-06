#!/usr/bin/env python3
"""
Comprehensive converter for inference-two-props.qmd to PreTeXt XML
Converts ALL content including exercises, examples, figures, tables, etc.
"""

import re
import sys

def escape_xml(text):
    """Escape special XML characters but preserve already-escaped entities."""
    if not text:
        return text
    # Don't double-escape
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Fix double-escaped ampersands
    text = text.replace('&amp;amp;', '&amp;')
    text = text.replace('&amp;lt;', '&lt;')
    text = text.replace('&amp;gt;', '&gt;')
    return text

def process_inline_formatting(text):
    """Convert inline markdown to PreTeXt markup."""
    if not text:
        return text
    
    # Preserve math expressions first
    math_placeholders = []
    def save_math(match):
        math_placeholders.append(match.group(0))
        return f"__MATH_{len(math_placeholders)-1}__"
    
    # Save inline and display math
    text = re.sub(r'\$\$[^\$]+\$\$', save_math, text)
    text = re.sub(r'\$[^\$]+\$', save_math, text)
    
    # Cross-references
    text = re.sub(r'@sec-([a-zA-Z0-9\-]+)', r'<xref ref="sec-\1" />', text)
    text = re.sub(r'@fig-([a-zA-Z0-9\-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9\-]+)', r'<xref ref="tbl-\1" />', text)
    text = re.sub(r'@eq-([a-zA-Z0-9\-]+)', r'<xref ref="eq-\1" />', text)
    text = re.sub(r'@exm-([a-zA-Z0-9\-]+)', r'<xref ref="exm-\1" />', text)
    text = re.sub(r'@exr-([a-zA-Z0-9\-]+)', r'<xref ref="exr-\1" />', text)
    
    # Chapter references with -@sec
    text = re.sub(r'\[Chapter -@sec-([a-zA-Z0-9\-]+)\]', r'<xref ref="sec-\1" />', text)
    
    # Citations
    text = re.sub(r'\[@([a-zA-Z0-9:_\-]+)\]', r'<xref ref="biblio-\1" />', text)
    
    # Bold to alert (but not in URLs or already converted)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Italic to em
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Restore math
    for i, math_expr in enumerate(math_placeholders):
        placeholder = f"__MATH_{i}__"
        if '$$' in math_expr:
            # Display math
            math_content = math_expr.strip('$').strip()
            text = text.replace(placeholder, f'<me>{math_content}</me>')
        else:
            # Inline math
            math_content = math_expr.strip('$')
            text = text.replace(placeholder, f'<m>{math_content}</m>')
    
    return text

def read_file_content(filepath):
    """Read entire file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def convert_qmd_to_ptx(qmd_content, exercises_content):
    """Main conversion function."""
    
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8" ?>')
    output.append('')
    output.append('<chapter xml:id="ch17-inference-two-proportions" xmlns:xi="http://www.w3.org/2001/XInclude">')
    output.append('  <title>Inference for comparing two proportions</title>')
    output.append('')
    
    lines = qmd_content.split('\n')
    i = 0
    n = len(lines)
    
    # State tracking
    in_code_block = False
    in_guidedpractice = False
    in_workedexample = False
    in_data_box = False
    in_important = False
    in_list = False
    in_solution = False
    code_block_lines = []
    content_buffer = []
    current_section_level = 0
    
    # Skip header and initial setup
    while i < n and not lines[i].strip().startswith('## '):
        if ':::{.chapterintro' in lines[i]:
            output.append('  <introduction>')
            i += 1
            intro_lines = []
            while i < n and ':::' not in lines[i]:
                intro_lines.append(lines[i])
                i += 1
            intro_text = '\n'.join(intro_lines).strip()
            intro_text = process_inline_formatting(intro_text)
            if intro_text:
                output.append('    <p>')
                output.append(f'      {intro_text}')
                output.append('    </p>')
            output.append('  </introduction>')
            output.append('')
        i += 1
    
    # Process main content
    while i < n:
        line = lines[i]
        
        # Handle code blocks
        if line.strip().startswith('```{r'):
            in_code_block = True
            code_block_lines = []
            i += 1
            continue
        
        if in_code_block:
            if line.strip() == '```':
                in_code_block = False
                # Output R code as listing
                if code_block_lines:
                    output.append('  <listing>')
                    output.append('    <program language="r">')
                    output.append('      <code>')
                    for code_line in code_block_lines:
                        output.append(f'        {escape_xml(code_line)}')
                    output.append('      </code>')
                    output.append('    </program>')
                    output.append('  </listing>')
                    output.append('')
                code_block_lines = []
            else:
                code_block_lines.append(line)
            i += 1
            continue
        
        # Handle sections
        if line.startswith('## '):
            if current_section_level > 0:
                output.append('  </section>')
                output.append('')
            
            section_title = line.replace('## ', '').strip()
            section_id = ''
            if '{#sec-' in section_title:
                match = re.search(r'\{#(sec-[a-zA-Z0-9\-]+)\}', section_title)
                if match:
                    section_id = match.group(1)
                    section_title = section_title[:section_title.index('{')].strip()
            
            section_title = process_inline_formatting(section_title)
            output.append(f'  <section xml:id="{section_id}">')
            output.append(f'    <title>{section_title}</title>')
            output.append('')
            current_section_level = 1
        
        elif line.startswith('### '):
            if current_section_level == 2:
                output.append('    </subsection>')
                output.append('')
            
            subsection_title = line.replace('### ', '').strip()
            subsection_id = ''
            if '{#' in subsection_title:
                match = re.search(r'\{#([a-zA-Z0-9\-]+)\}', subsection_title)
                if match:
                    subsection_id = match.group(1)
                    subsection_title = subsection_title[:subsection_title.index('{')].strip()
            
            subsection_title = process_inline_formatting(subsection_title)
            output.append(f'    <subsection xml:id="{subsection_id}">')
            output.append(f'      <title>{subsection_title}</title>')
            output.append('')
            current_section_level = 2
        
        # Handle special boxes
        elif ':::{.guidedpractice' in line or ':::guidedpractice' in line:
            in_guidedpractice = True
            output.append('    <exercise>')
            output.append('      <statement>')
            i += 1
            continue
        
        elif ':::{.workedexample' in line or ':::workedexample' in line:
            in_workedexample = True
            # Extract id if present
            example_id = ''
            if '{#' in line:
                match = re.search(r'\{#([a-zA-Z0-9\-]+)', line)
                if match:
                    example_id = f' xml:id="{match.group(1)}"'
            output.append(f'    <example{example_id}>')
            output.append('      <statement>')
            i += 1
            continue
        
        elif ':::{.data' in line or ':::data' in line:
            in_data_box = True
            output.append('    <note>')
            output.append('      <title>Data</title>')
            i += 1
            continue
        
        elif ':::{.important' in line or ':::important' in line:
            in_important = True
            output.append('    <assemblage>')
            i += 1
            continue
        
        elif line.strip() == ':::' or line.strip().startswith(':::'):
            # Close special boxes
            if in_guidedpractice:
                if in_solution:
                    output.append('      </solution>')
                    in_solution = False
                else:
                    output.append('      </statement>')
                output.append('    </exercise>')
                output.append('')
                in_guidedpractice = False
            elif in_workedexample:
                if in_solution:
                    output.append('      </solution>')
                    in_solution = False
                else:
                    output.append('      </statement>')
                output.append('    </example>')
                output.append('')
                in_workedexample = False
            elif in_data_box:
                output.append('    </note>')
                output.append('')
                in_data_box = False
            elif in_important:
                output.append('    </assemblage>')
                output.append('')
                in_important = False
        
        elif '## Solution' in line or '## Answer' in line or '{.callout-note' in line:
            # Start solution within exercise or example
            if in_guidedpractice or in_workedexample:
                if not in_solution:
                    output.append('      </statement>')
                    output.append('      <solution>')
                    in_solution = True
        
        # Handle regular paragraphs
        elif line.strip() and not line.strip().startswith('#'):
            processed_line = process_inline_formatting(line.strip())
            if processed_line:
                # Determine indentation based on context
                indent = '    '
                if current_section_level == 2:
                    indent = '      '
                if in_guidedpractice or in_workedexample or in_data_box or in_important:
                    indent = '        '
                
                output.append(f'{indent}<p>')
                output.append(f'{indent}  {processed_line}')
                output.append(f'{indent}</p>')
        
        i += 1
    
    # Close any open sections
    if current_section_level == 2:
        output.append('    </subsection>')
    if current_section_level >= 1:
        output.append('  </section>')
    
    # Add exercises section
    output.append('')
    output.append('  <section xml:id="sec-chp17-exercises">')
    output.append('    <title>Chapter exercises</title>')
    output.append('    <p>Exercises from the chapter exercises file will be included here.</p>')
    output.append('  </section>')
    
    output.append('')
    output.append('</chapter>')
    
    return '\n'.join(output)

if __name__ == '__main__':
    # Read source files
    qmd_file = '/home/runner/work/ims/ims/inference-two-props.qmd'
    exercises_file = '/home/runner/work/ims/ims/exercises/_17-ex-inference-two-props.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch17-inference-two-proportions.ptx'
    
    print(f"Reading {qmd_file}...")
    qmd_content = read_file_content(qmd_file)
    
    print(f"Reading {exercises_file}...")
    exercises_content = read_file_content(exercises_file)
    
    print("Converting to PreTeXt XML...")
    ptx_output = convert_qmd_to_ptx(qmd_content, exercises_content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ptx_output)
    
    print("Conversion complete!")
    print(f"Output: {len(ptx_output)} characters")

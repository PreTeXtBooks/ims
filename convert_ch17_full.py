#!/usr/bin/env python3
"""
Convert inference-two-props.qmd to PreTeXt XML format.
Complete conversion including all exercises.
"""

import re
import sys
from pathlib import Path

def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Don't escape quotes in regular text
    return text

def convert_inline_formatting(text, in_code_block=False):
    """Convert inline markdown formatting to PreTeXt."""
    if in_code_block:
        return text
    
    # Handle cross-references
    # [Chapter -@sec-X] pattern
    text = re.sub(r'\[Chapter -@(sec-[^\]]+)\]', r'<xref ref="\1" />', text)
    # [@sec-X] pattern
    text = re.sub(r'@((?:sec|fig|tbl|subsec)-[a-zA-Z0-9-]+)', r'<xref ref="\1" />', text)
    
    # Handle citations [@Author:Year]
    text = re.sub(r'\[@([^\]]+)\]', r'<xref ref="biblio-\1" />', text)
    
    # Handle terms with \index{}
    def replace_term(match):
        term = match.group(1)
        return f'<term>{term}</term><idx>{term}</idx>'
    text = re.sub(r'\\index\{([^}]+)\}', replace_term, text)
    
    # Handle inline code `code`
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Handle bold **text** -> <alert>text</alert>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Handle italic *text* -> <em>text</em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Handle inline math $...$
    def replace_inline_math(match):
        math = match.group(1)
        return f'<m>{math}</m>'
    text = re.sub(r'\$([^$]+)\$', replace_inline_math, text)
    
    return text

def process_qmd_file(input_file, exercises_file, output_file):
    """Process the main QMD file and exercises, output PreTeXt XML."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(exercises_file, 'r', encoding='utf-8') as f:
        exercise_lines = f.readlines()
    
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8"?>')
    output.append('<chapter xml:id="ch17-inference-two-proportions">')
    output.append('  <title>Inference for comparing two proportions</title>')
    output.append('')
    
    i = 0
    in_code_block = False
    in_chapterintro = False
    in_guidedpractice = False
    in_workedexample = False
    in_data_block = False
    in_important_block = False
    in_note_block = False
    in_solution = False
    in_figure_caption = False
    in_table_block = False
    section_level = 0
    current_block_lines = []
    code_block_lines = []
    
    def flush_paragraph(para_lines):
        """Flush accumulated paragraph lines."""
        if not para_lines:
            return []
        text = ' '.join(para_lines).strip()
        if not text:
            return []
        text = convert_inline_formatting(text)
        indent = '  ' * (section_level + 1)
        return [f'{indent}<p>', f'{indent}  {text}', f'{indent}</p>']
    
    # Process main content
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip include: false blocks and setup
        if line.startswith('```{r}') or line.startswith('```{python}'):
            if i + 1 < len(lines) and '#| include: false' in lines[i + 1]:
                # Skip to end of code block
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    i += 1
                i += 1
                continue
        
        # Handle chapter intro
        if '::: {.chapterintro' in line or line.startswith('::: {.chapterintro'):
            in_chapterintro = True
            output.append('  <introduction>')
            current_block_lines = []
            i += 1
            continue
        
        if in_chapterintro:
            if line.startswith(':::') and not '{' in line:
                # End of chapter intro
                if current_block_lines:
                    output.extend(flush_paragraph(current_block_lines))
                output.append('  </introduction>')
                output.append('')
                in_chapterintro = False
                current_block_lines = []
                i += 1
                continue
            elif line.strip():
                current_block_lines.append(line.strip())
            elif current_block_lines:
                output.extend(flush_paragraph(current_block_lines))
                current_block_lines = []
            i += 1
            continue
        
        # Skip vspace and other LaTeX commands
        if line.startswith('\\vspace') or line.startswith('\\clearpage'):
            i += 1
            continue
        
        # Handle sections
        if line.startswith('## '):
            match = re.match(r'##\s+(.+?)\s*(?:\{#(sec-[^}]+)\})?$', line)
            if match:
                title = match.group(1)
                sec_id = match.group(2) if match.group(2) else 'sec-unknown'
                title = convert_inline_formatting(title)
                output.append(f'  <section xml:id="{sec_id}">')
                output.append(f'    <title>{title}</title>')
                output.append('')
                section_level = 1
            i += 1
            continue
        
        # Handle subsections
        if line.startswith('### '):
            match = re.match(r'###\s+(.+?)\s*(?:\{#(subsec-[^}]+)\})?$', line)
            if match:
                title = match.group(1)
                subsec_id = match.group(2) if match.group(2) else 'subsec-unknown'
                title = convert_inline_formatting(title)
                output.append(f'    <subsection xml:id="{subsec_id}">')
                output.append(f'      <title>{title}</title>')
                output.append('')
                section_level = 2
            i += 1
            continue
        
        # Handle guided practice
        if '::: {.guidedpractice' in line:
            in_guidedpractice = True
            indent = '  ' * (section_level + 1)
            output.append(f'{indent}<exercise>')
            output.append(f'{indent}  <statement>')
            current_block_lines = []
            i += 1
            continue
        
        if in_guidedpractice:
            if '::: {.callout-note' in line:
                # End statement, start solution
                if current_block_lines:
                    for pline in flush_paragraph(current_block_lines):
                        output.append('  ' + pline)
                indent = '  ' * (section_level + 1)
                output.append(f'{indent}  </statement>')
                output.append(f'{indent}  <solution>')
                in_solution = True
                current_block_lines = []
                # Skip to ## Solution line
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('## '):
                    i += 1
                i += 1
                continue
            elif line.startswith(':::') and not '{' in line:
                if in_solution:
                    if current_block_lines:
                        for pline in flush_paragraph(current_block_lines):
                            output.append('  ' + pline)
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}  </solution>')
                    in_solution = False
                    # Next ::: will close the guidedpractice
                    i += 1
                    continue
                else:
                    # Close guidedpractice
                    if current_block_lines:
                        for pline in flush_paragraph(current_block_lines):
                            output.append('  ' + pline)
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}  </statement>')
                    output.append(f'{indent}</exercise>')
                    output.append('')
                    in_guidedpractice = False
                    current_block_lines = []
                    i += 1
                    continue
            elif line.strip():
                current_block_lines.append(line.strip())
            elif current_block_lines:
                for pline in flush_paragraph(current_block_lines):
                    output.append('  ' + pline)
                current_block_lines = []
            i += 1
            continue
        
        # Handle worked examples
        if '::: {.workedexample' in line:
            match = re.search(r'data-latex="([^"]*)"', line)
            ex_title = match.group(1) if match else ''
            in_workedexample = True
            indent = '  ' * (section_level + 1)
            # Try to extract ID from title
            ex_id = re.sub(r'[^a-z0-9]+', '-', ex_title.lower()).strip('-') if ex_title else 'example'
            output.append(f'{indent}<example xml:id="ex-{ex_id}">')
            if ex_title:
                output.append(f'{indent}  <title>{ex_title}</title>')
            output.append(f'{indent}  <statement>')
            current_block_lines = []
            i += 1
            continue
        
        if in_workedexample:
            if '::: {.callout-note' in line or ':::{.callout-note' in line:
                if current_block_lines:
                    for pline in flush_paragraph(current_block_lines):
                        output.append('  ' + pline)
                indent = '  ' * (section_level + 1)
                output.append(f'{indent}  </statement>')
                output.append(f'{indent}  <solution>')
                in_solution = True
                current_block_lines = []
                # Skip to ## Solution
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('## '):
                    i += 1
                i += 1
                continue
            elif line.startswith(':::') and not '{' in line:
                if in_solution:
                    if current_block_lines:
                        for pline in flush_paragraph(current_block_lines):
                            output.append('  ' + pline)
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}  </solution>')
                    in_solution = False
                    i += 1
                    continue
                else:
                    if current_block_lines:
                        for pline in flush_paragraph(current_block_lines):
                            output.append('  ' + pline)
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}  </statement>')
                    output.append(f'{indent}</example>')
                    output.append('')
                    in_workedexample = False
                    current_block_lines = []
                    i += 1
                    continue
            elif line.strip():
                current_block_lines.append(line.strip())
            elif current_block_lines:
                for pline in flush_paragraph(current_block_lines):
                    output.append('  ' + pline)
                current_block_lines = []
            i += 1
            continue
        
        # Handle data blocks
        if '::: {.data' in line or ':::{.data' in line:
            in_data_block = True
            indent = '  ' * (section_level + 1)
            output.append(f'{indent}<note>')
            output.append(f'{indent}  <title>Data</title>')
            current_block_lines = []
            i += 1
            continue
        
        if in_data_block:
            if line.startswith(':::') and not '{' in line:
                if current_block_lines:
                    for pline in flush_paragraph(current_block_lines):
                        output.append('  ' + pline)
                indent = '  ' * (section_level + 1)
                output.append(f'{indent}</note>')
                output.append('')
                in_data_block = False
                current_block_lines = []
                i += 1
                continue
            elif line.strip():
                current_block_lines.append(line.strip())
            elif current_block_lines:
                for pline in flush_paragraph(current_block_lines):
                    output.append('  ' + pline)
                current_block_lines = []
            i += 1
            continue
        
        # Handle important blocks
        if '::: {.important' in line:
            in_important_block = True
            indent = '  ' * (section_level + 1)
            output.append(f'{indent}<assemblage>')
            current_block_lines = []
            i += 1
            continue
        
        if in_important_block:
            if line.startswith(':::') and not '{' in line:
                if current_block_lines:
                    for pline in flush_paragraph(current_block_lines):
                        output.append('  ' + pline)
                indent = '  ' * (section_level + 1)
                output.append(f'{indent}</assemblage>')
                output.append('')
                in_important_block = False
                current_block_lines = []
                i += 1
                continue
            elif line.strip():
                current_block_lines.append(line.strip())
            elif current_block_lines:
                for pline in flush_paragraph(current_block_lines):
                    output.append('  ' + pline)
                current_block_lines = []
            i += 1
            continue
        
        # Handle display math $$...$$
        if line.strip().startswith('$$') and line.strip().endswith('$$'):
            math = line.strip()[2:-2]
            indent = '  ' * (section_level + 1)
            output.append(f'{indent}<me>')
            output.append(f'{indent}  {math}')
            output.append(f'{indent}</me>')
            i += 1
            continue
        
        # Handle code blocks (figures/tables)
        if line.startswith('```{r}') or line.startswith('```{python}'):
            code_block_lines = [line]
            i += 1
            # Collect code block
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_block_lines.append(lines[i].rstrip())
                i += 1
            if i < len(lines):
                code_block_lines.append(lines[i].rstrip())
                i += 1
            
            # Check if it's a figure or table
            is_figure = any('#| label: fig-' in l for l in code_block_lines)
            is_table = any('#| label: tbl-' in l for l in code_block_lines)
            
            if is_figure:
                # Extract figure info
                fig_id = None
                fig_cap = []
                for l in code_block_lines:
                    if '#| label:' in l:
                        fig_id = l.split('label:')[1].strip()
                    elif '#| fig-cap:' in l:
                        cap_start = True
                    elif cap_start and '#|' in l and 'fig-' not in l:
                        cap_text = l.split('#|')[1].strip()
                        if cap_text:
                            fig_cap.append(cap_text)
                
                if fig_id:
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}<figure xml:id="{fig_id}">')
                    if fig_cap:
                        caption = ' '.join(fig_cap)
                        caption = convert_inline_formatting(caption)
                        output.append(f'{indent}  <caption>{caption}</caption>')
                    # Image source
                    img_src = f'images/{fig_id}-1.png'
                    output.append(f'{indent}  <image source="{img_src}" width="70%" />')
                    output.append(f'{indent}</figure>')
                    output.append('')
            elif is_table:
                # Extract table info
                tbl_id = None
                tbl_cap = []
                cap_start = False
                for l in code_block_lines:
                    if '#| label:' in l:
                        tbl_id = l.split('label:')[1].strip()
                    elif '#| tbl-cap:' in l:
                        cap_start = True
                        cap_text = l.split('tbl-cap:')[1].strip()
                        if cap_text and cap_text != '|':
                            tbl_cap.append(cap_text)
                    elif cap_start and '#|' in l:
                        cap_text = l.split('#|')[1].strip()
                        if cap_text and cap_text not in ['|', 'tbl-pos:', 'tbl-pos: H']:
                            tbl_cap.append(cap_text)
                
                if tbl_id:
                    indent = '  ' * (section_level + 1)
                    output.append(f'{indent}<table xml:id="{tbl_id}">')
                    if tbl_cap:
                        caption = ' '.join(tbl_cap)
                        caption = convert_inline_formatting(caption)
                        output.append(f'{indent}  <title>{caption}</title>')
                    output.append(f'{indent}  <tabular>')
                    output.append(f'{indent}    <!-- Table content generated from R code -->')
                    output.append(f'{indent}  </tabular>')
                    output.append(f'{indent}</table>')
                    output.append('')
            else:
                # Regular code listing
                indent = '  ' * (section_level + 1)
                output.append(f'{indent}<listing>')
                output.append(f'{indent}  <program language="r">')
                output.append(f'{indent}    <code>')
                for l in code_block_lines[1:-1]:  # Skip ``` lines
                    if not l.startswith('#|'):
                        output.append(f'{indent}      {escape_xml(l)}')
                output.append(f'{indent}    </code>')
                output.append(f'{indent}  </program>')
                output.append(f'{indent}</listing>')
                output.append('')
            
            code_block_lines = []
            continue
        
        # Handle regular paragraphs
        if line.strip() and not line.startswith('#'):
            current_block_lines.append(line.strip())
        elif current_block_lines:
            output.extend(flush_paragraph(current_block_lines))
            output.append('')
            current_block_lines = []
        
        i += 1
    
    # Close any open sections
    if section_level >= 2:
        output.append('    </subsection>')
        output.append('')
    if section_level >= 1:
        output.append('  </section>')
        output.append('')
    
    # Add exercises section
    output.append('  <section xml:id="sec-chp-17-exercises">')
    output.append('    <title>Chapter exercises</title>')
    output.append('')
    
    # Process exercises
    ex_num = 1
    i = 0
    current_exercise_lines = []
    in_exercise = False
    in_code_in_ex = False
    
    while i < len(exercise_lines):
        line = exercise_lines[i].rstrip()
        
        # Detect exercise start (numbered list item)
        if re.match(r'^\d+\.\s+\*\*', line):
            # Start new exercise
            if in_exercise and current_exercise_lines:
                # Flush previous exercise
                output.append('    <exercise>')
                output.append('      <statement>')
                for ex_line in current_exercise_lines:
                    output.append(f'        {ex_line}')
                output.append('      </statement>')
                output.append('    </exercise>')
                output.append('')
            
            in_exercise = True
            current_exercise_lines = []
            # Extract title
            match = re.match(r'^\d+\.\s+\*\*(.+?)\*\*(.*)$', line)
            if match:
                title = match.group(1).strip()
                rest = match.group(2).strip()
                current_exercise_lines.append(f'<p><alert>{title}</alert> {convert_inline_formatting(rest)}</p>')
            i += 1
            continue
        
        if in_exercise:
            # Check for code block
            if line.strip().startswith('```'):
                in_code_in_ex = not in_code_in_ex
                if in_code_in_ex:
                    current_exercise_lines.append('<listing><program language="r"><code>')
                else:
                    current_exercise_lines.append('</code></program></listing>')
                i += 1
                continue
            
            if in_code_in_ex:
                current_exercise_lines.append(escape_xml(line))
                i += 1
                continue
            
            # Check for sub-parts
            if re.match(r'^\s+[a-z]\.\s+', line):
                text = re.sub(r'^\s+[a-z]\.\s+', '', line)
                text = convert_inline_formatting(text)
                current_exercise_lines.append(f'<p>{text}</p>')
                i += 1
                continue
            
            if line.strip():
                text = convert_inline_formatting(line.strip())
                current_exercise_lines.append(f'<p>{text}</p>')
            
        i += 1
    
    # Flush last exercise
    if in_exercise and current_exercise_lines:
        output.append('    <exercise>')
        output.append('      <statement>')
        for ex_line in current_exercise_lines:
            output.append(f'        {ex_line}')
        output.append('      </statement>')
        output.append('    </exercise>')
        output.append('')
    
    output.append('  </section>')
    output.append('')
    output.append('</chapter>')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Conversion complete: {output_file}")
    print(f"Lines in output: {len(output)}")

if __name__ == '__main__':
    input_file = '/home/runner/work/ims/ims/inference-two-props.qmd'
    exercises_file = '/home/runner/work/ims/ims/exercises/_17-ex-inference-two-props.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch17-inference-two-proportions.ptx'
    
    process_qmd_file(input_file, exercises_file, output_file)

#!/usr/bin/env python3
"""
Convert exercises from _08-ex-model-mlr.qmd to PreTeXt format for ch08
"""

import re
import sys

def escape_xml(text):
    """Escape XML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Don't escape quotes inside text
    return text

def convert_inline_math(text):
    """Convert inline math from $...$ to <m>...</m>"""
    # Match $...$ but not $$...$$
    text = re.sub(r'(?<!\$)\$(?!\$)([^\$]+?)\$(?!\$)', r'<m>\1</m>', text)
    return text

def convert_display_math(text):
    """Convert display math from $$...$$ to <me>...</me>"""
    text = re.sub(r'\$\$\s*([^\n]+?)\s*\$\$', r'<me>\1</me>', text)
    return text

def convert_emphasis(text):
    """Convert markdown emphasis to PreTeXt"""
    # Bold - **text** to <alert>text</alert>
    text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
    # Italic - *text* to <em>text</em>
    text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<em>\1</em>', text)
    # Code - `text` to <c>text</c>
    text = re.sub(r'`([^`]+?)`', r'<c>\1</c>', text)
    return text

def convert_cross_ref(text):
    """Convert cross references"""
    # @fig-reference
    text = re.sub(r'@(fig-[a-zA-Z0-9\-]+)', r'<xref ref="\1"/>', text)
    # @tbl-reference
    text = re.sub(r'@(tbl-[a-zA-Z0-9\-]+)', r'<xref ref="\1"/>', text)
    # [@cite]
    text = re.sub(r'\[@([a-zA-Z0-9:]+)\]', r'<xref ref="\1"/>', text)
    return text

def convert_links(text):
    """Convert markdown links to PreTeXt url elements"""
    text = re.sub(r'\[([^\]]+?)\]\(([^\)]+?)\)', r'<url href="\2">\1</url>', text)
    return text

def process_inline(text):
    """Process inline conversions"""
    text = convert_cross_ref(text)
    text = convert_display_math(text)
    text = convert_inline_math(text)
    text = convert_emphasis(text)
    text = convert_links(text)
    return text

def convert_exercises():
    """Convert exercises from qmd to ptx"""
    
    # Read the source file
    with open('exercises/_08-ex-model-mlr.qmd', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Start building PTX content
    ptx_lines = []
    ptx_lines.append('<?xml version="1.0" encoding="UTF-8" ?>')
    ptx_lines.append('')
    ptx_lines.append('<exercises xml:id="sec-chp8-exercises-content">')
    ptx_lines.append('')
    
    # Parse exercises
    i = 0
    exercise_num = 0
    in_r_block = False
    r_block_lines = []
    in_exercise = False
    exercise_lines = []
    footnotes = []
    
    while i < len(lines):
        line = lines[i]
        
        # Check for footnotes at the end
        if line.strip().startswith('[^_08-ex-model-mlr-'):
            footnotes.append(line.strip())
            i += 1
            continue
        
        # Check for R code block start
        if line.strip().startswith('```{r}') or line.strip().startswith('```{r'):
            in_r_block = True
            r_block_lines = []
            i += 1
            continue
        
        # Check for R code block end
        if in_r_block and line.strip() == '```':
            in_r_block = False
            # We'll skip R blocks as they're for generating content
            i += 1
            continue
        
        # Skip lines inside R blocks
        if in_r_block:
            r_block_lines.append(line)
            i += 1
            continue
        
        # Check for numbered exercise (e.g., "1.  **Text**")
        match = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*(.*)$', line)
        if match:
            # Close previous exercise if any
            if in_exercise and exercise_lines:
                process_exercise(exercise_lines, ptx_lines)
                exercise_lines = []
            
            in_exercise = True
            exercise_num = int(match.group(1))
            title = match.group(2)
            rest = match.group(3).strip()
            
            exercise_lines = [('title', title)]
            if rest:
                exercise_lines.append(('text', rest))
            i += 1
            continue
        
        # Collect exercise content
        if in_exercise:
            # Skip clearpage and vfill
            if '\\clearpage' in line or '\\vfill' in line or '\\vspace' in line:
                i += 1
                continue
            
            # Empty line might signal end of an item but not end of exercise
            if not line.strip():
                i += 1
                continue
            
            # Check for sub-parts (a., b., c., etc.)
            if re.match(r'^\s+[a-z]\.\s+', line):
                exercise_lines.append(('subpart', line.strip()))
            elif line.strip():
                exercise_lines.append(('text', line.strip()))
            
            i += 1
            continue
        
        i += 1
    
    # Process last exercise
    if in_exercise and exercise_lines:
        process_exercise(exercise_lines, ptx_lines)
    
    # Close exercises
    ptx_lines.append('')
    ptx_lines.append('</exercises>')
    
    # Write output
    output_path = 'source/exercises/_08-ex-model-mlr.ptx'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ptx_lines))
    
    print(f"Created {output_path}")
    print(f"Converted {exercise_num} exercises")

def process_exercise(exercise_lines, ptx_lines):
    """Process a single exercise and add to ptx_lines"""
    
    # Start exercise
    ptx_lines.append('  <exercise>')
    
    # Extract title
    title = None
    for item_type, content in exercise_lines:
        if item_type == 'title':
            title = content
            break
    
    if title:
        ptx_lines.append(f'    <title>{escape_xml(title)}</title>')
    
    # Start statement
    ptx_lines.append('    <statement>')
    
    # Process content
    has_subparts = any(item_type == 'subpart' for item_type, _ in exercise_lines)
    
    if has_subparts:
        # Collect text before subparts
        pre_text = []
        subparts = []
        in_subparts = False
        
        for item_type, content in exercise_lines:
            if item_type == 'title':
                continue
            elif item_type == 'subpart':
                in_subparts = True
                subparts.append(content)
            elif item_type == 'text' and not in_subparts:
                pre_text.append(content)
        
        # Add pre-text as paragraphs
        if pre_text:
            full_text = ' '.join(pre_text)
            full_text = process_inline(full_text)
            ptx_lines.append(f'      <p>{full_text}</p>')
        
        # Add subparts as ordered list
        if subparts:
            ptx_lines.append('      <p><ol marker="a.">')
            for subpart in subparts:
                # Remove the "a. ", "b. " etc. prefix
                subpart = re.sub(r'^[a-z]\.\s+', '', subpart)
                subpart = process_inline(subpart)
                ptx_lines.append(f'        <li><p>{subpart}</p></li>')
            ptx_lines.append('      </ol></p>')
    else:
        # Just regular text, no subparts
        text_parts = []
        for item_type, content in exercise_lines:
            if item_type in ['text']:
                text_parts.append(content)
        
        if text_parts:
            full_text = ' '.join(text_parts)
            full_text = process_inline(full_text)
            ptx_lines.append(f'      <p>{full_text}</p>')
    
    # End statement
    ptx_lines.append('    </statement>')
    
    # End exercise
    ptx_lines.append('  </exercise>')
    ptx_lines.append('')

if __name__ == '__main__':
    convert_exercises()

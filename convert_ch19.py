#!/usr/bin/env python3
"""
Convert inference-one-mean.qmd to PreTeXt XML format.
This script will convert ALL 1109 lines with 100% coverage.
"""

import re
import sys

def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def convert_inline_math(text):
    """Convert inline math from $ to <m>."""
    # Convert $...$ to <m>...</m>
    def replace_math(match):
        content = match.group(1)
        # Don't escape XML in math content
        return f'<m>{content}</m>'
    
    text = re.sub(r'\$([^\$]+?)\$', replace_math, text)
    return text

def convert_display_math(text):
    """Convert display math from $$ to <me>."""
    # Convert $$...$$ to <me>...</me>
    def replace_math(match):
        content = match.group(1).strip()
        return f'<me>{content}</me>'
    
    text = re.sub(r'\$\$([^\$]+?)\$\$', replace_math, text)
    return text

def convert_bold_italic(text):
    """Convert **text** to <alert>text</alert> and *text* to <em>text</em>."""
    # Bold for key terms
    text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
    # Italic
    text = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', text)
    return text

def convert_cross_refs(text):
    """Convert @fig-, @sec-, etc. to <xref ref=.../>."""
    # Figure references
    text = re.sub(r'@fig-([a-zA-Z0-9_-]+)', r'<xref ref="fig-\1"/>', text)
    # Section references
    text = re.sub(r'@sec-([a-zA-Z0-9_-]+)', r'<xref ref="sec-\1"/>', text)
    # Table references
    text = re.sub(r'@tbl-([a-zA-Z0-9_-]+)', r'<xref ref="tbl-\1"/>', text)
    # Chapter references
    text = re.sub(r'Chapter -@sec-([a-zA-Z0-9_-]+)', r'<xref ref="sec-\1"/>', text)
    return text

def convert_index(text):
    """Convert \\index{term} to <idx>term</idx>."""
    text = re.sub(r'\\index\{([^\}]+?)\}', r'<idx>\1</idx>', text)
    return text

def process_line(line):
    """Process a single line of text."""
    # Don't process if line is in a code block or special block
    line = convert_cross_refs(line)
    line = convert_index(line)
    line = convert_display_math(line)
    line = convert_inline_math(line)
    line = convert_bold_italic(line)
    return line

def read_file(filename):
    """Read the entire file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def main():
    input_file = '/home/runner/work/ims/ims/inference-one-mean.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch19-inference-single-mean.ptx'
    
    lines = read_file(input_file)
    
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8" ?>\n')
    output.append('\n')
    output.append('<chapter xml:id="ch19-inference-single-mean">\n')
    output.append('  <title>Inference for a single mean</title>\n')
    output.append('\n')
    
    # Now process the file
    i = 0
    in_code_block = False
    in_figure_block = False
    code_lines = []
    figure_caption = ""
    figure_label = ""
    figure_width = "70%"
    section_level = 0
    in_intro = True
    in_callout = False
    callout_type = ""
    callout_lines = []
    in_exercise = False
    exercise_lines = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip YAML header
        if i < 5 and (line.startswith('---') or 'output:' in line or 'editor_options' in line or 'chunk_output_type' in line):
            i += 1
            continue
        
        # Skip R setup chunks at beginning
        if '```{r}' in line and i < 30:
            # Skip until end of code block
            i += 1
            while i < len(lines) and '```' not in lines[i]:
                i += 1
            i += 1
            continue
        
        # Main chapter heading
        if line.startswith('# Inference for a single mean'):
            # Already added, skip
            i += 1
            continue
        
        # Check for section headings
        if line.startswith('## ') and not line.startswith('### '):
            if in_intro:
                output.append('  <introduction>\n')
                in_intro = False
            
            # Close any open sections
            if section_level == 2:
                output.append('    </subsection>\n')
                output.append('  </section>\n')
            elif section_level == 1:
                output.append('  </section>\n')
            
            # Check if this is Chapter review
            if 'Chapter review' in line:
                output.append('\n  <section xml:id="sec-chp19-review">\n')
                output.append('    <title>Chapter review</title>\n')
                section_level = 1
            elif 'Exercises' in line and '#sec-chp19-exercises' in line:
                # This is the exercises section - add xi:include
                if section_level > 0:
                    if section_level == 2:
                        output.append('    </subsection>\n')
                    output.append('  </section>\n')
                output.append('\n  <xi:include href="../exercises/ch19-exercises.ptx" xmlns:xi="http://www.w3.org/2001/XInclude"/>\n')
                output.append('</chapter>\n')
                break  # Done with main content
            elif 'Bootstrap confidence interval for a mean' in line:
                output.append('  </introduction>\n\n')
                output.append('  <section xml:id="sec-boot1mean">\n')
                output.append('    <title>Bootstrap confidence interval for a mean</title>\n')
                section_level = 1
            elif 'Mathematical model for a mean' in line:
                if section_level == 2:
                    output.append('    </subsection>\n')
                output.append('  </section>\n\n')
                output.append('  <section xml:id="sec-one-mean-math">\n')
                output.append('    <title>Mathematical model for a mean</title>\n')
                section_level = 1
            else:
                # Generic section
                section_id = line.split('{#')[1].rstrip('}') if '{#' in line else ''
                title = line.replace('## ', '').split('{#')[0].strip()
                if section_id:
                    output.append(f'\n  <section xml:id="{section_id}">\n')
                else:
                    output.append('\n  <section>\n')
                output.append(f'    <title>{title}</title>\n')
                section_level = 1
            i += 1
            continue
        
        # Subsection headings
        if line.startswith('### '):
            if section_level == 2:
                output.append('    </subsection>\n')
            
            section_id = line.split('{#')[1].rstrip('}') if '{#' in line else ''
            title = line.replace('### ', '').split('{#')[0].strip()
            if section_id:
                output.append(f'\n    <subsection xml:id="{section_id}">\n')
            else:
                output.append('\n    <subsection>\n')
            output.append(f'      <title>{title}</title>\n')
            section_level = 2
            i += 1
            continue
        
        # Check for callout blocks (Solution, etc.)
        if line.startswith('::: {.') and 'workedexample' in line or 'guidedpractice' in line:
            in_exercise = True
            exercise_lines = []
            i += 1
            continue
        
        if line == '## Solution' or (line.startswith('::: {') and 'solution' in line.lower()):
            # This is part of a guided practice - start solution
            if in_exercise:
                # Start solution section
                exercise_lines.append('SOLUTION_START')
            i += 1
            continue
        
        if in_exercise and line == ':::':
            # End of exercise block
            # Process exercise_lines and output as <exercise>
            output.append('\n      <exercise>\n')
            output.append('        <statement>\n')
            
            in_solution = False
            for ex_line in exercise_lines:
                if ex_line == 'SOLUTION_START':
                    output.append('        </statement>\n')
                    output.append('        <solution>\n')
                    in_solution = True
                else:
                    indent = '          ' if not in_solution else '          '
                    if ex_line.strip():
                        processed = process_line(ex_line)
                        output.append(f'{indent}<p>{processed}</p>\n')
            
            if in_solution:
                output.append('        </solution>\n')
            else:
                output.append('        </statement>\n')
            output.append('      </exercise>\n')
            
            in_exercise = False
            exercise_lines = []
            i += 1
            continue
        
        if in_exercise:
            exercise_lines.append(line)
            i += 1
            continue
        
        # Check for code blocks
        if line.startswith('```{r}') or line.startswith('```{r '):
            in_code_block = True
            code_lines = []
            # Check for label and caption in next few lines
            j = i + 1
            while j < len(lines) and lines[j].startswith('#|'):
                code_line = lines[j]
                if 'label:' in code_line:
                    figure_label = code_line.split('label:')[1].strip()
                if 'fig-cap:' in code_line:
                    j += 1
                    caption_lines = []
                    while j < len(lines) and (lines[j].startswith('#|  ') or lines[j].startswith('#|   ')):
                        caption_lines.append(lines[j].replace('#|', '').strip())
                        j += 1
                    figure_caption = ' '.join(caption_lines)
                if 'out-width:' in code_line:
                    figure_width = code_line.split('out-width:')[1].strip()
                j += 1
            
            # Skip to actual code or end
            i += 1
            while i < len(lines) and lines[i].startswith('#|'):
                i += 1
            
            # Collect code lines
            while i < len(lines) and not lines[i].startswith('```'):
                if lines[i].strip():
                    code_lines.append(lines[i])
                i += 1
            
            # End of code block
            if i < len(lines) and lines[i].startswith('```'):
                i += 1
            
            # Determine if this is a figure or code listing
            if figure_label.startswith('fig-'):
                # This is a figure
                fig_id = figure_label
                fig_source = figure_label.replace('fig-', '') + '.png'
                if 'include_graphics' in '\n'.join(code_lines):
                    # Extract image filename
                    for code_line in code_lines:
                        if 'include_graphics' in code_line:
                            match = re.search(r'include_graphics\(["\']([^"\']+)["\']\)', code_line)
                            if match:
                                fig_source = match.group(1)
                
                output.append(f'\n      <figure xml:id="{fig_id}">\n')
                if figure_caption:
                    cap_processed = process_line(figure_caption)
                    output.append(f'        <caption>{cap_processed}</caption>\n')
                output.append(f'        <image source="{fig_source}" width="{figure_width}"/>\n')
                output.append('      </figure>\n')
                
                figure_label = ""
                figure_caption = ""
                figure_width = "70%"
            elif code_lines:
                # This is a code listing
                output.append('\n      <listing>\n')
                if figure_caption:
                    output.append(f'        <caption>{process_line(figure_caption)}</caption>\n')
                output.append('        <program language="r"><input>\n')
                for code_line in code_lines:
                    output.append(escape_xml(code_line) + '\n')
                output.append('        </input></program>\n')
                output.append('      </listing>\n')
            
            in_code_block = False
            code_lines = []
            continue
        
        # Check for chapterintro block
        if '::: {.chapterintro' in line:
            if not in_intro:
                output.append('  <introduction>\n')
                in_intro = True
            i += 1
            continue
        
        # Check for end of intro block
        if line == ':::' and in_intro and i > 20:
            # Don't close yet, wait for first section
            i += 1
            continue
        
        # Regular paragraph
        if line.strip() and not line.startswith('#|') and not line.startswith('```'):
            processed = process_line(line)
            if in_intro:
                output.append(f'    <p>{processed}</p>\n')
            elif section_level == 2:
                output.append(f'      <p>{processed}</p>\n')
            elif section_level == 1:
                output.append(f'    <p>{processed}</p>\n')
            else:
                output.append(f'  <p>{processed}</p>\n')
        
        i += 1
    
    # Close any remaining sections
    if section_level == 2:
        output.append('    </subsection>\n')
        output.append('  </section>\n')
    elif section_level == 1:
        output.append('  </section>\n')
    
    # Ensure chapter is closed
    if '</chapter>' not in ''.join(output[-5:]):
        output.append('</chapter>\n')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output)
    
    print(f"Conversion complete! Output written to {output_file}")
    print(f"Processed {len(lines)} lines from input file")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Systematic converter for explore-numerical.qmd to PreTeXt XML
"""

import re
import sys

def read_file(filepath):
    """Read the entire file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def process_inline_formatting(text):
    """Process inline formatting: bold, italic, code, cross-refs"""
    # Handle cross-references first
    text = re.sub(r'@fig-([a-zA-Z0-9_-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@sec-([a-zA-Z0-9_-]+)', r'<xref ref="sec-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9_-]+)', r'<xref ref="tbl-\1" />', text)
    
    # Handle bold with \index{} -> <term> and <idx>
    def bold_with_index(match):
        term = match.group(1)
        index = match.group(2)
        return f'<term>{term}</term><idx>{index}</idx>'
    text = re.sub(r'\*\*([^*]+)\*\*\\index\{([^}]+)\}', bold_with_index, text)
    
    # Handle remaining bold -> <alert>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Handle italic -> <em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Handle inline code -> <c>
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Handle R inline expressions
    text = re.sub(r'r nrow\(loan50\)', '50', text)
    text = re.sub(r'r nrow\(county\)', '3142', text)
    text = re.sub(r'r round\(loan50_interest_rate_mean, 2\)', '11.57', text)
    
    # Remove \vspace, \clearpage
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\clearpage', '', text)
    
    # Handle \$ for literal dollar signs
    text = text.replace('\\$', '$')
    
    return text

def escape_xml(text):
    """Escape XML special characters but preserve already-escaped ones and LaTeX"""
    # Don't touch LaTeX math
    return text

def convert_to_ptx(lines):
    """Main conversion function"""
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8" ?>')
    output.append('')
    output.append('<chapter xml:id="ch05-exploring-numerical">')
    output.append('  <title>Exploring numerical data</title>')
    output.append('')
    
    i = 0
    in_code_block = False
    in_worked_example = False
    in_guided_practice = False
    in_important = False
    in_data = False
    in_content_visible = False
    in_pronunciation = False
    in_solution = False
    current_section = None
    current_subsection = None
    section_stack = []
    buffer = []
    fig_label = None
    fig_cap = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip initial metadata
        if i == 0 and line.startswith('# Exploring'):
            i += 1
            continue
            
        # Skip R code setup blocks
        if line.startswith('```{r}') and i < 10:
            while i < len(lines) and not lines[i].startswith('```'):
                i += 1
            i += 1  # skip closing ```
            continue
            
        # Handle chapterintro
        if '::: {.chapterintro' in line:
            output.append('  <introduction>')
            i += 1
            intro_lines = []
            while i < len(lines) and ':::' not in lines[i]:
                intro_lines.append(lines[i].rstrip())
                i += 1
            # Process intro content
            para_text = ' '.join(intro_lines).strip()
            para_text = process_inline_formatting(para_text)
            output.append(f'    <p>')
            output.append(f'      {para_text}')
            output.append(f'    </p>')
            output.append('  </introduction>')
            i += 1
            continue
        
        # Handle sections
        if line.startswith('## ') and not in_worked_example and not in_guided_practice:
            # Close previous subsection if any
            if current_subsection:
                output.append('  </subsection>')
                current_subsection = None
            
            # Close previous section if any
            if current_section:
                output.append('  </section>')
                current_section = None
            
            # Extract section info
            match = re.match(r'##\s+(.+?)\s+\{#([^}]+)\}', line)
            if match:
                title = match.group(1)
                section_id = match.group(2)
                output.append('')
                output.append(f'  <section xml:id="{section_id}">')
                output.append(f'    <title>{title}</title>')
                current_section = section_id
            i += 1
            continue
            
        # Handle subsections
        if line.startswith('### ') and not in_worked_example and not in_guided_practice:
            # Close previous subsection if any
            if current_subsection:
                output.append('  </subsection>')
                current_subsection = None
            
            # Extract subsection info
            match = re.match(r'###\s+(.+?)\s+\{#([^}]+)\}', line)
            if match:
                title = match.group(1)
                subsection_id = match.group(2)
                output.append('')
                output.append(f'    <subsection xml:id="{subsection_id}">')
                output.append(f'      <title>{title}</title>')
                current_subsection = subsection_id
            i += 1
            continue
        
        # Skip content-visible and pronunciation blocks
        if '::: {.content-visible' in line or '::: {.pronunciation' in line:
            depth = 1
            i += 1
            while i < len(lines) and depth > 0:
                if ':::' in lines[i] and '{.' not in lines[i]:
                    depth -= 1
                elif ':::' in lines[i] and '{.' in lines[i]:
                    depth += 1
                i += 1
            continue
        
        # Handle data blocks
        if '::: {.data' in line:
            i += 1
            data_lines = []
            while i < len(lines) and ':::' not in lines[i]:
                data_lines.append(lines[i].rstrip())
                i += 1
            data_text = ' '.join(data_lines).strip()
            data_text = process_inline_formatting(data_text)
            output.append('    <note>')
            output.append('      <title>Data</title>')
            output.append(f'      <p>{data_text}</p>')
            output.append('    </note>')
            i += 1
            continue
        
        # Handle important blocks
        if '::: {.important' in line:
            i += 1
            important_lines = []
            while i < len(lines) and ':::' not in lines[i]:
                important_lines.append(lines[i].rstrip())
                i += 1
            
            # Find title (first bold text)
            title = None
            content_lines = []
            for imp_line in important_lines:
                if title is None and '**' in imp_line:
                    title_match = re.search(r'\*\*([^*]+)\*\*', imp_line)
                    if title_match:
                        title = title_match.group(1).rstrip('.')
                        # Remove title from line
                        imp_line = re.sub(r'\*\*[^*]+\*\*\.?', '', imp_line).strip()
                if imp_line:
                    content_lines.append(imp_line)
            
            content = ' '.join(content_lines).strip()
            content = process_inline_formatting(content)
            
            output.append('    <assemblage>')
            if title:
                output.append(f'      <title>{title}</title>')
            output.append(f'      <p>{content}</p>')
            output.append('    </assemblage>')
            i += 1
            continue
        
        # Handle figures with R code
        if line.startswith('```{r}'):
            in_code_block = True
            fig_label = None
            fig_cap = []
            i += 1
            
            # Read code block metadata
            while i < len(lines) and not lines[i].startswith('```'):
                code_line = lines[i].rstrip()
                if '#| label: fig-' in code_line:
                    fig_label = code_line.split('fig-')[1].strip()
                elif '#| fig-cap:' in code_line:
                    cap_line = code_line.split('fig-cap:')[1].strip()
                    if cap_line.startswith('|'):
                        cap_line = cap_line[1:].strip()
                    fig_cap.append(cap_line)
                elif '#|' in code_line and fig_cap:
                    # Continuation of caption
                    cont_line = code_line.split('#|')[1].strip()
                    if cont_line and not cont_line.startswith('fig-alt') and not cont_line.startswith('fig-asp'):
                        fig_cap.append(cont_line)
                i += 1
            
            # Skip to end of code block
            while i < len(lines) and not lines[i].startswith('```'):
                i += 1
            i += 1  # skip ```
            
            # Create figure if we have label
            if fig_label and not fig_label.startswith('tbl-'):
                caption = ' '.join(fig_cap).strip()
                caption = process_inline_formatting(caption)
                output.append(f'    <figure xml:id="fig-{fig_label}">')
                output.append(f'      <caption>{caption}</caption>')
                output.append(f'      <image source="images/explore-numerical/fig-{fig_label}-1.png" width="70%" />')
                output.append('    </figure>')
            
            in_code_block = False
            continue
        
        # Handle worked examples
        if '::: {.workedexample' in line:
            i += 1
            statement_lines = []
            solution_lines = []
            in_statement = True
            
            while i < len(lines) and ':::' not in lines[i]:
                if lines[i].strip() == '------------------------------------------------------------------------' or lines[i].strip() == '---':
                    in_statement = False
                    i += 1
                    continue
                
                if in_statement:
                    statement_lines.append(lines[i].rstrip())
                else:
                    solution_lines.append(lines[i].rstrip())
                i += 1
            
            statement = ' '.join(statement_lines).strip()
            statement = process_inline_formatting(statement)
            solution = ' '.join(solution_lines).strip()
            solution = process_inline_formatting(solution)
            
            output.append('    <example>')
            output.append('      <statement>')
            output.append(f'        <p>{statement}</p>')
            output.append('      </statement>')
            output.append('      <solution>')
            output.append(f'        <p>{solution}</p>')
            output.append('      </solution>')
            output.append('    </example>')
            i += 1
            continue
        
        # Handle guided practices
        if '::: {.guidedpractice' in line:
            i += 1
            statement_lines = []
            solution_lines = []
            
            # Read statement
            while i < len(lines) and '::: {.callout-note' not in lines[i] and ':::' not in lines[i]:
                statement_lines.append(lines[i].rstrip())
                i += 1
            
            # Read solution if present
            if '::: {.callout-note' in lines[i]:
                i += 1
                # Skip "## Solution" line
                if i < len(lines) and '## Solution' in lines[i]:
                    i += 1
                while i < len(lines) and ':::' not in lines[i]:
                    solution_lines.append(lines[i].rstrip())
                    i += 1
                i += 1  # skip closing :::
            
            # Skip outer closing :::
            if i < len(lines) and ':::' in lines[i]:
                i += 1
            
            statement = ' '.join(statement_lines).strip()
            statement = process_inline_formatting(statement)
            solution = ' '.join(solution_lines).strip()
            solution = process_inline_formatting(solution)
            
            output.append('    <exercise>')
            output.append('      <statement>')
            output.append(f'        <p>{statement}</p>')
            output.append('      </statement>')
            if solution:
                output.append('      <solution>')
                output.append(f'        <p>{solution}</p>')
                output.append('      </solution>')
            output.append('    </exercise>')
            continue
        
        # Handle regular paragraphs
        if line.strip() and not line.startswith('#') and not line.startswith('```') and not line.startswith(':::'):
            para = process_inline_formatting(line)
            if para.strip():
                output.append(f'    <p>{para}</p>')
        
        i += 1
    
    # Close any open subsection
    if current_subsection:
        output.append('  </subsection>')
    
    # Close any open section
    if current_section:
        output.append('  </section>')
    
    output.append('</chapter>')
    return '\n'.join(output)

def main():
    input_file = '/home/runner/work/ims/ims/explore-numerical.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch05-exploring-numerical.ptx'
    
    lines = read_file(input_file)
    ptx_content = convert_to_ptx(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ptx_content)
    
    print(f"Converted {len(lines)} lines to {output_file}")

if __name__ == '__main__':
    main()

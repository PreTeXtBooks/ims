#!/usr/bin/env python3
"""Convert explore-numerical.qmd to PreTeXt XML format."""

import re
import sys

def escape_xml(text):
    """Escape special XML characters but preserve existing entities."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Fix double escaping of entities
    text = text.replace('&amp;lt;', '&lt;')
    text = text.replace('&amp;gt;', '&gt;')
    text = text.replace('&amp;amp;', '&amp;')
    return text

def process_inline_formatting(text):
    """Process inline text formatting: bold, italic, code, cross-refs."""
    # First, handle cross-references
    text = re.sub(r'@fig-([a-zA-Z0-9-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@sec-([a-zA-Z0-9-]+)', r'<xref ref="sec-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9-]+)', r'<xref ref="tbl-\1" />', text)
    
    # Handle bold with index -> term+idx
    # Match **text**\index{index_text}
    text = re.sub(r'\*\*([^*]+)\*\*\\index\{([^}]+)\}', 
                  r'<term>\1</term><idx>\2</idx>', text)
    
    # Handle bold alone -> alert
    text = re.sub(r'\*\*([^*]+)\*\*', r'<alert>\1</alert>', text)
    
    # Handle italic -> em
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Handle inline code -> c
    text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
    
    # Handle inline math (preserve LaTeX)
    # Already preserved by not escaping $ in math mode
    
    return text

def read_source_file(filepath):
    """Read the source QMD file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def convert_to_ptx(lines):
    """Convert QMD lines to PTX."""
    output = []
    output.append('<?xml version="1.0" encoding="UTF-8" ?>\n')
    output.append('\n')
    output.append('<chapter xml:id="ch05-exploring-numerical">\n')
    output.append('  <title>Exploring numerical data</title>\n')
    output.append('\n')
    
    i = 0
    indent = '  '
    section_stack = []  # Track open sections
    in_block = None  # Track current block type
    block_content = []
    block_indent = ''
    skip_until = None  # For skipping content
    
    while i < len(lines):
        line = lines[i]
        orig_line = line
        line = line.rstrip('\n')
        
        # Skip R setup blocks
        if line.strip().startswith('```{r}') and i + 1 < len(lines) and '#| include: false' in lines[i+1]:
            # Skip until end of code block
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            i += 1
            continue
        
        # Skip terms collection blocks
        if 'terms_chp_05' in line:
            i += 1
            continue
        
        # Skip vspace and clearpage
        if line.strip().startswith('\\vspace') or line.strip().startswith('\\clearpage'):
            i += 1
            continue
        
        # Skip pronunciation blocks
        if line.strip() == '::: {.pronunciation}':
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                i += 1
            i += 1
            continue
        
        # Handle chapter intro
        if line.strip() == '::: {.chapterintro data-latex=""}':
            output.append(indent + '<introduction>\n')
            i += 1
            intro_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                intro_lines.append(lines[i].rstrip('\n'))
                i += 1
            # Process intro content
            intro_text = '\n'.join(intro_lines).strip()
            intro_text = process_inline_formatting(intro_text)
            # Split into paragraphs
            paras = intro_text.split('\n\n')
            for para in paras:
                if para.strip():
                    output.append(indent + '  <p>\n')
                    output.append(indent + '    ' + para.strip() + '\n')
                    output.append(indent + '  </p>\n')
                    output.append('\n')
            output.append(indent + '</introduction>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle figures (R code blocks with fig- label)
        if line.strip().startswith('```{r}'):
            # Look ahead for label
            j = i + 1
            label = None
            caption = []
            while j < len(lines) and not lines[j].strip().startswith('```'):
                if lines[j].strip().startswith('#| label: fig-'):
                    label = lines[j].strip().split(':', 1)[1].strip()
                elif lines[j].strip().startswith('#| fig-cap:'):
                    # Collect multi-line caption
                    cap_line = lines[j].strip().split(':', 1)[1].strip()
                    if cap_line == '|':
                        j += 1
                        while j < len(lines) and (lines[j].strip().startswith('#|  ') or lines[j].strip() == '#|'):
                            if lines[j].strip() != '#|':
                                caption.append(lines[j].strip()[4:])  # Remove '#|  '
                            j += 1
                        j -= 1
                    else:
                        caption.append(cap_line)
                j += 1
            
            if label and label.startswith('fig-'):
                # This is a figure
                caption_text = ' '.join(caption).strip()
                caption_text = process_inline_formatting(caption_text)
                fig_id = label
                
                output.append(indent + '<figure xml:id="' + fig_id + '">\n')
                output.append(indent + '  <caption>' + caption_text + '</caption>\n')
                output.append(indent + '  <image source="images/explore-numerical/' + fig_id + '-1.png" width="70%" />\n')
                output.append(indent + '</figure>\n')
                output.append('\n')
                
                # Skip to end of code block
                i = j + 1
                continue
            else:
                # Skip code blocks without fig- label
                i = j + 1
                continue
        
        # Handle sections
        section_match = re.match(r'^##\s+(.+?)\s*\{#(sec-[a-zA-Z0-9-]+)\}\s*$', line)
        if section_match:
            title = section_match.group(1).strip()
            sec_id = section_match.group(2)
            
            # Close any open subsections
            while section_stack and section_stack[-1]['type'] == 'subsection':
                sect = section_stack.pop()
                indent = '  ' * (len(section_stack) + 1)
                output.append(indent + '</subsection>\n')
                output.append('\n')
            
            # Close any open section
            if section_stack and section_stack[-1]['type'] == 'section':
                section_stack.pop()
                indent = '  ' * (len(section_stack) + 1)
                output.append(indent + '</section>\n')
                output.append('\n')
            
            # Open new section
            section_stack.append({'type': 'section', 'id': sec_id})
            indent = '  ' * (len(section_stack) + 1)
            output.append(indent + '<section xml:id="' + sec_id + '">\n')
            title = process_inline_formatting(title)
            output.append(indent + '  <title>' + title + '</title>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle subsections
        subsection_match = re.match(r'^###\s+(.+?)\s*\{#(subsec-[a-zA-Z0-9-]+)\}\s*$', line)
        if subsection_match:
            title = subsection_match.group(1).strip()
            subsec_id = subsection_match.group(2)
            
            # Close any open subsection
            if section_stack and section_stack[-1]['type'] == 'subsection':
                section_stack.pop()
                indent = '  ' * (len(section_stack) + 1)
                output.append(indent + '</subsection>\n')
                output.append('\n')
            
            # Open new subsection
            section_stack.append({'type': 'subsection', 'id': subsec_id})
            indent = '  ' * (len(section_stack) + 1)
            output.append(indent + '<subsection xml:id="' + subsec_id + '">\n')
            title = process_inline_formatting(title)
            output.append(indent + '  <title>' + title + '</title>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle worked examples
        if line.strip() == '::: {.workedexample data-latex=""}':
            i += 1
            example_content = []
            while i < len(lines) and lines[i].strip() != ':::':
                example_content.append(lines[i].rstrip('\n'))
                i += 1
            
            # Split by separator
            separator_idx = -1
            for j, l in enumerate(example_content):
                if l.strip() == '------------------------------------------------------------------------':
                    separator_idx = j
                    break
            
            if separator_idx >= 0:
                statement = '\n'.join(example_content[:separator_idx]).strip()
                solution = '\n'.join(example_content[separator_idx+1:]).strip()
            else:
                statement = '\n'.join(example_content).strip()
                solution = ''
            
            statement = process_inline_formatting(statement)
            solution = process_inline_formatting(solution)
            
            output.append(indent + '<example>\n')
            output.append(indent + '  <statement>\n')
            output.append(indent + '    <p>' + statement + '</p>\n')
            output.append(indent + '  </statement>\n')
            if solution:
                output.append(indent + '  <solution>\n')
                output.append(indent + '    <p>' + solution + '</p>\n')
                output.append(indent + '  </solution>\n')
            output.append(indent + '</example>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle guided practices
        if line.strip() == '::: {.guidedpractice data-latex=""}':
            i += 1
            gp_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                gp_lines.append(lines[i].rstrip('\n'))
                i += 1
            
            # Find statement (before callout-note)
            statement_lines = []
            j = 0
            while j < len(gp_lines):
                if gp_lines[j].strip() == '::: {.callout-note}':
                    break
                statement_lines.append(gp_lines[j])
                j += 1
            
            statement = '\n'.join(statement_lines).strip()
            statement = process_inline_formatting(statement)
            
            # Find solution (inside callout-note)
            solution = ''
            if j < len(gp_lines):
                j += 1  # Skip ::: {.callout-note}
                # Skip "## Answer" if present
                if j < len(gp_lines) and gp_lines[j].strip().startswith('## '):
                    j += 1
                solution_lines = []
                while j < len(gp_lines) and gp_lines[j].strip() != ':::':
                    solution_lines.append(gp_lines[j])
                    j += 1
                solution = '\n'.join(solution_lines).strip()
                solution = process_inline_formatting(solution)
            
            output.append(indent + '<exercise>\n')
            output.append(indent + '  <statement>\n')
            output.append(indent + '    <p>' + statement + '</p>\n')
            output.append(indent + '  </statement>\n')
            if solution:
                output.append(indent + '  <solution>\n')
                output.append(indent + '    <p>' + solution + '</p>\n')
                output.append(indent + '  </solution>\n')
            output.append(indent + '</exercise>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle important blocks
        if line.strip() == '::: {.important data-latex=""}':
            i += 1
            imp_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                imp_lines.append(lines[i].rstrip('\n'))
                i += 1
            
            content = '\n'.join(imp_lines).strip()
            
            # Extract title (first bold text)
            title_match = re.search(r'\*\*([^*]+)\*\*', content)
            if title_match:
                title = title_match.group(1)
                # Remove title from content
                content = re.sub(r'\*\*' + re.escape(title) + r'\*\*\.?\s*', '', content, count=1)
            else:
                title = ''
            
            content = process_inline_formatting(content)
            
            output.append(indent + '<assemblage>\n')
            if title:
                output.append(indent + '  <title>' + title + '</title>\n')
            output.append(indent + '  <p>' + content + '</p>\n')
            output.append(indent + '</assemblage>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle data blocks
        if line.strip() == '::: {.data data-latex=""}':
            i += 1
            data_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                data_lines.append(lines[i].rstrip('\n'))
                i += 1
            
            content = '\n'.join(data_lines).strip()
            content = process_inline_formatting(content)
            
            output.append(indent + '<note>\n')
            output.append(indent + '  <title>Data</title>\n')
            output.append(indent + '  <p>' + content + '</p>\n')
            output.append(indent + '</note>\n')
            output.append('\n')
            i += 1
            continue
        
        # Handle regular paragraphs
        if line.strip() and not line.strip().startswith('#') and not line.strip().startswith(':::'):
            # Collect paragraph lines
            para_lines = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith(':::') and not lines[i].strip().startswith('```'):
                para_lines.append(lines[i].rstrip('\n'))
                i += 1
            
            para = ' '.join([l.strip() for l in para_lines])
            
            # Replace R expressions
            para = para.replace('`r nrow(loan50)`', '50')
            para = para.replace('`r nrow(county)`', '3142')
            para = para.replace('`r round(loan50_interest_rate_mean, 2)`', '11.57')
            
            para = process_inline_formatting(para)
            
            output.append(indent + '<p>' + para + '</p>\n')
            output.append('\n')
            continue
        
        # Default: skip line
        i += 1
    
    # Close any remaining sections
    while section_stack:
        sect = section_stack.pop()
        indent = '  ' * (len(section_stack) + 1)
        if sect['type'] == 'subsection':
            output.append(indent + '</subsection>\n')
        else:
            output.append(indent + '</section>\n')
        output.append('\n')
    
    output.append('</chapter>\n')
    
    return ''.join(output)

def main():
    source_file = '/home/runner/work/ims/ims/explore-numerical.qmd'
    target_file = '/home/runner/work/ims/ims/source/chapters/ch05-exploring-numerical.ptx'
    
    lines = read_source_file(source_file)
    ptx_content = convert_to_ptx(lines)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(ptx_content)
    
    print(f"Conversion complete. Output written to {target_file}")
    print(f"Converted {len(lines)} lines from source file")

if __name__ == '__main__':
    main()

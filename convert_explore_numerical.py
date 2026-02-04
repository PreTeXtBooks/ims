#!/usr/bin/env python3
"""Convert explore-numerical.qmd to PreTeXt XML format."""

import re
import sys

def escape_xml(text):
    """Escape XML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def process_inline_formatting(text):
    """Process inline formatting like bold, italic, code, cross-refs."""
    # Handle inline R code replacements
    text = re.sub(r'`r nrow\(loan50\)`', '50', text)
    text = re.sub(r'`r nrow\(county\)`', '3142', text)
    text = re.sub(r'`r.*?round\(loan50_interest_rate_mean.*?\)`', '11.57', text)
    
    # Cross-references
    text = re.sub(r'@fig-([a-zA-Z0-9-]+)', r'<xref ref="fig-\1" />', text)
    text = re.sub(r'@tbl-([a-zA-Z0-9-]+)', r'<xref ref="tbl-\1" />', text)
    text = re.sub(r'@sec-([a-zA-Z0-9-]+)', r'<xref ref="sec-\1" />', text)
    
    # Bold with index (term)
    text = re.sub(r'\*\*([^*]+?)\*\*\\index\{([^}]+)\}', r'<term>\1</term><idx>\2</idx>', text)
    # Bold without index
    text = re.sub(r'\*\*([^*]+?)\*\*', r'<alert>\1</alert>', text)
    
    # Italic
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
    
    # Code
    text = re.sub(r'`([^`]+?)`', r'<c>\1</c>', text)
    
    # Index alone
    text = re.sub(r'\\index\{([^}]+)\}', r'<idx>\1</idx>', text)
    
    # Remove vspace and clearpage
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\clearpage', '', text)
    
    return text

def extract_figure_label(lines, start_idx):
    """Extract figure label from R code block."""
    label = None
    caption = []
    for i in range(start_idx, min(start_idx + 20, len(lines))):
        if '#| label:' in lines[i]:
            label = lines[i].split(':', 1)[1].strip()
        elif '#| fig-cap:' in lines[i]:
            # Start collecting caption
            cap_line = lines[i].split(':', 1)[1].strip()
            if cap_line:
                caption.append(cap_line)
            # Continue reading caption lines
            j = i + 1
            while j < len(lines) and lines[j].startswith('#|   '):
                caption.append(lines[j].replace('#|   ', '').strip())
                j += 1
            break
    
    caption_text = ' '.join(caption).strip()
    # Remove pipe symbols
    caption_text = caption_text.replace('|', '').strip()
    
    return label, caption_text

class PTXConverter:
    def __init__(self, lines):
        self.lines = lines
        self.output = []
        self.indent_level = 1
        self.i = 0
        
    def indent(self, extra=0):
        return '  ' * (self.indent_level + extra)
    
    def add_line(self, text, extra_indent=0):
        if text.strip():
            self.output.append(self.indent(extra_indent) + text + '\n')
        else:
            self.output.append('\n')
    
    def convert(self):
        """Main conversion method."""
        # XML declaration and chapter opening
        self.output.append('<?xml version="1.0" encoding="UTF-8" ?>\n\n')
        self.output.append('<chapter xml:id="ch05-exploring-numerical">\n')
        self.output.append('  <title>Exploring numerical data</title>\n\n')
        
        # Skip title line and initial R code block
        self.i = 0
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            # Skip title
            if line.startswith('# Exploring numerical data'):
                self.i += 1
                self.i += 1  # Skip blank line
                continue
            
            # Skip initial R setup block
            if '```{r}' in line and self.i + 1 < len(self.lines) and 'include: false' in self.lines[self.i + 1]:
                while self.i < len(self.lines) and '```' not in self.lines[self.i]:
                    self.i += 1
                self.i += 1  # Skip closing ```
                self.i += 1  # Skip blank line after
                continue
            
            break
        
        # Now process the rest
        self.process_content()
        
        # Close chapter
        self.output.append('</chapter>\n')
        
        return ''.join(self.output)
    
    def process_content(self):
        """Process the main content."""
        in_introduction = False
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            # Check for chapter intro
            if '::: {.chapterintro' in line:
                self.add_line('<introduction>')
                self.indent_level += 1
                in_introduction = True
                self.i += 1
                continue
            
            # Check for end of intro or start of section
            if in_introduction:
                if line.strip() == ':::' or line.startswith('## '):
                    self.indent_level -= 1
                    self.add_line('</introduction>')
                    self.add_line('')
                    in_introduction = False
                    if line.strip() == ':::':
                        self.i += 1
                        continue
            
            # Handle sections
            if line.startswith('## ') and not line.startswith('## Solution'):
                # Extract section title and ID
                match = re.match(r'##\s+(.+?)\s+\{#(.+?)\}', line)
                if match:
                    title = match.group(1)
                    sec_id = match.group(2)
                    self.add_line(f'<section xml:id="{sec_id}">')
                    self.indent_level += 1
                    self.add_line(f'<title>{title}</title>')
                    self.add_line('')
                    self.i += 1
                    continue
                else:
                    # Section without ID (like "## Chapter review")
                    title = line.replace('##', '').strip()
                    self.i += 1
                    continue
            
            # Handle subsections  
            if line.startswith('### '):
                match = re.match(r'###\s+(.+?)(?:\s+\{#(.+?)\})?', line)
                if match:
                    title = match.group(1)
                    subsec_id = match.group(2) if match.group(2) else None
                    if subsec_id:
                        self.add_line(f'<subsection xml:id="{subsec_id}">')
                    else:
                        self.add_line('<subsection>')
                    self.indent_level += 1
                    self.add_line(f'<title>{title}</title>')
                    self.add_line('')
                    self.i += 1
                    continue
            
            # Handle code blocks
            if line.strip().startswith('```{r}'):
                self.process_code_block()
                continue
            
            # Handle special blocks
            if '::: {.workedexample' in line:
                self.process_worked_example()
                continue
            
            if '::: {.guidedpractice' in line:
                self.process_guided_practice()
                continue
            
            if '::: {.important' in line:
                self.process_important()
                continue
            
            if '::: {.data' in line:
                self.process_data_block()
                continue
            
            # Skip pronunciation and content-visible blocks
            if '::: {.pronunciation' in line or '::: {.content-visible' in line:
                while self.i < len(self.lines) and self.lines[self.i].strip() != ':::':
                    self.i += 1
                self.i += 1  # Skip :::
                continue
            
            # Handle paragraphs
            if line.strip() and not line.startswith('#'):
                self.process_paragraph()
                continue
            
            # Skip blank lines
            if not line.strip():
                self.i += 1
                continue
            
            # Default: skip
            self.i += 1
    
    def process_paragraph(self):
        """Process a paragraph of text."""
        para_lines = []
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            # Stop at blank line, section header, or special block
            if (not line.strip() or 
                line.startswith('#') or 
                line.strip().startswith(':::') or
                line.strip().startswith('```')):
                break
            
            para_lines.append(line.rstrip())
            self.i += 1
        
        if para_lines:
            # Join and process
            text = ' '.join(para_lines)
            text = process_inline_formatting(text)
            
            # Check if this is a list
            if text.strip().startswith('-'):
                self.add_line('<ul>')
                # Split into list items
                items = text.strip().split('\n-')
                for item in items:
                    item = item.strip().lstrip('-').strip()
                    if item:
                        self.add_line(f'  <li><p>{item}</p></li>')
                self.add_line('</ul>')
            else:
                self.add_line('<p>')
                self.add_line(f'  {text}', 0)
                self.add_line('</p>')
            self.add_line('')
    
    def process_code_block(self):
        """Process R code block - check if it's a figure or regular code."""
        start_i = self.i
        self.i += 1
        
        # Check for figure label
        label, caption = extract_figure_label(self.lines, start_i)
        
        # Skip to end of code block
        while self.i < len(self.lines) and '```' not in self.lines[self.i]:
            self.i += 1
        self.i += 1  # Skip closing ```
        
        if label:
            # This is a figure
            caption = process_inline_formatting(caption)
            # Determine image filename
            img_file = f"images/explore-numerical/{label}-1.png"
            
            self.add_line(f'<figure xml:id="{label}">')
            self.add_line(f'  <caption>{caption}</caption>', 0)
            self.add_line(f'  <image source="{img_file}" width="70%" />', 0)
            self.add_line('</figure>')
            self.add_line('')
        # else: skip non-figure code blocks
    
    def process_worked_example(self):
        """Process worked example block."""
        self.i += 1  # Skip opening :::
        
        statement_lines = []
        solution_lines = []
        in_solution = False
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            if line.strip() == ':::':
                break
            
            if '------------------------------------------------------------------------' in line:
                in_solution = True
                self.i += 1
                continue
            
            if in_solution:
                solution_lines.append(line.rstrip())
            else:
                statement_lines.append(line.rstrip())
            
            self.i += 1
        
        self.i += 1  # Skip closing :::
        
        # Output
        self.add_line('<example>')
        self.add_line('  <statement>', 0)
        self.add_line('    <p>', 0)
        statement_text = ' '.join(statement_lines)
        statement_text = process_inline_formatting(statement_text)
        self.add_line(f'      {statement_text}', 0)
        self.add_line('    </p>', 0)
        self.add_line('  </statement>', 0)
        
        if solution_lines:
            self.add_line('  <solution>', 0)
            self.add_line('    <p>', 0)
            solution_text = ' '.join(solution_lines)
            solution_text = process_inline_formatting(solution_text)
            self.add_line(f'      {solution_text}', 0)
            self.add_line('    </p>', 0)
            self.add_line('  </solution>', 0)
        
        self.add_line('</example>')
        self.add_line('')
    
    def process_guided_practice(self):
        """Process guided practice block."""
        self.i += 1  # Skip opening :::
        
        statement_lines = []
        solution_lines = []
        in_callout = False
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            # End of guidedpractice block
            if line.strip() == ':::' and not in_callout:
                break
            
            # Start of callout-note (solution)
            if '::: {.callout-note' in line:
                in_callout = True
                self.i += 1
                # Skip "## Solution" line
                if self.i < len(self.lines) and self.lines[self.i].startswith('## Solution'):
                    self.i += 1
                continue
            
            # End of callout
            if line.strip() == ':::' and in_callout:
                in_callout = False
                self.i += 1
                continue
            
            if in_callout:
                solution_lines.append(line.rstrip())
            else:
                statement_lines.append(line.rstrip())
            
            self.i += 1
        
        self.i += 1  # Skip closing :::
        
        # Output
        self.add_line('<exercise>')
        self.add_line('  <statement>', 0)
        self.add_line('    <p>', 0)
        statement_text = ' '.join(statement_lines)
        statement_text = process_inline_formatting(statement_text)
        self.add_line(f'      {statement_text}', 0)
        self.add_line('    </p>', 0)
        self.add_line('  </statement>', 0)
        
        if solution_lines:
            self.add_line('  <solution>', 0)
            self.add_line('    <p>', 0)
            solution_text = ' '.join(solution_lines)
            solution_text = process_inline_formatting(solution_text)
            self.add_line(f'      {solution_text}', 0)
            self.add_line('    </p>', 0)
            self.add_line('  </solution>', 0)
        
        self.add_line('</exercise>')
        self.add_line('')
    
    def process_important(self):
        """Process important block."""
        self.i += 1  # Skip opening :::
        
        title = None
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            if line.strip() == ':::':
                break
            
            # Check for title (bold text with period)
            if line.strip().startswith('**') and line.strip().endswith('**'):
                title = line.strip().strip('*').strip().rstrip('.')
                self.i += 1
                continue
            
            content_lines.append(line.rstrip())
            self.i += 1
        
        self.i += 1  # Skip closing :::
        
        # Output
        self.add_line('<assemblage>')
        if title:
            self.add_line(f'  <title>{title}</title>', 0)
        
        # Process content
        text = ' '.join(content_lines)
        text = process_inline_formatting(text)
        
        if text.strip():
            self.add_line('  <p>', 0)
            self.add_line(f'    {text}', 0)
            self.add_line('  </p>', 0)
        
        self.add_line('</assemblage>')
        self.add_line('')
    
    def process_data_block(self):
        """Process data block."""
        self.i += 1  # Skip opening :::
        
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.lines[self.i]
            
            if line.strip() == ':::':
                break
            
            content_lines.append(line.rstrip())
            self.i += 1
        
        self.i += 1  # Skip closing :::
        
        # Output
        self.add_line('<note>')
        self.add_line('  <title>Data</title>', 0)
        self.add_line('  <p>', 0)
        
        text = ' '.join(content_lines)
        text = process_inline_formatting(text)
        self.add_line(f'    {text}', 0)
        
        self.add_line('  </p>', 0)
        self.add_line('</note>')
        self.add_line('')


# Main execution
if __name__ == '__main__':
    with open('explore-numerical.qmd', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    converter = PTXConverter(lines)
    result = converter.convert()
    
    print(result[:2000])
    print(f"\n... (converted {len(result)} characters total)")


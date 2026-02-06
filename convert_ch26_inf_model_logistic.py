#!/usr/bin/env python3
"""
Converter for inf-model-logistic.qmd to PreTeXt XML format
Handles chapter 26: Inference for logistic regression
"""

import re
import sys

class QmdToPreTeXtConverter:
    def __init__(self):
        self.output = []
        self.indent_level = 0
        self.in_code_block = False
        self.code_buffer = []
        self.current_label = None
        self.current_caption = None
        
    def indent(self, level=None):
        """Return indentation string"""
        if level is None:
            level = self.indent_level
        return '  ' * level
    
    def add_line(self, line, level=None):
        """Add a line with proper indentation"""
        self.output.append(self.indent(level) + line)
    
    def convert_inline_markdown(self, text):
        """Convert inline markdown to PreTeXt"""
        if not text:
            return text
        
        # Store math expressions to protect them
        math_exprs = []
        def store_math(m):
            math_exprs.append(m.group(1))
            return f"__MATH{len(math_exprs)-1}__"
        text = re.sub(r'\$([^\$]+)\$', store_math, text)
        
        # Store code spans
        code_spans = []
        def store_code(m):
            code_spans.append(m.group(1))
            return f"__CODE{len(code_spans)-1}__"
        text = re.sub(r'`([^`]+)`', store_code, text)
        
        # Bold -> alert
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
        
        # Italic -> em
        text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
        
        # Links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<url href="\2">\1</url>', text)
        
        # Restore code
        for i, code in enumerate(code_spans):
            text = text.replace(f"__CODE{i}__", f"<c>{code}</c>")
        
        # Restore math
        for i, math in enumerate(math_exprs):
            text = text.replace(f"__MATH{i}__", f"<m>{math}</m>")
        
        # Cross-references
        text = re.sub(r'@fig-([a-zA-Z0-9\-_]+)', r'<xref ref="fig-\1" />', text)
        text = re.sub(r'@tbl-([a-zA-Z0-9\-_]+)', r'<xref ref="tbl-\1" />', text)
        text = re.sub(r'@sec-([a-zA-Z0-9\-_]+)', r'<xref ref="sec-\1" />', text)
        text = re.sub(r'\[Chapter -@sec-([a-zA-Z0-9\-_]+)\]', r'<xref ref="sec-\1" />', text)
        
        # Citations
        text = re.sub(r'\[@([a-zA-Z0-9\-:_]+)\]', r'<fn>Citation: \1</fn>', text)
        
        return text
    
    def escape_xml(self, text):
        """Escape XML special characters in code"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def process_paragraph(self, para_lines):
        """Process a paragraph"""
        if not para_lines:
            return
        
        # Join lines and convert
        text = ' '.join(para_lines)
        text = self.convert_inline_markdown(text)
        
        self.add_line('<p>')
        self.add_line('  ' + text, self.indent_level)
        self.add_line('</p>')
        self.add_line('')
    
    def convert(self):
        """Main conversion routine"""
        # Read the qmd file
        with open('/home/runner/work/ims/ims/inf-model-logistic.qmd', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Start document
        self.output.append('<?xml version="1.0" encoding="UTF-8" ?>')
        self.output.append('')
        self.output.append('<chapter xml:id="ch26-inference-logistic-regression">')
        self.indent_level = 1
        self.add_line('<title>Inference for logistic regression</title>')
        self.output.append('')
        
        # Process line by line
        i = 0
        para_buffer = []
        
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip header line
            if i == 0 and line.startswith('# '):
                i += 1
                continue
            
            # Skip include: false code blocks
            if line.startswith('```{r}') or line.startswith('```{r,'):
                # Check if this is an include: false block
                include_false = False
                if i + 1 < len(lines) and 'include: false' in lines[i+1]:
                    include_false = True
                
                # Find end of code block
                j = i + 1
                code_lines = []
                while j < len(lines) and not lines[j].startswith('```'):
                    if not include_false:
                        code_lines.append(lines[j].rstrip())
                    j += 1
                
                # If not include: false, add as listing
                if not include_false and code_lines:
                    # Flush paragraph buffer
                    if para_buffer:
                        self.process_paragraph(para_buffer)
                        para_buffer = []
                    
                    # Extract label and caption if present
                    label = None
                    caption = None
                    filtered_code = []
                    
                    for code_line in code_lines:
                        if code_line.startswith('#| label:'):
                            label = code_line.split(':', 1)[1].strip()
                        elif code_line.startswith('#| tbl-cap:') or code_line.startswith('#| fig-cap:'):
                            caption_start = code_line.split(':', 1)[1].strip()
                            caption = caption_start
                        elif code_line.startswith('#|'):
                            # Skip other directives
                            continue
                        else:
                            filtered_code.append(code_line)
                    
                    # Create listing with R code
                    if label:
                        self.add_line(f'<listing xml:id="listing-{label}">')
                    else:
                        self.add_line('<listing>')
                    self.indent_level += 1
                    
                    if caption:
                        caption_text = self.convert_inline_markdown(caption)
                        self.add_line(f'<caption>{caption_text}</caption>')
                    else:
                        self.add_line('<caption>R code</caption>')
                    
                    self.add_line('<program language="r">')
                    self.add_line('  <input>', self.indent_level)
                    for code_line in filtered_code:
                        escaped = self.escape_xml(code_line)
                        self.add_line(escaped, self.indent_level + 1)
                    self.add_line('  </input>', self.indent_level)
                    self.add_line('</program>')
                    
                    self.indent_level -= 1
                    self.add_line('</listing>')
                    self.add_line('')
                
                i = j + 1
                continue
            
            # Section headers
            if line.startswith('## '):
                # Flush paragraph buffer
                if para_buffer:
                    self.process_paragraph(para_buffer)
                    para_buffer = []
                
                # Close previous section if any
                if hasattr(self, 'in_section') and self.in_section:
                    self.indent_level -= 1
                    self.add_line('</section>')
                    self.add_line('')
                
                title = line[3:].strip()
                section_id = title.lower().replace(' ', '-').replace(',', '')
                self.add_line(f'<section xml:id="sec-{section_id}">')
                self.indent_level += 1
                self.add_line(f'<title>{title}</title>')
                self.add_line('')
                self.in_section = True
                
                i += 1
                continue
            
            # Subsection headers
            if line.startswith('### '):
                # Flush paragraph buffer
                if para_buffer:
                    self.process_paragraph(para_buffer)
                    para_buffer = []
                
                title = line[4:].strip()
                subsection_id = title.lower().replace(' ', '-').replace(',', '')
                self.add_line(f'<subsection xml:id="subsec-{subsection_id}">')
                self.indent_level += 1
                self.add_line(f'<title>{title}</title>')
                self.add_line('')
                
                i += 1
                continue
            
            # Special callouts
            if line.startswith('::: {.'):
                # Flush paragraph buffer
                if para_buffer:
                    self.process_paragraph(para_buffer)
                    para_buffer = []
                
                # Determine type
                if '.chapterintro' in line:
                    self.add_line('<introduction>')
                    self.indent_level += 1
                elif '.important' in line:
                    self.add_line('<note>')
                    self.indent_level += 1
                    self.add_line('<title>Important</title>')
                elif '.data' in line:
                    self.add_line('<note>')
                    self.indent_level += 1
                    self.add_line('<title>Data</title>')
                elif '.guidedpractice' in line:
                    self.add_line('<exercise>')
                    self.indent_level += 1
                    self.add_line('<title>Guided Practice</title>')
                    self.add_line('<statement>')
                    self.indent_level += 1
                else:
                    self.add_line('<note>')
                    self.indent_level += 1
                
                # Find closing :::
                j = i + 1
                callout_lines = []
                while j < len(lines) and not lines[j].strip().startswith(':::'):
                    callout_lines.append(lines[j].rstrip())
                    j += 1
                
                # Process content
                current_para = []
                for cline in callout_lines:
                    if cline.strip() == '':
                        if current_para:
                            self.process_paragraph(current_para)
                            current_para = []
                    else:
                        current_para.append(cline.strip())
                
                if current_para:
                    self.process_paragraph(current_para)
                
                # Close callout
                if '.guidedpractice' in line:
                    self.indent_level -= 1
                    self.add_line('</statement>')
                    self.add_line('<solution>')
                    self.indent_level += 1
                    self.add_line('<p>Solution to be added.</p>')
                    self.indent_level -= 1
                    self.add_line('</solution>')
                elif '.chapterintro' in line:
                    pass  # Will close at first section
                else:
                    pass
                
                self.indent_level -= 1
                if '.chapterintro' in line:
                    self.add_line('</introduction>')
                elif '.guidedpractice' in line:
                    self.add_line('</exercise>')
                else:
                    self.add_line('</note>')
                self.add_line('')
                
                i = j + 1
                continue
            
            # Empty lines
            if line.strip() == '':
                if para_buffer:
                    self.process_paragraph(para_buffer)
                    para_buffer = []
                i += 1
                continue
            
            # Regular text lines - add to paragraph buffer
            para_buffer.append(line.strip())
            i += 1
        
        # Flush final paragraph
        if para_buffer:
            self.process_paragraph(para_buffer)
        
        # Close any open sections
        if hasattr(self, 'in_section') and self.in_section:
            self.indent_level -= 1
            self.add_line('</section>')
        
        # Close chapter
        self.output.append('</chapter>')
        
        # Write output
        output_file = '/home/runner/work/ims/ims/source/chapters/ch26-inference-logistic-regression.ptx'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"Conversion complete! Output written to {output_file}")

if __name__ == '__main__':
    converter = QmdToPreTeXtConverter()
    converter.convert()
    print("Done!")

#!/usr/bin/env python3
"""
Conversion script for inference-paired-means.qmd to PreTeXt format
"""

import re
import sys

class QmdToPreTeXtConverter:
    def __init__(self):
        self.lines = []
        self.output = []
        self.i = 0
        self.section_stack = []
        self.in_content_visible = False
        self.content_visible_depth = 0
        self.last_code_block = None  # Store last R code block for figures/tables
        
    def convert_file(self, input_file: str, output_file: str):
        """Main conversion function"""
        with open(input_file, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        
        self.output = []
        self.i = 0
        
        # Add XML declaration and section opening
        self.output.append('<?xml version="1.0" encoding="UTF-8"?>')
        self.output.append('<section xml:id="sec-inference-paired-means" xmlns:xi="http://www.w3.org/2001/XInclude">')
        self.output.append('')
        
        # Process all lines
        while self.i < len(self.lines):
            self.process_line()
            self.i += 1
        
        # Close any remaining sections
        while self.section_stack:
            tag = self.section_stack.pop()
            self.output.append(f'</{tag}>')
            self.output.append('')
        
        # Close main section
        self.output.append('</section>')
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"Conversion complete: {len(self.lines)} lines processed")
        print(f"Output written to: {output_file}")
    
    def current_line(self) -> str:
        if self.i < len(self.lines):
            return self.lines[self.i].rstrip()
        return ""
    
    def peek_line(self, offset: int = 1) -> str:
        idx = self.i + offset
        if idx < len(self.lines):
            return self.lines[idx].rstrip()
        return ""
    
    def process_line(self):
        """Process a single line"""
        line = self.current_line()
        
        if not line.strip():
            if not self.in_content_visible:
                self.output.append('')
            return
        
        # Check for content-visible blocks
        if '::: {.content-visible' in line:
            self.in_content_visible = True
            self.content_visible_depth = 1
            return
        
        if self.in_content_visible:
            if line.strip().startswith(':::'):
                if '{' in line:
                    self.content_visible_depth += 1
                else:
                    self.content_visible_depth -= 1
                    if self.content_visible_depth == 0:
                        self.in_content_visible = False
            return
        
        # Skip vspace, clearpage, footnotes
        if (line.strip().startswith(r'\vspace') or 
            line.strip().startswith(r'\clearpage') or
            line.strip().startswith('[^')):
            return
        
        # Display math blocks
        if line.strip() == '$$':
            self.process_display_math()
            return
        
        # Code blocks
        if line.strip().startswith('```'):
            self.process_code_block()
            return
        
        # Headers
        if line.startswith('#') and not line.startswith('#|'):
            self.process_header(line)
            return
        
        # Special blocks
        if line.strip().startswith(':::'):
            self.process_special_block(line)
            return
        
        # Includes
        if '{{< include' in line:
            self.process_include(line)
            return
        
        # Blockquotes
        if line.strip().startswith('>'):
            self.process_blockquote()
            return
        
        # Lists
        if line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line.strip()):
            self.process_list()
            return
        
        # Regular paragraph
        if line.strip():
            self.process_paragraph(line)
    
    def process_header(self, line: str):
        """Process markdown headers"""
        match = re.match(r'^(#{1,4})\s+(.+?)(?:\s+\{#([^}]+)\})?$', line)
        if not match:
            return
        
        hashes, title, xml_id = match.groups()
        level = len(hashes)
        title = self.convert_inline(title)
        
        if level == 1:
            while self.section_stack:
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            self.output.append(f'<title>{title}</title>')
            self.output.append('')
        elif level == 2:
            while self.section_stack and self.section_stack[-1] == 'subsection':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            if self.section_stack and self.section_stack[-1] == 'section':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            if xml_id:
                self.output.append(f'<section xml:id="{xml_id}">')
            else:
                self.output.append('<section>')
            self.output.append(f'  <title>{title}</title>')
            self.output.append('')
            self.section_stack.append('section')
        elif level == 3:
            if self.section_stack and self.section_stack[-1] == 'subsection':
                tag = self.section_stack.pop()
                self.output.append(f'</{tag}>')
                self.output.append('')
            if xml_id:
                self.output.append(f'<subsection xml:id="{xml_id}">')
            else:
                self.output.append('<subsection>')
            self.output.append(f'  <title>{title}</title>')
            self.output.append('')
            self.section_stack.append('subsection')
        elif level == 4:
            # subsubsections - no special structure, just bold
            self.output.append(f'<p><term>{title}</term></p>')
            self.output.append('')
    
    def escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def process_code_block(self):
        """Process R code blocks"""
        self.i += 1
        metadata = {}
        code_lines = []
        current_key = None
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip().startswith('```'):
                break
            
            if line.strip().startswith('#|'):
                content = line.strip()[2:].strip()
                if ':' in content:
                    parts = content.split(':', 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    current_key = key
                    if key in metadata:
                        metadata[key] += ' ' + value
                    else:
                        metadata[key] = value
                else:
                    if current_key and current_key in metadata:
                        metadata[current_key] += ' ' + content
            else:
                code_lines.append(line)
            
            self.i += 1
        
        label = metadata.get('label', '')
        include = metadata.get('include', 'true')
        
        # Skip if include: false
        if include == 'false':
            return
        
        code_text = '\n'.join(code_lines).strip()
        
        # Skip terms definitions
        if 'terms_chp_' in code_text and '=' in code_text:
            return
        
        # Store code for potential figure/table
        self.last_code_block = {
            'label': label,
            'code': code_text,
            'metadata': metadata
        }
        
        # Process figures
        if label.startswith('fig-'):
            fig_cap = metadata.get('fig-cap', '')
            fig_cap = fig_cap.strip('|').strip()
            fig_cap = self.convert_inline(fig_cap)
            
            self.output.append(f'<figure xml:id="{label}">')
            self.output.append(f'  <caption>{fig_cap}</caption>')
            self.output.append(f'  <image source="images/{label}-1.png" width="70%" />')
            self.output.append('</figure>')
            self.output.append('')
            
            # Add R code listing after figure
            if code_text:
                escaped_code = self.escape_xml(code_text)
                self.output.append(f'<listing xml:id="{label}-code">')
                self.output.append(f'  <caption>R code for {label}</caption>')
                self.output.append('  <program language="r">')
                self.output.append('    <input>')
                for code_line in escaped_code.split('\n'):
                    self.output.append(f'{code_line}')
                self.output.append('    </input>')
                self.output.append('  </program>')
                self.output.append('</listing>')
                self.output.append('')
        
        # Process tables
        elif label.startswith('tbl-'):
            tbl_cap = metadata.get('tbl-cap', '')
            tbl_cap = tbl_cap.strip('|').strip()
            tbl_cap = self.convert_inline(tbl_cap)
            
            self.output.append(f'<table xml:id="{label}">')
            self.output.append(f'  <title>{tbl_cap}</title>')
            self.output.append(f'  <image source="images/{label}-1.png" width="70%" />')
            self.output.append('</table>')
            self.output.append('')
            
            # Add R code listing after table
            if code_text:
                escaped_code = self.escape_xml(code_text)
                self.output.append(f'<listing xml:id="{label}-code">')
                self.output.append(f'  <caption>R code for {label}</caption>')
                self.output.append('  <program language="r">')
                self.output.append('    <input>')
                for code_line in escaped_code.split('\n'):
                    self.output.append(f'{code_line}')
                self.output.append('    </input>')
                self.output.append('  </program>')
                self.output.append('</listing>')
                self.output.append('')
    
    def process_special_block(self, line: str):
        """Process special blocks"""
        if '.guidedpractice' in line:
            self.process_guided_practice()
        elif '.workedexample' in line:
            self.process_worked_example()
        elif '.data' in line:
            self.process_data_block()
        elif '.important' in line:
            self.process_important_block()
        elif '.chapterintro' in line:
            self.process_chapterintro()
        elif '.onebox' in line:
            self.process_onebox()
        elif '.exercises' in line:
            self.process_exercises_block()
        elif '.pronunciation' in line:
            self.skip_until_closing_fence()
        else:
            self.skip_until_closing_fence()
    
    def process_chapterintro(self):
        """Process chapter introduction"""
        self.i += 1
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            if line.strip():
                content_lines.append(line)
            self.i += 1
        
        self.output.append('<introduction>')
        for line in content_lines:
            if line.strip():
                converted = self.convert_inline(line.strip())
                self.output.append(f'  <p>{converted}</p>')
        self.output.append('</introduction>')
        self.output.append('')
    
    def process_important_block(self):
        """Process important block"""
        self.i += 1
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            if line.strip():
                content_lines.append(line)
            self.i += 1
        
        self.output.append('<note>')
        for line in content_lines:
            if line.strip() and not line.strip().startswith(r'\index'):
                converted = self.convert_inline(line.strip())
                if line.strip().startswith('**') and line.strip().endswith('**'):
                    self.output.append(f'  <title>{converted}</title>')
                else:
                    self.output.append(f'  <p>{converted}</p>')
        self.output.append('</note>')
        self.output.append('')
    
    def process_onebox(self):
        """Process onebox block"""
        self.i += 1
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            if line.strip():
                content_lines.append(line)
            self.i += 1
        
        self.output.append('<assemblage>')
        for line in content_lines:
            if line.strip():
                converted = self.convert_inline(line.strip())
                if line.strip().startswith('**') and line.strip().endswith('**'):
                    self.output.append(f'  <title>{converted}</title>')
                else:
                    self.output.append(f'  <p>{converted}</p>')
        self.output.append('</assemblage>')
        self.output.append('')
    
    def process_exercises_block(self):
        """Process exercises block - extract includes"""
        self.i += 1
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            
            # Check for include directive
            if '{{< include' in line:
                match = re.search(r'\{\{<\s*include\s+([^>]+)\s*>\}\}', line)
                if match:
                    include_file = match.group(1).strip()
                    self.output.append(f'<xi:include href="{include_file}" />')
                    self.output.append('')
            
            self.i += 1
    
    def process_guided_practice(self):
        """Process guided practice"""
        self.i += 1
        title_line = self.current_line()
        self.i += 1
        
        statement_lines = []
        solution_lines = []
        in_solution = False
        depth = 1  # We're already inside the .guidedpractice block
        
        while self.i < len(self.lines):
            line = self.current_line()
            
            # Check for nested blocks
            if line.strip().startswith(':::'):
                if '{' in line:
                    # Opening a nested block
                    if '.callout-note' in line:
                        in_solution = True
                    depth += 1
                else:
                    # Closing a block
                    depth -= 1
                    if depth == 0:
                        # We've closed the guidedpractice block
                        break
                    if in_solution and depth == 1:
                        # Closed the solution block
                        in_solution = False
                self.i += 1
                continue
            
            # Process content
            if in_solution:
                if line.strip() and not line.strip().startswith('##'):
                    solution_lines.append(line)
            elif line.strip():
                statement_lines.append(line)
            
            self.i += 1
        
        self.output.append('<exercise>')
        self.output.append(f'  <title>{self.convert_inline(title_line.strip())}</title>')
        self.output.append('  <statement>')
        for line in statement_lines:
            if line.strip():
                self.output.append(f'    <p>{self.convert_inline(line.strip())}</p>')
        self.output.append('  </statement>')
        if solution_lines:
            self.output.append('  <solution>')
            for line in solution_lines:
                if line.strip():
                    self.output.append(f'    <p>{self.convert_inline(line.strip())}</p>')
            self.output.append('  </solution>')
        self.output.append('</exercise>')
        self.output.append('')
    
    def process_worked_example(self):
        """Process worked example"""
        self.i += 1
        content_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == ':::':
                break
            
            # Skip code blocks
            if line.strip().startswith('```'):
                self.i += 1
                while self.i < len(self.lines):
                    if self.current_line().strip().startswith('```'):
                        break
                    self.i += 1
                self.i += 1
                continue
            
            # Handle display math
            if line.strip() == '$$':
                self.i += 1
                math_lines = []
                while self.i < len(self.lines):
                    if self.current_line().strip() == '$$':
                        break
                    math_lines.append(self.current_line())
                    self.i += 1
                if math_lines:
                    content_lines.append(('math', '\n'.join(math_lines).strip()))
                self.i += 1
                continue
            
            if line.strip():
                content_lines.append(('text', line))
            self.i += 1
        
        self.output.append('<example>')
        for content_type, line in content_lines:
            if content_type == 'text':
                # Strip trailing backslashes (LaTeX line continuations)
                text = line.strip().rstrip('\\').strip()
                converted = self.convert_inline(text)
                self.output.append(f'  <p>{converted}</p>')
            elif content_type == 'math':
                self.output.append(f'  <me><![CDATA[')
                self.output.append(f'{line}')
                self.output.append(f'  ]]></me>')
        self.output.append('</example>')
        self.output.append('')
    
    def process_data_block(self):
        """Process data block"""
        self.skip_until_closing_fence()
    
    def skip_until_closing_fence(self):
        """Skip until closing ::: fence"""
        depth = 1
        self.i += 1
        
        while self.i < len(self.lines) and depth > 0:
            line = self.current_line()
            if line.strip().startswith(':::'):
                if '{' in line:
                    depth += 1
                else:
                    depth -= 1
            self.i += 1
        self.i -= 1
    
    def process_display_math(self):
        """Process display math block"""
        self.i += 1
        math_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if line.strip() == '$$':
                break
            math_lines.append(line)
            self.i += 1
        
        math_text = '\n'.join(math_lines).strip()
        self.output.append('<me><![CDATA[')
        self.output.append(math_text)
        self.output.append(']]></me>')
        self.output.append('')
    
    def process_include(self, line: str):
        """Process include directive"""
        match = re.search(r'\{\{<\s*include\s+([^>]+)\s*>\}\}', line)
        if match:
            include_file = match.group(1).strip()
            self.output.append(f'<xi:include href="{include_file}" />')
            self.output.append('')
    
    def process_list(self):
        """Process markdown list"""
        list_lines = []
        is_ordered = re.match(r'^\d+\.\s', self.current_line().strip())
        
        while self.i < len(self.lines):
            line = self.current_line()
            if not line.strip():
                break
            if not (line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line.strip())):
                break
            list_lines.append(line)
            self.i += 1
        self.i -= 1
        
        tag = 'ol' if is_ordered else 'ul'
        self.output.append(f'<{tag}>')
        
        for line in list_lines:
            # Remove list marker
            text = re.sub(r'^[\-\*\+]|\d+\.', '', line.strip(), count=1).strip()
            converted = self.convert_inline(text)
            self.output.append(f'  <li><p>{converted}</p></li>')
        
        self.output.append(f'</{tag}>')
        self.output.append('')
    
    def process_blockquote(self):
        """Process blockquote (lines starting with >)"""
        quote_lines = []
        
        while self.i < len(self.lines):
            line = self.current_line()
            if not line.strip().startswith('>'):
                break
            # Remove the > and any leading space
            text = line.strip()[1:].strip()
            if text:
                quote_lines.append(text)
            self.i += 1
        self.i -= 1
        
        if quote_lines:
            self.output.append('<blockquote>')
            text = ' '.join(quote_lines)
            converted = self.convert_inline(text)
            self.output.append(f'  <p>{converted}</p>')
            self.output.append('</blockquote>')
            self.output.append('')
    
    def process_paragraph(self, line: str):
        """Process a paragraph"""
        para_lines = [line]
        
        while self.i + 1 < len(self.lines):
            next_line = self.peek_line()
            if not next_line.strip():
                break
            if (next_line.startswith('#') or 
                next_line.strip().startswith('```') or
                next_line.strip().startswith(':::') or
                next_line.strip().startswith(('- ', '* ', '+ ', '>')) or
                re.match(r'^\d+\.\s', next_line.strip()) or
                next_line.strip() == '$$' or
                '{{< include' in next_line):
                break
            self.i += 1
            para_lines.append(next_line)
        
        text = ' '.join(line.strip() for line in para_lines if line.strip())
        converted = self.convert_inline(text)
        self.output.append(f'<p>{converted}</p>')
        self.output.append('')
    
    def convert_inline(self, text: str) -> str:
        """Convert inline markdown to PreTeXt"""
        # Chapter references with -@sec- (must come before general cross-references)
        text = re.sub(r'\[Chapter -@(sec-[^\]]+)\]', r'<xref ref="\1" />', text)
        
        # Appendix references with -@sec-
        text = re.sub(r'\[Appendix -@(sec-[^\]]+)\]', r'<xref ref="\1" />', text)
        
        # Section references
        text = re.sub(r'\[Section @(sec-[^\]]+)\]', r'<xref ref="\1" />', text)
        
        # Table/Figure references in (see @tbl-... ) format
        text = re.sub(r'\(see @([a-z]+-[a-z0-9\-]+)\)', r'(see <xref ref="\1" />)', text)
        
        # General cross-references @tbl-xxx, @fig-xxx
        text = re.sub(r'@([a-z]+-[a-z0-9\-]+)', r'<xref ref="\1" />', text)
        
        # Bold
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<term>\1</term>', text)
        
        # Italic
        text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
        
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
        
        # Inline math
        text = re.sub(r'\$([^\$]+)\$', r'<m>\1</m>', text)
        
        return text


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_inference_paired_means.py <input.qmd> <output.ptx>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    converter = QmdToPreTeXtConverter()
    converter.convert_file(input_file, output_file)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Complete converter for explore-numerical.qmd to PreTeXt XML format.
Handles all 1449 lines systematically with proper structure.
"""

import re
import sys
from typing import List, Tuple, Optional

class PreTeXtConverter:
    def __init__(self):
        self.lines = []
        self.output = []
        self.current_line = 0
        self.in_code_block = False
        self.in_callout = False
        self.section_stack = []  # Track open sections/subsections
        
    def read_file(self, filename: str):
        """Read the input file."""
        with open(filename, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
    
    def write_file(self, filename: str):
        """Write the output file."""
        content = '\n'.join(self.output)
        # Clean up excessive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def peek_line(self, offset=0) -> Optional[str]:
        """Peek at a line without consuming it."""
        idx = self.current_line + offset
        if idx < len(self.lines):
            return self.lines[idx].rstrip()
        return None
    
    def consume_line(self) -> Optional[str]:
        """Consume and return the current line."""
        if self.current_line < len(self.lines):
            line = self.lines[self.current_line].rstrip()
            self.current_line += 1
            return line
        return None
    
    def skip_lines(self, count: int):
        """Skip ahead by count lines."""
        self.current_line += count
    
    def close_sections_to_level(self, level: int):
        """Close all sections at or above the given level."""
        while self.section_stack and self.section_stack[-1] >= level:
            tag = 'subsection' if self.section_stack[-1] == 3 else 'section'
            self.output.append(f'</{tag}>')
            self.output.append('')
            self.section_stack.pop()
    
    def format_inline(self, text: str) -> str:
        """Format inline text elements."""
        if not text:
            return text
        
        # Check if this text is ONLY display math ($$...$$)
        display_math_only = re.match(r'^\s*\$\$.*\$\$\s*$', text, flags=re.DOTALL)
        
        # Protect math content ($$...$$ and $...$) BEFORE any processing
        math_placeholders = []
        display_math_positions = []
        def save_math(match):
            idx = len(math_placeholders)
            math_placeholders.append(match.group(0))
            if match.group(0).startswith('$$'):
                display_math_positions.append(idx)
            return f'ĦMATHŦ{idx}ĦENDŦ'
        # Protect display math first
        text = re.sub(r'\$\$.*?\$\$', save_math, text, flags=re.DOTALL)
        # Then inline math
        text = re.sub(r'\$[^\$]+?\$', save_math, text)
        
        # Replace r nrow values (outside of math)
        text = text.replace('`r nrow(loan50)`', '50')
        text = text.replace('`r nrow(county)`', '3142')
        text = text.replace('`r round(loan50_interest_rate_mean, 2)`', '11.57')
        
        # Remove footnote markers ^[...]
        text = re.sub(r'\^\[([^\]]+)\]', '', text)
        
        # Remove standalone \index{...} commands (not following bold)
        text = re.sub(r'\\index\{[^}]*\}', '', text)
        
        # Handle **bold**\index{term} -> <term>text</term><idx>text</idx>
        text = re.sub(r'\*\*([^*]+?)\*\*\\index\{([^}]*)\}', 
                     lambda m: f'<term>{m.group(1)}</term><idx>{m.group(2) if m.group(2) else m.group(1)}</idx>', 
                     text)
        
        # Handle **bold** alone -> <alert>text</alert>
        text = re.sub(r'\*\*([^*]+?)\*\*', r'<alert>\1</alert>', text)
        
        # Handle *italic* -> <em>text</em>
        text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
        
        # Handle `code` -> <c>code</c>
        text = re.sub(r'`([^`]+?)`', r'<c>\1</c>', text)
        
        # Handle [link text](url) -> use unique placeholder
        url_placeholders = []
        def save_url(match):
            url_placeholders.append((match.group(2), match.group(1)))
            return f'ĦURLŦ{len(url_placeholders)-1}ĦENDŦ'
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', save_url, text)
        
        # Handle cross-references with placeholders
        xref_placeholders = []
        def save_xref(match):
            xref_placeholders.append((match.group(1), match.group(2)))
            return f'ĦXREFŦ{len(xref_placeholders)-1}ĦENDŦ'
        text = re.sub(r'@(fig|sec|tbl)-([a-zA-Z0-9-]+)', save_xref, text)
        
        # Clean up XML entities (but NOT in our placeholders which use special chars)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        
        # Now restore our XML tags
        text = text.replace('&lt;term&gt;', '<term>').replace('&lt;/term&gt;', '</term>')
        text = text.replace('&lt;idx&gt;', '<idx>').replace('&lt;/idx&gt;', '</idx>')
        text = text.replace('&lt;alert&gt;', '<alert>').replace('&lt;/alert&gt;', '</alert>')
        text = text.replace('&lt;em&gt;', '<em>').replace('&lt;/em&gt;', '</em>')
        text = text.replace('&lt;c&gt;', '<c>').replace('&lt;/c&gt;', '</c>')
        
        # Restore URLs from placeholders
        for i, (href, link_text) in enumerate(url_placeholders):
            text = text.replace(f'ĦURLŦ{i}ĦENDŦ', f'<url href="{href}">{link_text}</url>')
        
        # Restore xrefs from placeholders
        for i, (ref_type, ref_id) in enumerate(xref_placeholders):
            text = text.replace(f'ĦXREFŦ{i}ĦENDŦ', f'<xref ref="{ref_type}-{ref_id}" />')
        
        # Restore math content wrapped in CDATA for display math
        for i, math_content in enumerate(math_placeholders):
            if i in display_math_positions:
                # Strip the $$ markers and wrap in CDATA
                math_inner = math_content[2:-2].strip()  # Remove $$ from both ends
                text = text.replace(f'ĦMATHŦ{i}ĦENDŦ', f'<![CDATA[{math_inner}]]>')
            else:
                # Inline math - keep as is
                text = text.replace(f'ĦMATHŦ{i}ĦENDŦ', math_content)
        
        return text
    
    def extract_fig_caption(self, start_line: int) -> Tuple[Optional[str], int]:
        """Extract multi-line fig-cap from a code block."""
        caption_lines = []
        i = start_line
        in_caption = False
        
        while i < len(self.lines):
            line = self.lines[i].rstrip()
            
            if '#| fig-cap: |' in line:
                in_caption = True
                i += 1
                continue
            
            if in_caption:
                if line.startswith('#|   ') or line.startswith('#|    '):
                    # Caption continuation
                    caption_lines.append(line[5:].strip())
                    i += 1
                elif line.startswith('#|') and not line.startswith('#|   '):
                    # Next directive, end of caption
                    break
                elif line == '```':
                    # End of code block
                    break
                else:
                    i += 1
            else:
                if line == '```':
                    break
                i += 1
        
        if caption_lines:
            caption = ' '.join(caption_lines)
            return self.format_inline(caption), i
        return None, i
    
    def handle_code_block(self) -> bool:
        """Handle R code blocks, extracting figures where appropriate."""
        start = self.current_line
        line = self.consume_line()
        
        # Skip setup blocks
        if self.peek_line() and '#| include: false' in self.peek_line():
            while self.current_line < len(self.lines):
                line = self.consume_line()
                if line == '```':
                    return True
            return True
        
        # Look for #| label: fig-
        fig_label = None
        i = self.current_line
        while i < len(self.lines) and i < self.current_line + 20:
            if self.lines[i].startswith('#| label: fig-'):
                fig_label = self.lines[i].split('fig-')[1].strip()
                break
            if self.lines[i].startswith('#| label: tbl-'):
                # Skip table blocks
                while self.current_line < len(self.lines):
                    if self.consume_line() == '```':
                        return True
                return True
            if self.lines[i] == '```':
                break
            i += 1
        
        if fig_label:
            # Extract caption
            caption, _ = self.extract_fig_caption(self.current_line)
            
            # Skip to end of code block
            while self.current_line < len(self.lines):
                if self.consume_line() == '```':
                    break
            
            # Output figure
            if caption:
                self.output.append(f'<figure xml:id="fig-{fig_label}">')
                self.output.append(f'  <caption>{caption}</caption>')
                self.output.append(f'  <image source="images/explore-numerical/fig-{fig_label}-1.png" width="70%" />')
                self.output.append('</figure>')
                self.output.append('')
            return True
        
        # Skip non-figure code blocks
        while self.current_line < len(self.lines):
            if self.consume_line() == '```':
                return True
        return True
    
    def handle_workedexample(self) -> bool:
        """Handle worked example blocks."""
        self.consume_line()  # consume ::: {.workedexample
        
        statement_lines = []
        solution_lines = []
        in_solution = False
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line == ':::':
                self.consume_line()
                break
            
            if line and line.strip() == '------------------------------------------------------------------------':
                in_solution = True
                self.consume_line()
                continue
            
            self.consume_line()
            
            if line:
                if in_solution:
                    solution_lines.append(line)
                else:
                    statement_lines.append(line)
        
        # Output example
        self.output.append('<example>')
        self.output.append('  <statement>')
        
        stmt_text = ' '.join(statement_lines).strip()
        if stmt_text:
            self.output.append(f'    <p>{self.format_inline(stmt_text)}</p>')
        
        self.output.append('  </statement>')
        self.output.append('  <solution>')
        
        sol_text = ' '.join(solution_lines).strip()
        if sol_text:
            self.output.append(f'    <p>{self.format_inline(sol_text)}</p>')
        
        self.output.append('  </solution>')
        self.output.append('</example>')
        self.output.append('')
        
        return True
    
    def handle_guidedpractice(self) -> bool:
        """Handle guided practice blocks."""
        self.consume_line()  # consume ::: {.guidedpractice
        
        statement_lines = []
        solution_lines = []
        in_solution = False
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line == ':::' and in_solution:
                # End of nested callout
                self.consume_line()
                in_solution = False
                continue
            
            if line == ':::' and not in_solution:
                # End of guidedpractice
                self.consume_line()
                break
            
            if line and line.startswith('::: {.callout-note'):
                # Start of solution
                in_solution = True
                self.consume_line()
                continue
            
            self.consume_line()
            
            if line:
                # Skip "## Solution" and "## Answer" headings inside blocks
                if line.strip() in ['## Solution', '## Answer']:
                    continue
                    
                if in_solution:
                    solution_lines.append(line)
                else:
                    statement_lines.append(line)
        
        # Output exercise
        self.output.append('<exercise>')
        self.output.append('  <statement>')
        
        stmt_text = ' '.join(statement_lines).strip()
        if stmt_text:
            self.output.append(f'    <p>{self.format_inline(stmt_text)}</p>')
        
        self.output.append('  </statement>')
        
        if solution_lines:
            self.output.append('  <solution>')
            sol_text = ' '.join(solution_lines).strip()
            if sol_text:
                self.output.append(f'    <p>{self.format_inline(sol_text)}</p>')
            self.output.append('  </solution>')
        
        self.output.append('</exercise>')
        self.output.append('')
        
        return True
    
    def handle_important_block(self) -> bool:
        """Handle important blocks."""
        self.consume_line()  # consume ::: {.important
        
        content_lines = []
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line == ':::':
                self.consume_line()
                break
            
            self.consume_line()
            
            if line:
                content_lines.append(line)
        
        # Extract first bold text as title
        content_text = ' '.join(content_lines).strip()
        title_match = re.search(r'\*\*([^*]+?)\*\*', content_text)
        
        if title_match:
            title = title_match.group(1)
            # Remove the title from content - get everything after the title
            content_text = content_text[title_match.end():].strip()
            # Remove any standalone \index{} that comes right after
            content_text = re.sub(r'^\\index\{[^}]*\}\s*', '', content_text)
            # Remove leading colon and period if present
            content_text = re.sub(r'^[:.]\s*', '', content_text)
        
        self.output.append('<assemblage>')
        if title:
            self.output.append(f'  <title>{self.format_inline(title)}</title>')
        
        if content_text:
            self.output.append(f'  <p>{self.format_inline(content_text)}</p>')
        
        self.output.append('</assemblage>')
        self.output.append('')
        
        return True
    
    def handle_data_block(self) -> bool:
        """Handle data blocks."""
        self.consume_line()  # consume ::: {.data
        
        content_lines = []
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line == ':::':
                self.consume_line()
                break
            
            self.consume_line()
            
            if line:
                content_lines.append(line)
        
        content_text = ' '.join(content_lines).strip()
        
        self.output.append('<note>')
        self.output.append('  <title>Data</title>')
        if content_text:
            self.output.append(f'  <p>{self.format_inline(content_text)}</p>')
        self.output.append('</note>')
        self.output.append('')
        
        return True
    
    def handle_chapterintro(self) -> bool:
        """Handle chapter intro block."""
        self.consume_line()  # consume ::: {.chapterintro
        
        content_lines = []
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line == ':::':
                self.consume_line()
                break
            
            self.consume_line()
            
            if line:
                content_lines.append(line)
        
        self.output.append('<introduction>')
        
        for line in content_lines:
            line = line.strip()
            if line:
                self.output.append(f'  <p>{self.format_inline(line)}</p>')
        
        self.output.append('</introduction>')
        self.output.append('')
        
        return True
    
    def handle_list(self) -> bool:
        """Handle bullet and numbered lists."""
        first_line = self.peek_line()
        
        # Determine list type
        is_ordered = bool(re.match(r'^\d+\.', first_line.strip()))
        tag = 'ol' if is_ordered else 'ul'
        
        self.output.append(f'<{tag}>')
        
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if not line:
                break
            
            # Check if it's a list item
            if is_ordered:
                match = re.match(r'^\d+\.\s+(.+)$', line.strip())
            else:
                match = re.match(r'^-\s+(.+)$', line.strip())
            
            if match:
                self.consume_line()
                content = match.group(1)
                self.output.append(f'  <li><p>{self.format_inline(content)}</p></li>')
            else:
                # End of list
                break
        
        self.output.append(f'</{tag}>')
        self.output.append('')
        
        return True
    
    def handle_section(self) -> bool:
        """Handle section headings."""
        line = self.consume_line()
        
        # Determine level
        if line.startswith('###'):
            level = 3
            title_part = line[3:].strip()
        elif line.startswith('##'):
            level = 2
            title_part = line[2:].strip()
        else:
            return False
        
        # Extract title and ID
        match = re.match(r'(.+?)\s+\{#([^}]+)\}', title_part)
        if match:
            title = match.group(1).strip()
            xml_id = match.group(2)
        else:
            title = title_part
            xml_id = title.lower().replace(' ', '-')
        
        # Close sections as needed
        self.close_sections_to_level(level)
        
        # Open new section
        tag = 'subsection' if level == 3 else 'section'
        self.output.append(f'<{tag} xml:id="{xml_id}">')
        self.output.append(f'  <title>{self.format_inline(title)}</title>')
        self.output.append('')
        
        self.section_stack.append(level)
        
        return True
    
    def handle_paragraph(self, line: str) -> bool:
        """Handle regular paragraph text."""
        # Accumulate paragraph lines
        para_lines = [line]
        
        while self.current_line < len(self.lines):
            next_line = self.peek_line()
            
            if not next_line:
                # Blank line ends paragraph
                self.consume_line()
                break
            
            # Check if next line starts a new block
            if (next_line.startswith('#') or 
                next_line.startswith('```') or 
                next_line.startswith(':::') or
                re.match(r'^-\s+', next_line) or
                re.match(r'^\d+\.', next_line)):
                break
            
            self.consume_line()
            para_lines.append(next_line)
        
        # Output paragraph
        para_text = ' '.join(para_lines).strip()
        if para_text:
            self.output.append(f'<p>{self.format_inline(para_text)}</p>')
            self.output.append('')
        
        return True
    
    def convert(self):
        """Main conversion logic."""
        # XML declaration
        self.output.append('<?xml version="1.0" encoding="UTF-8"?>')
        self.output.append('<chapter xml:id="ch05-exploring-numerical" xmlns:xi="http://www.w3.org/2001/XInclude">')
        self.output.append('')
        
        # Process first line (chapter title)
        title_line = self.consume_line()
        if title_line.startswith('#'):
            match = re.match(r'#\s+(.+?)\s+\{#([^}]+)\}', title_line)
            if match:
                title = match.group(1)
                self.output.append(f'<title>{self.format_inline(title)}</title>')
                self.output.append('')
        
        # Process all lines
        while self.current_line < len(self.lines):
            line = self.peek_line()
            
            if line is None:
                break
            
            # Skip empty lines
            if not line:
                self.consume_line()
                continue
            
            # Skip specific patterns
            if (line.startswith('terms_chp_05') or 
                line.startswith('\\vspace') or 
                line.startswith('\\clearpage') or
                '::: {.pronunciation}' in line or
                '::: {.content-visible' in line):
                self.consume_line()
                # Skip until end of block if it's a ::: block
                if line.startswith(':::'):
                    while self.current_line < len(self.lines):
                        if self.consume_line() == ':::':
                            break
                continue
            
            # Handle code blocks
            if line.startswith('```{r}'):
                self.handle_code_block()
                continue
            
            # Handle special blocks
            if line.startswith('::: {.chapterintro'):
                self.handle_chapterintro()
                continue
            
            if line.startswith('::: {.workedexample'):
                self.handle_workedexample()
                continue
            
            if line.startswith('::: {.guidedpractice'):
                self.handle_guidedpractice()
                continue
            
            if line.startswith('::: {.important'):
                self.handle_important_block()
                continue
            
            if line.startswith('::: {.data'):
                self.handle_data_block()
                continue
            
            # Skip exercises include
            if line.startswith('::: {.exercises'):
                while self.current_line < len(self.lines):
                    if self.consume_line() == ':::':
                        break
                continue
            
            # Handle sections
            if line.startswith('##'):
                # Check if this is inside a block (e.g., "## Solution")
                # We skip those by context, but generally ## at start of line is a section
                if line.startswith('### '):
                    self.handle_section()
                    continue
                elif line.startswith('## '):
                    # Check if it's Chapter review section
                    if 'Chapter review' in line:
                        self.close_sections_to_level(2)
                        self.output.append('<section xml:id="sec-chp5-review">')
                        self.output.append('  <title>Chapter review</title>')
                        self.output.append('')
                        self.section_stack.append(2)
                        self.consume_line()
                        continue
                    elif 'Exercises' in line and '#sec-chp5-exercises' in line:
                        self.close_sections_to_level(2)
                        self.output.append('<section xml:id="sec-chp5-exercises">')
                        self.output.append('  <title>Exercises</title>')
                        self.output.append('')
                        self.section_stack.append(2)
                        self.consume_line()
                        
                        # Process content until end
                        para_lines = []
                        while self.current_line < len(self.lines):
                            next_line = self.peek_line()
                            if not next_line:
                                self.consume_line()
                                continue
                            if next_line.startswith('##'):
                                break
                            if next_line.startswith(':::'):
                                # Skip exercises block content
                                self.consume_line()
                                while self.current_line < len(self.lines):
                                    if self.consume_line() == ':::':
                                        break
                                continue
                            # Collect text
                            self.consume_line()
                            if next_line.strip():
                                para_lines.append(next_line.strip())
                        
                        # Output collected paragraphs
                        if para_lines:
                            for para in para_lines:
                                self.output.append(f'  <p>{self.format_inline(para)}</p>')
                        
                        # Close exercises section
                        self.close_sections_to_level(2)
                        continue
                    else:
                        self.handle_section()
                        continue
            
            # Handle lists
            if re.match(r'^-\s+', line) or re.match(r'^\d+\.', line):
                self.handle_list()
                continue
            
            # Handle regular paragraph
            self.consume_line()
            self.handle_paragraph(line)
        
        # Close any remaining sections
        self.close_sections_to_level(1)
        
        # Close chapter
        self.output.append('</chapter>')

def main():
    converter = PreTeXtConverter()
    
    input_file = '/home/runner/work/ims/ims/explore-numerical.qmd'
    output_file = '/home/runner/work/ims/ims/source/chapters/ch05-exploring-numerical.ptx'
    
    print(f"Reading {input_file}...")
    converter.read_file(input_file)
    
    print(f"Converting {len(converter.lines)} lines...")
    converter.convert()
    
    print(f"Writing {output_file}...")
    converter.write_file(output_file)
    
    print(f"Conversion complete! Generated {len(converter.output)} output lines.")

if __name__ == '__main__':
    main()

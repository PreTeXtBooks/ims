#!/usr/bin/env python3
"""
Conversion script for Ch20 exercises from Quarto to PreTeXt format
Converts exercises/_20-ex-inference-two-means.qmd to PTX format
"""

import re
import sys

class ExerciseConverter:
    def __init__(self):
        self.lines = []
        self.output = []
        self.i = 0
        self.current_exercise_num = 0
        
    def convert_file(self, input_file: str, solutions_file: str, output_file: str):
        """Main conversion function"""
        # Read exercises
        with open(input_file, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        
        # Read solutions
        solutions = []
        with open(solutions_file, 'r', encoding='utf-8') as f:
            solutions = f.readlines()
        
        # Parse solutions into a dict
        self.solutions = self.parse_solutions(solutions)
        
        self.output = []
        self.i = 0
        self.current_exercise_num = 0
        
        # Add XML declaration and exercises opening
        self.output.append('<?xml version="1.0" encoding="UTF-8" ?>')
        self.output.append('')
        self.output.append('<exercises xml:id="exercises-20-inference-two-means">')
        self.output.append('')
        
        # Skip YAML header
        if self.current_line().strip() == '---':
            self.i += 1
            while self.i < len(self.lines) and self.current_line().strip() != '---':
                self.i += 1
            self.i += 1  # Skip closing ---
        
        # Process all lines
        while self.i < len(self.lines):
            self.process_line()
            self.i += 1
        
        # Close exercises
        self.output.append('</exercises>')
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"Conversion complete: {self.current_exercise_num} exercises processed")
        print(f"Output written to: {output_file}")
    
    def parse_solutions(self, lines):
        """Parse the solutions file into a dict keyed by exercise number"""
        solutions_dict = {}
        current_exercise_num = 1  # Start at exercise 1
        current_text = []
        
        for line in lines:
            # Match "1. " pattern (always means next odd exercise in sequence)
            if re.match(r'^1\.\s+', line):
                # Save previous exercise if exists
                if current_text:
                    solutions_dict[current_exercise_num] = ''.join(current_text).strip()
                    current_text = []
                
                # Start new solution
                current_text.append(re.sub(r'^1\.\s+', '', line))
            elif line.strip().startswith(r'\addtocounter{enumi}{1}'):
                # Save previous exercise
                if current_text:
                    solutions_dict[current_exercise_num] = ''.join(current_text).strip()
                    current_text = []
                # Move to next odd exercise (skip the even one)
                current_exercise_num += 2
            elif current_exercise_num >= 1:
                current_text.append(line)
        
        # Save last exercise
        if current_text:
            solutions_dict[current_exercise_num] = ''.join(current_text).strip()
        
        return solutions_dict
    
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
        """Process a single line looking for exercise starts"""
        line = self.current_line()
        
        # Check for exercise start (numbered list item)
        match = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)$', line)
        if match:
            self.current_exercise_num = int(match.group(1))
            title = match.group(2).strip()
            first_sentence = match.group(3).strip()
            self.process_exercise(title, first_sentence)
            return
    
    def process_exercise(self, title, first_sentence):
        """Process a complete exercise"""
        self.output.append(f'  <exercise>')
        self.output.append(f'    <title>{self.convert_inline(title)}</title>')
        self.output.append(f'    <statement>')
        
        # Collect exercise content
        content_lines = []
        if first_sentence:
            content_lines.append(first_sentence)
        
        self.i += 1
        
        # Read until we hit next exercise or end
        while self.i < len(self.lines):
            line = self.current_line()
            
            # Check if this is the start of next exercise
            if re.match(r'^\d+\.\s+\*\*', line):
                self.i -= 1  # Back up so main loop can process it
                break
            
            # Skip footnote references at end
            if line.strip().startswith('[^_20-ex-inference-two-means'):
                self.i += 1
                continue
            
            # Skip page breaks and vspace commands
            if line.strip() in [r'\clearpage', r'\vfill'] or line.strip().startswith(r'\vspace'):
                self.i += 1
                continue
            
            content_lines.append(line)
            self.i += 1
        
        # Process the content
        self.output_content(content_lines, '      ')
        
        self.output.append(f'    </statement>')
        
        # Add solution if available (odd-numbered exercises only)
        if self.current_exercise_num in self.solutions:
            solution_text = self.solutions[self.current_exercise_num]
            self.output.append(f'    <solution>')
            self.output_solution(solution_text, '      ')
            self.output.append(f'    </solution>')
        
        self.output.append(f'  </exercise>')
        self.output.append('')
    
    def output_content(self, lines, indent):
        """Process and output content lines"""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Skip LaTeX commands
            if line.startswith(r'\vspace') or line.startswith(r'\clearpage'):
                i += 1
                continue
            
            # Check for code block
            if line.startswith('```'):
                i += 1
                code_lines = []
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # Skip closing ```
                
                # Output as figure (for R code that generates plots)
                # We just skip the code for now as it generates images
                continue
            
            # Check for display math
            if line == '$$':
                i += 1
                math_lines = []
                while i < len(lines) and lines[i].strip() != '$$':
                    math_lines.append(lines[i].rstrip())
                    i += 1
                i += 1  # Skip closing $$
                
                if math_lines:
                    math_content = '\n'.join(math_lines)
                    # Convert & to \amp for PreTeXt
                    math_content = re.sub(r'(?<!\\)&', r'\\amp', math_content)
                    self.output.append(f'{indent}<me>')
                    self.output.append(math_content)
                    self.output.append(f'{indent}</me>')
                continue
            
            # Check for sub-parts (a., b., c., etc.)
            if re.match(r'^\s*[a-z]\.\s+', line):
                # Start an ordered list - collect all sub-parts
                list_items = []
                while i < len(lines):
                    line = lines[i].strip()
                    
                    # Skip blank lines and LaTeX commands between sub-parts
                    if not line or line.startswith(r'\vspace') or line.startswith(r'\clearpage'):
                        i += 1
                        continue
                    
                    match = re.match(r'^([a-z])\.\s+(.+)$', line)
                    if match:
                        list_items.append(self.convert_inline(match.group(2)))
                        i += 1
                    elif line and not line.startswith('```') and not line == '$$' and not re.match(r'^\d+\.\s+\*\*', line):
                        # Continuation of previous item
                        if list_items:
                            list_items[-1] += ' ' + self.convert_inline(line)
                        i += 1
                    else:
                        break
                
                # Only output the list once with all items
                if list_items:
                    self.output.append(f'{indent}<p><ol marker="a.">')
                    for item in list_items:
                        self.output.append(f'{indent}  <li>{item}</li>')
                    self.output.append(f'{indent}</ol></p>')
                continue
            
            # Regular paragraph - collect multi-line
            para_lines = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if (not next_line or 
                    next_line.startswith('```') or 
                    next_line == '$$' or
                    re.match(r'^[a-z]\.\s+', next_line)):
                    break
                para_lines.append(next_line)
                i += 1
            
            para_text = ' '.join(para_lines)
            processed = self.convert_inline(para_text)
            self.output.append(f'{indent}<p>{processed}</p>')
        
    def output_solution(self, solution_text, indent):
        """Output solution content"""
        # Normalize \( and \) to ( and ) first
        solution_text = re.sub(r'\\[(]', '(', solution_text)
        solution_text = re.sub(r'\\[)]', ')', solution_text)
        
        # Split into parts if it contains sub-parts like (a), (b), etc.
        parts = re.split(r'\s*[(]([a-z])[)]\s*', solution_text)
        
        if len(parts) > 1:
            # Has sub-parts - remove leading text before first part
            self.output.append(f'{indent}<p><ol marker="a.">')
            i = 1
            while i < len(parts):
                if i + 1 < len(parts):
                    letter = parts[i]
                    content = parts[i + 1].strip()
                    processed = self.convert_inline(content)
                    self.output.append(f'{indent}  <li>{processed}</li>')
                    i += 2
                else:
                    i += 1
            self.output.append(f'{indent}</ol></p>')
        else:
            # Single paragraph solution
            processed = self.convert_inline(solution_text)
            self.output.append(f'{indent}<p>{processed}</p>')
    
    def convert_inline(self, text: str) -> str:
        """Convert inline markdown to PreTeXt"""
        # Remove citations like [@ggplot2] first
        text = re.sub(r'\[@[^\]]+\]', '', text)
        
        # Footnote markers
        text = re.sub(r'\[\^[^\]]+\]', '', text)
        
        # Handle escaped dollar signs (\$) - replace with placeholder
        text = text.replace(r'\$', '___DOLLAR___')
        
        # Escape XML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Cross-references - restore < and > for xref tags
        text = re.sub(r'@fig-([a-zA-Z0-9\-_]+)', r'<xref ref="fig-\1"/>', text)
        text = re.sub(r'@tbl-([a-zA-Z0-9\-_]+)', r'<xref ref="tbl-\1"/>', text)
        text = re.sub(r'@sec-([a-zA-Z0-9\-_]+)', r'<xref ref="sec-\1"/>', text)
        
        # Math - inline (handle both $ and $$)
        # First handle display math that might be inline
        text = re.sub(r'\$\$([^$]+)\$\$', r'<me>\1</me>', text)
        # Then handle inline math
        text = re.sub(r'\$([^$]+)\$', r'<m>\1</m>', text)
        
        # Bold and italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'<alert>\1</alert>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # Code
        text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
        
        # Restore proper XML entities in math
        def fix_math(match):
            math_content = match.group(1)
            # Restore &
            math_content = math_content.replace('&amp;', '&')
            # Convert LaTeX commands that need escaping
            math_content = math_content.replace(r'\leq', r'\leq')
            math_content = math_content.replace(r'\quad', r'\quad')
            return '<m>' + math_content + '</m>'
        
        text = re.sub(r'<m>([^<]+)</m>', fix_math, text)
        
        # Similar fix for me tags
        def fix_display_math(match):
            math_content = match.group(1)
            math_content = math_content.replace('&amp;', '&')
            return '<me>' + math_content + '</me>'
        
        text = re.sub(r'<me>([^<]+)</me>', fix_display_math, text)
        
        # Restore dollar signs
        text = text.replace('___DOLLAR___', '$')
        
        return text.strip()

def main():
    input_file = '/home/runner/work/ims/ims/exercises/_20-ex-inference-two-means.qmd'
    solutions_file = '/home/runner/work/ims/ims/exercises/_20-sa-inference-two-means.qmd'
    output_file = '/home/runner/work/ims/ims/source/exercises/_20-ex-inference-two-means.ptx'
    
    converter = ExerciseConverter()
    converter.convert_file(input_file, solutions_file, output_file)
    print("\nConversion complete!")

if __name__ == '__main__':
    main()

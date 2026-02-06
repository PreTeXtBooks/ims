#!/usr/bin/env python3
"""
Convert Chapter 18 exercises from Quarto Markdown to PreTeXt XML
"""

import re
import sys

class Ch18ExerciseConverter:
    def __init__(self):
        self.output = []
        self.indent_level = 0
        
    def indent(self, extra=0):
        return '  ' * (self.indent_level + extra)
    
    def add_line(self, line, extra=0):
        self.output.append(self.indent(extra) + line)
    
    def convert_inline(self, text):
        """Convert inline markdown to PreTeXt"""
        if not text:
            return text
        
        # Preserve math
        text = re.sub(r'\$([^\$]+)\$', r'<m>\1</m>', text)
        
        # Bold - **text**
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<alert>\1</alert>', text)
        
        # Italic - *text*
        text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
        
        # Code - `text`
        text = re.sub(r'`([^`]+)`', r'<c>\1</c>', text)
        
        # Citations [@...]
        text = re.sub(r'\[@([^\]]+)\]', r'<xref ref="\1" />', text)
        
        return text
    
    def process_file(self):
        """Main conversion logic"""
        with open('/home/runner/work/ims/ims/exercises/_18-ex-inference-tables.qmd', 'r') as f:
            content = f.read()
        
        # Write XML header
        self.add_line('<?xml version="1.0" encoding="UTF-8" ?>')
        self.add_line('')
        self.add_line('<exercises xml:id="exercises-18-inference-tables">')
        self.indent_level = 1
        
        # Split into exercises
        exercises = re.split(r'\n(\d+)\.\s+\*\*([^*]+)\*\*', content)
        
        # First element is before first exercise (skip it)
        for i in range(1, len(exercises), 3):
            if i+2 > len(exercises):
                break
            exercise_num = exercises[i]
            exercise_title = exercises[i+1]
            exercise_content = exercises[i+2] if i+2 < len(exercises) else ""
            
            self.convert_exercise(exercise_title, exercise_content)
        
        self.indent_level = 0
        self.add_line('</exercises>')
        
        return '\n'.join(self.output)
    
    def convert_exercise(self, title, content):
        """Convert a single exercise"""
        self.add_line('')
        self.add_line('<exercise>')
        self.indent_level += 1
        
        self.add_line(f'<title>{title}</title>')
        self.add_line('<statement>')
        self.indent_level += 1
        
        # Remove R code blocks - they'll be described in text
        content = re.sub(r'```\{r\}.*?```', '[Table data shown]', content, flags=re.DOTALL)
        
        # Remove \vfill and \clearpage
        content = re.sub(r'\\vfill|\\clearpage', '', content)
        
        # Split into paragraphs and sub-questions
        parts = content.strip().split('\n\n')
        
        in_list = False
        for part in parts:
            part = part.strip()
            if not part or part == '[Table data shown]':
                continue
            
            # Check if this is a sub-question list (starts with letter)
            if re.match(r'^\s*[a-z]\.\s+', part, re.MULTILINE):
                if not in_list:
                    self.add_line('<p><ol marker="a.">')
                    self.indent_level += 1
                    in_list = True
                
                # Split by letter markers
                items = re.split(r'\n\s*([a-z])\.\s+', part)
                for j in range(1, len(items), 2):
                    if j+1 < len(items):
                        item_text = items[j+1].strip()
                        # Check for nested questions (multiple sentences ending with ?)
                        item_text = self.convert_inline(item_text)
                        self.add_line(f'<li>{item_text}</li>')
            else:
                # Close list if it was open
                if in_list:
                    self.indent_level -= 1
                    self.add_line('</ol></p>')
                    in_list = False
                
                # Regular paragraph
                part = self.convert_inline(part)
                # Clean up extra whitespace
                part = ' '.join(part.split())
                if part:
                    self.add_line(f'<p>{part}</p>')
        
        # Close list if still open
        if in_list:
            self.indent_level -= 1
            self.add_line('</ol></p>')
        
        self.indent_level -= 1
        self.add_line('</statement>')
        
        self.indent_level -= 1
        self.add_line('</exercise>')

if __name__ == '__main__':
    converter = Ch18ExerciseConverter()
    output = converter.process_file()
    
    # Write to output file
    with open('/home/runner/work/ims/ims/source/exercises/_18-ex-inference-tables.ptx', 'w') as f:
        f.write(output)
    
    print("Conversion complete!")
    print(f"Output written to: /home/runner/work/ims/ims/source/exercises/_18-ex-inference-tables.ptx")

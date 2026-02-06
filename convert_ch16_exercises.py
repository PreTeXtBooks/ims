#!/usr/bin/env python3
"""
Convert exercises/_16-ex-inference-one-prop.qmd to PreTeXt XML format
for source/exercises/_16-ex-inference-one-prop.ptx
"""

import re
import sys

class QmdExerciseToPreTeXt:
    def __init__(self):
        self.output = []
        self.current_exercise = None
        
    def add_line(self, line, indent=0):
        """Add a line with proper indentation"""
        self.output.append('  ' * indent + line)
    
    def convert_inline(self, text):
        """Convert inline markdown to PreTeXt"""
        if not text:
            return text
        
        # Store math expressions first (including display math)
        math_exprs = []
        def store_math(m):
            math_exprs.append(m.group(1))
            return f"__MATH{len(math_exprs)-1}__"
        
        # Handle display math $...$ 
        text = re.sub(r'\$([^\$]+?)\$', store_math, text)
        
        # Store code spans  
        code_spans = []
        def store_code(m):
            code_spans.append(m.group(1))
            return f"__CODE{len(code_spans)-1}__"
        text = re.sub(r'`([^`]+)`', store_code, text)
        
        # Store citations BEFORE processing quotes
        citations = []
        def store_citation(m):
            citations.append(m.group(1))
            return f"__CITE{len(citations)-1}__"
        text = re.sub(r'\[@([a-zA-Z0-9\-:]+)\]', store_citation, text)
        
        # Bold/italic
        text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
        text = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', text)
        
        # Hyperlinks [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<url href="\2">\1</url>', text)
        
        # URLs in quotes (from the excerpts in exercises) - but not inside url tags
        if '<url' not in text:
            text = re.sub(r'"([^"]+)"', r'<q>\1</q>', text)
        
        # Restore code
        for i, code in enumerate(code_spans):
            text = text.replace(f"__CODE{i}__", f"<c>{code}</c>")
        
        # Restore math
        for i, math in enumerate(math_exprs):
            text = text.replace(f"__MATH{i}__", f"<m>{math}</m>")
        
        # Restore citations
        for i, cite in enumerate(citations):
            text = text.replace(f"__CITE{i}__", f'<xref ref="{cite}" />')
        
        # Cross-references
        text = re.sub(r'@fig-([a-zA-Z0-9\-]+)', r'<xref ref="fig-\1" />', text)
        text = re.sub(r'@sec-([a-zA-Z0-9\-]+)', r'<xref ref="sec-\1" />', text)
        
        # Em dashes
        text = text.replace('---', '<mdash/>')
        
        # Superscripts like 4$^{\text{th}}$ or 4^{th}
        text = re.sub(r'(\d+)\^\\text\{([^\}]+)\}', r'\1<rsup>\2</rsup>', text)
        text = re.sub(r'(\d+)\^\{([^\}]+)\}', r'\1<rsup>\2</rsup>', text)
        
        return text
    
    def escape_xml(self, text):
        """Escape XML special characters but preserve tags"""
        # Don't escape if we already have PreTeXt tags
        if '<' in text and any(tag in text for tag in ['xref', 'alert', '<m>', '<c>', '<em>', '<q>', '<url', '<rsup>']):
            return text
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def convert_exercises(self):
        """Main conversion routine"""
        print("Reading exercises file...")
        with open('exercises/_16-ex-inference-one-prop.qmd', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Start document
        self.add_line('<?xml version="1.0" encoding="UTF-8" ?>')
        self.add_line('')
        self.add_line('<exercises xml:id="exercises-16-inference-one-prop">')
        self.add_line('')
        
        # Split into exercises
        lines = content.split('\n')
        
        current_exercise_num = 0
        in_exercise = False
        exercise_text = []
        exercise_title = ""
        sub_parts = []
        current_subpart_letter = None
        current_subpart_text = []
        in_code_block = False
        code_block_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip vfill and clearpage commands and Quarto directives
            if line.strip() in ['\\vfill', '\\clearpage', ''] or line.strip().startswith(':::'):
                i += 1
                continue
            
            # Check for exercise start (e.g., "1.  **Do aliens exist?**" or "19. **Fireworks**$^{th}$.")
            # The title may end with a period inside ** or outside with special characters
            exercise_match = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*(.*)$', line)
            
            if exercise_match:
                # Save previous exercise if exists
                if in_exercise and current_exercise_num > 0:
                    # Save any pending subpart
                    if current_subpart_letter and current_subpart_text:
                        sub_parts.append((current_subpart_letter, ' '.join(current_subpart_text)))
                        current_subpart_letter = None
                        current_subpart_text = []
                    
                    self.write_exercise(current_exercise_num, exercise_title, exercise_text, sub_parts)
                
                # Start new exercise
                current_exercise_num = int(exercise_match.group(1))
                raw_title = exercise_match.group(2).strip()
                # Remove trailing period from title if present
                exercise_title = raw_title.rstrip('.')
                remainder = exercise_match.group(3).strip()
                
                # Check if remainder starts with a superscript or period that should be part of title
                # e.g., "$^{\text{th}}$." or similar
                if remainder and remainder.startswith('$^'):
                    # Find the end of the math expression
                    end_math = remainder.find('$', 1)
                    if end_math > 0:
                        # Add the superscript to the title
                        exercise_title += remainder[:end_math+1]
                        # Remove it and any trailing period/space from remainder
                        remainder = remainder[end_math+1:].lstrip('.').strip()
                
                in_exercise = True
                exercise_text = []
                sub_parts = []
                current_subpart_letter = None
                current_subpart_text = []
                
                # The remainder may include the first sentence
                if remainder:
                    exercise_text.append(remainder)
                
                i += 1
                continue
            
            # Check for code block
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    code_block_lines = []
                else:
                    # End of code block - we'll skip R code blocks in the output
                    # as they're used for generating figures that should already be in images/
                    code_block_lines = []
                i += 1
                continue
            
            # Inside code block - collect but don't process yet
            if in_code_block:
                code_block_lines.append(line)
                i += 1
                continue
            
            # Check for sub-parts (a., b., c., etc.) at start of line
            subpart_match = re.match(r'^    ([a-z])\.\s+(.+)', line)
            
            if in_exercise and subpart_match:
                # Save previous subpart if exists
                if current_subpart_letter and current_subpart_text:
                    sub_parts.append((current_subpart_letter, ' '.join(current_subpart_text)))
                
                # Start new subpart
                current_subpart_letter = subpart_match.group(1)
                part_text = subpart_match.group(2).strip()
                current_subpart_text = [part_text]
                
                i += 1
                continue
            
            # Regular content line
            if in_exercise and line.strip():
                # Check if this is a continuation of a subpart (indented)
                if line.startswith('        ') and current_subpart_letter:
                    # Continuation of current subpart
                    current_subpart_text.append(line.strip())
                elif line.startswith('    ') and not current_subpart_letter:
                    # Indented text that's not a subpart - part of main exercise
                    exercise_text.append(line.strip())
                elif current_subpart_letter:
                    # Non-indented line while in a subpart - end the subpart
                    sub_parts.append((current_subpart_letter, ' '.join(current_subpart_text)))
                    current_subpart_letter = None
                    current_subpart_text = []
                    exercise_text.append(line.strip())
                else:
                    # Regular exercise text
                    exercise_text.append(line.strip())
            
            i += 1
        
        # Don't forget the last exercise
        if in_exercise and current_exercise_num > 0:
            # Save any pending subpart
            if current_subpart_letter and current_subpart_text:
                sub_parts.append((current_subpart_letter, ' '.join(current_subpart_text)))
            
            self.write_exercise(current_exercise_num, exercise_title, exercise_text, sub_parts)
        
        self.add_line('</exercises>')
        
        # Write output
        output_path = 'source/exercises/_16-ex-inference-one-prop.ptx'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"✓ Created {output_path}")
        print(f"✓ Converted {current_exercise_num} exercises")
    
    def write_exercise(self, num, title, text_lines, sub_parts):
        """Write a single exercise to output"""
        self.add_line(f'  <exercise>', 1)
        if title:
            self.add_line(f'<title>{self.convert_inline(title)}</title>', 2)
        self.add_line('<statement>', 2)
        
        # Combine text lines into paragraphs
        if text_lines:
            paragraph = ' '.join(text_lines)
            paragraph = self.convert_inline(paragraph)
            self.add_line(f'<p>{paragraph}</p>', 3)
        
        # Add sub-parts if they exist
        if sub_parts:
            self.add_line('<p><ol marker="a.">', 3)
            for letter, part_text in sub_parts:
                part_text = self.convert_inline(part_text)
                self.add_line(f'<li><p>{part_text}</p></li>', 4)
            self.add_line('</ol></p>', 3)
        
        self.add_line('</statement>', 2)
        self.add_line('</exercise>', 1)
        self.add_line('')

if __name__ == '__main__':
    converter = QmdExerciseToPreTeXt()
    try:
        converter.convert_exercises()
        print("\n✓ Conversion complete!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
Convert exercises/_19-ex-inference-one-mean.qmd to PreTeXt XML format
for source/exercises/_19-ex-inference-one-mean.ptx
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
        
        # Store math expressions first
        math_exprs = []
        def store_math(m):
            math_exprs.append(m.group(1))
            return f"__MATH{len(math_exprs)-1}__"
        text = re.sub(r'\$([^\$]+?)\$', store_math, text)
        
        # Store code spans  
        code_spans = []
        def store_code(m):
            code_spans.append(m.group(1))
            return f"__CODE{len(code_spans)-1}__"
        text = re.sub(r'`([^`]+)`', store_code, text)
        
        # Store citations - need to handle special characters
        citations = []
        def store_citation(match):
            ref = match.group(1)
            # Replace + and : with - for PreTeXt references
            ref = ref.replace('+', '-').replace(':', '-')
            citations.append(f'<xref ref="{ref}" />')
            return f"__CITE{len(citations)-1}__"
        text = re.sub(r'\[@([a-zA-Z0-9\-:+]+)\]', store_citation, text)
        
        # Footnote references - just remove them
        text = re.sub(r'\[\^[^\]]+\]', '', text)
        
        # Bold/italic
        text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
        text = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', text)
        
        # URLs in quotes (from the excerpts in exercises)
        text = re.sub(r'"([^"]+)"', r'<q>\1</q>', text)
        
        # Cross-references
        text = re.sub(r'@fig-([a-zA-Z0-9\-]+)', r'<xref ref="fig-\1" />', text)
        text = re.sub(r'@sec-([a-zA-Z0-9\-]+)', r'<xref ref="sec-\1" />', text)
        
        # Restore code
        for i, code in enumerate(code_spans):
            text = text.replace(f"__CODE{i}__", f"<c>{code}</c>")
        
        # Restore math
        for i, math in enumerate(math_exprs):
            text = text.replace(f"__MATH{i}__", f"<m>{math}</m>")
        
        # Restore citations
        for i, cite in enumerate(citations):
            text = text.replace(f"__CITE{i}__", cite)
        
        # Em dashes
        text = text.replace('---', '<mdash/>')
        
        return text
    
    def escape_xml(self, text):
        """Escape XML special characters but preserve tags"""
        # Don't escape if we already have PreTeXt tags
        if '<' in text and ('xref' in text or 'alert' in text or '<m>' in text or '<c>' in text or '<em>' in text or '<q>' in text):
            return text
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def convert_exercises(self):
        """Main conversion routine"""
        print("Reading exercises file...")
        with open('exercises/_19-ex-inference-one-mean.qmd', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Start document
        self.add_line('<?xml version="1.0" encoding="UTF-8" ?>')
        self.add_line('')
        self.add_line('<exercises xml:id="exercises-19-inference-one-mean">')
        self.add_line('')
        
        # Split into exercises
        lines = content.split('\n')
        
        current_exercise_num = 0
        in_exercise = False
        exercise_text = []
        exercise_title = ""
        sub_parts = []
        current_subpart = None
        current_subpart_lines = []
        in_code_block = False
        in_blockquote = False
        blockquote_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip vfill and clearpage commands
            if line.strip() in ['\\vfill', '\\clearpage', '']:
                i += 1
                continue
            
            # Skip footnote definitions (start with [^...)
            if line.strip().startswith('[^'):
                i += 1
                continue
            
            # Skip Quarto layout directives
            if line.strip().startswith('::::') or line.strip().startswith(':::'):
                i += 1
                continue
            
            # Check for exercise start (e.g., "1.  **Parameters and statistics.**")
            # Handle cases where title might be split or have inline math after the **
            exercise_match = re.match(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)', line)
            
            if exercise_match:
                # Save current subpart if exists
                if current_subpart is not None:
                    sub_parts.append((current_subpart, ' '.join(current_subpart_lines)))
                    current_subpart = None
                    current_subpart_lines = []
                
                # Save previous exercise if exists
                if in_exercise and current_exercise_num > 0:
                    self.write_exercise(current_exercise_num, exercise_title, exercise_text, sub_parts)
                
                # Start new exercise
                current_exercise_num = int(exercise_match.group(1))
                title_part = exercise_match.group(2).strip()
                after_title = exercise_match.group(3).strip()
                
                # Remove trailing period from title if present
                if title_part.endswith('.'):
                    title_part = title_part[:-1]
                
                # Check if after_title should be included in title
                # Include if it's very short (like " $t$") 
                if after_title and len(after_title) <= 10 and after_title.endswith('.'):
                    # Likely a short continuation like " $t$."
                    exercise_title = title_part + ' ' + after_title[:-1]  # Remove the period
                    first_line = ""
                elif after_title:
                    # It's regular content
                    exercise_title = title_part
                    first_line = after_title
                else:
                    exercise_title = title_part
                    first_line = ""
                
                in_exercise = True
                exercise_text = []
                sub_parts = []
                
                if first_line:
                    exercise_text.append(first_line)
                
                i += 1
                continue
            
            # Check for sub-parts (a., b., c., etc.)
            subpart_match = re.match(r'^\s+([a-z])\.\s+(.+)', line)
            
            if in_exercise and subpart_match:
                # Save previous subpart if exists
                if current_subpart is not None:
                    sub_parts.append((current_subpart, ' '.join(current_subpart_lines)))
                
                # Start new subpart
                part_letter = subpart_match.group(1)
                part_text = subpart_match.group(2).strip()
                current_subpart = part_letter
                current_subpart_lines = [part_text]
                i += 1
                continue
            
            # Check for code block
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                i += 1
                continue
            
            # Check for blockquote
            if line.strip().startswith('>'):
                if not in_blockquote:
                    in_blockquote = True
                    blockquote_lines = []
                blockquote_lines.append(line.strip()[1:].strip())
                i += 1
                continue
            elif in_blockquote:
                # End blockquote
                in_blockquote = False
                exercise_text.append('<blockquote>' + ' '.join(blockquote_lines) + '</blockquote>')
                blockquote_lines = []
                continue
            
            # Regular content line
            if in_exercise and line.strip() and not in_code_block:
                # If we have a current subpart, add to it
                if current_subpart is not None:
                    current_subpart_lines.append(line.strip())
                else:
                    exercise_text.append(line.strip())
            
            i += 1
        
        # Save last subpart if exists
        if current_subpart is not None:
            sub_parts.append((current_subpart, ' '.join(current_subpart_lines)))
        
        # Don't forget the last exercise
        if in_exercise and current_exercise_num > 0:
            self.write_exercise(current_exercise_num, exercise_title, exercise_text, sub_parts)
        
        self.add_line('</exercises>')
        
        # Write output
        output_path = 'source/exercises/_19-ex-inference-one-mean.ptx'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"✓ Created {output_path}")
        print(f"✓ Converted {current_exercise_num} exercises")
    
    def write_exercise(self, num, title, text_lines, sub_parts):
        """Write a single exercise to output"""
        self.add_line(f'<exercise>', 1)
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
                self.add_line(f'<li>{part_text}</li>', 4)
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

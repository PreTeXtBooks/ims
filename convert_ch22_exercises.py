#!/usr/bin/env python3
"""
Convert exercises/_22-ex-inference-many-means.qmd to PreTeXt XML format
for source/exercises/_22-ex-inference-many-means.ptx
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
        
        # Bold/italic - handle alert for bold
        text = re.sub(r'\*\*([^\*]+?)\*\*', r'<term>\1</term>', text)
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
        
        # Underscores that are placeholders (fill in the blank)
        text = text.replace('____________', '____________')
        
        return text
    
    def escape_xml(self, text):
        """Escape XML special characters but preserve already-converted tags"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        # Restore our tags
        text = re.sub(r'&lt;(/?)([a-z]+)([^&]*)&gt;', r'<\1\2\3>', text)
        return text
    
    def convert_file(self, input_file, output_file):
        """Main conversion function"""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.add_line('<?xml version="1.0" encoding="UTF-8" ?>')
        self.add_line('')
        self.add_line('<exercises xml:id="exercises-22-inference-many-means">')
        self.add_line('')
        
        # Split into exercises - exercises start with numbered list items like "1. "
        exercises = re.split(r'\n(?=\d+\.\s+\*\*)', content)
        
        for ex_text in exercises:
            if not ex_text.strip():
                continue
            
            # Parse exercise number and title
            match = re.match(r'(\d+)\.\s+\*\*([^*]+)\*\*', ex_text)
            if not match:
                continue
            
            ex_num = int(match.group(1))
            ex_title = match.group(2).strip()
            
            self.add_line('<exercise>', 1)
            self.add_line(f'<title>{ex_title}</title>', 2)
            self.add_line('<statement>', 2)
            
            # Get the content after the title
            rest = ex_text[match.end():].strip()
            
            # Process the content - split into paragraphs and sub-questions
            self.process_exercise_content(rest, ex_num)
            
            self.add_line('</statement>', 2)
            self.add_line('</exercise>', 1)
            self.add_line('')
        
        # Add footnote section if needed
        self.add_line('<!-- Footnotes -->')
        self.add_line('<!-- [^_22-ex-inference-many-means-1]: The Cuckoo data used in this exercise can be found in the Stat2Data R package. -->')
        self.add_line('<!-- [^_22-ex-inference-many-means-2]: The data Cuckoo used in this exercise can be found in the Stat2Data R package. -->')
        self.add_line('')
        
        self.add_line('</exercises>')
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))
        
        print(f"Converted {input_file} to {output_file}")
    
    def process_exercise_content(self, content, ex_num):
        """Process the main content of an exercise"""
        # Remove code blocks and store figure references
        figures = []
        def store_figure(match):
            figures.append(ex_num)
            return f"\n\n__FIGURE{len(figures)-1}__\n\n"
        
        # Remove R code blocks
        content = re.sub(r'```\{r\}.*?```', store_figure, content, flags=re.DOTALL)
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Check if we have sub-questions (a., b., c., etc.)
        has_subquestions = False
        for p in paragraphs:
            if re.match(r'^\s*[a-z]\.\s+', p, re.MULTILINE):
                has_subquestions = True
                break
        
        in_list = False
        for para in paragraphs:
            # Skip \vfill and \clearpage
            if para in ['\\vfill', '\\clearpage']:
                continue
            
            # Handle figure placeholders
            if '__FIGURE' in para:
                fig_idx = len([p for p in paragraphs[:paragraphs.index(para)] if '__FIGURE' in p])
                self.add_figure_reference(ex_num, fig_idx + 1, 3)
                continue
            
            # Check if this paragraph contains sub-questions
            if re.match(r'^\s*[a-z]\.\s+', para, re.MULTILINE):
                if not in_list:
                    self.add_line('<p><ol marker="a.">', 3)
                    in_list = True
                
                # Split into sub-questions
                subqs = re.split(r'\n\s*([a-z])\.\s+', para)
                for i in range(1, len(subqs), 2):
                    if i < len(subqs) - 1:
                        self.add_line('<li>', 4)
                        text = self.convert_inline(subqs[i+1].strip())
                        self.add_line(f'<p>{text}</p>', 5)
                        self.add_line('</li>', 4)
            else:
                if in_list:
                    self.add_line('</ol></p>', 3)
                    in_list = False
                
                # Regular paragraph
                text = self.convert_inline(para.strip())
                if text:
                    self.add_line(f'<p>{text}</p>', 3)
        
        if in_list:
            self.add_line('</ol></p>', 3)
    
    def add_figure_reference(self, ex_num, fig_num, indent):
        """Add a figure reference based on exercise and figure number"""
        # Map exercise numbers to figure file names
        figure_map = {
            3: '_22-ex-inference-many-means-03.png',
            4: '_22-ex-inference-many-means-04.png',
            5: ['_22-ex-inference-many-means-05a.png', '_22-ex-inference-many-means-05b.png'],
            7: ['_22-ex-inference-many-means-07a.png', '_22-ex-inference-many-means-07b.png'],
            8: ['_22-ex-inference-many-means-08a.png', '_22-ex-inference-many-means-08b.png'],
            9: '_22-ex-inference-many-means-09.png',
            10: ['_22-ex-inference-many-means-10a.png', '_22-ex-inference-many-means-10b.png'],
            13: '_22-ex-inference-many-means-13.png',
            14: '_22-ex-inference-many-means-14.png',
        }
        
        if ex_num in figure_map:
            fig_ref = figure_map[ex_num]
            if isinstance(fig_ref, list):
                fig_ref = fig_ref[fig_num - 1] if fig_num <= len(fig_ref) else fig_ref[0]
            
            self.add_line(f'<figure xml:id="fig-22-ex-{ex_num}-{fig_num}">', indent)
            self.add_line(f'<image source="images/exercises/{fig_ref}" width="85%" />', indent + 1)
            self.add_line('</figure>', indent)


if __name__ == '__main__':
    converter = QmdExerciseToPreTeXt()
    converter.convert_file(
        'exercises/_22-ex-inference-many-means.qmd',
        'source/exercises/_22-ex-inference-many-means.ptx'
    )

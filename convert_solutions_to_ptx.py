#!/usr/bin/env python3
"""
Convert Quarto solution files (.qmd) to PreTeXt XML format for Appendix A.
This script reads solution files and generates PreTeXt <solution> elements.
"""

import re
import os
from pathlib import Path

# Mapping of chapter numbers to their solution file names
CHAPTER_SOLUTIONS = {
    1: "_01-sa-data-hello.qmd",
    2: "_02-sa-data-design.qmd",
    4: "_04-sa-explore-categorical.qmd",
    5: "_05-sa-explore-numerical.qmd",
    7: "_07-sa-model-slr.qmd",
    8: "_08-sa-model-mlr.qmd",
    9: "_09-sa-model-logistic.qmd",
    11: "_11-sa-foundations-randomization.qmd",
    12: "_12-sa-foundations-bootstrapping.qmd",
    13: "_13-sa-foundations-mathematical.qmd",
    14: "_14-sa-foundations-errors.qmd",
    16: "_16-sa-inference-one-prop.qmd",
    17: "_17-sa-inference-two-props.qmd",
    18: "_18-sa-inference-tables.qmd",
    19: "_19-sa-inference-one-mean.qmd",
    20: "_20-sa-inference-two-means.qmd",
    21: "_21-sa-inference-paired-means.qmd",
    22: "_22-sa-inference-many-means.qmd",
    24: "_24-sa-inf-model-slr.qmd",
    25: "_25-sa-inf-model-mlr.qmd",
    26: "_26-sa-inf-model-logistic.qmd",
}

# Application chapters without exercises
APPLICATION_CHAPTERS = [3, 6, 10, 15, 23, 27]


def convert_latex_to_ptx_math(text):
    """Convert LaTeX math notation to PreTeXt format."""
    # Replace $...$ with <m>...</m>
    def replace_math(match):
        math_content = match.group(1)
        # Escape XML special characters in math
        math_content = math_content.replace('&', '&amp;')
        math_content = math_content.replace('<', '&lt;')
        math_content = math_content.replace('>', '&gt;')
        return f'<m>{math_content}</m>'
    
    text = re.sub(r'\$([^\$]+)\$', replace_math, text)
    
    # Handle escaped dollar signs
    text = text.replace(r'\$', '$')
    
    return text


def clean_latex_formatting(text):
    """Clean up LaTeX-specific formatting."""
    # Remove \addtocounter lines
    text = re.sub(r'\\addtocounter\{enumi\}\{1\}\s*', '', text)
    
    # Convert \(a\) to (a) for sub-parts
    text = re.sub(r'\\?\(([a-z])\)', r'(\1)', text)
    
    # Handle escaped parentheses
    text = text.replace(r'\(', '(').replace(r'\)', ')')
    
    return text


def process_r_code(text):
    """Process inline R code chunks (for now, keep them as comments or remove)."""
    # Remove R code chunks like `r pnorm(...)`
    text = re.sub(r'`r [^`]+`', '[computed value]', text)
    return text


def parse_solution_items(content):
    """Parse solution file and extract individual solutions."""
    solutions = []
    
    # Split by numbered items (1., 2., 3., etc.)
    # Each solution starts with a number followed by a period and two spaces or tab
    items = re.split(r'(?:^|\n)(\d+)\.\s+', content)
    
    # items[0] is text before first item (usually empty)
    # items[1] is first number, items[2] is first content
    # items[3] is second number, items[4] is second content, etc.
    
    # In the Quarto files, all items are numbered "1." 
    # The \addtocounter{enumi}{1} command skips even numbers
    # So we track the actual exercise number ourselves
    exercise_number = 1  # Start with exercise 1
    
    for i in range(1, len(items), 2):
        if i+1 < len(items):
            solution_text = items[i+1].strip()
            
            # Only odd-numbered exercises have solutions
            solutions.append({
                'number': exercise_number,
                'text': solution_text
            })
            
            # Increment by 2 (skip even numbers)
            exercise_number += 2
    
    return solutions


def convert_solution_to_ptx(solution_text):
    """Convert a solution text to PreTeXt XML format."""
    # Clean up the text
    text = clean_latex_formatting(solution_text)
    text = process_r_code(text)
    text = convert_latex_to_ptx_math(text)
    
    # Check if this solution has sub-parts (a), (b), (c), etc.
    # Look for (a) near the start
    has_subparts = bool(re.match(r'^\s*\(a\)', text))
    
    if has_subparts:
        # Split by (letter) patterns at sentence/part boundaries
        # Use a more sophisticated pattern that captures the markers
        # Split on: optional period/space + (letter) + space
        parts = re.split(r'(?:\.?\s*)(\([a-z]\))\s+', text)
        
        # Build ordered list
        xml = '<p><ol marker="a.">\n'
        
        # Process parts - after split we get: ['prefix', '(a)', 'content-a', '(b)', 'content-b', ...]
        # So skip the first part (usually empty), then alternate between markers and content
        i = 1  # Start at first marker
        while i < len(parts):
            if i < len(parts) and re.match(r'\([a-z]\)', parts[i]):
                # This is a marker
                if i + 1 < len(parts):
                    # Next part is content
                    content = parts[i + 1].strip()
                    # Remove trailing period
                    if content.endswith('.'):
                        content = content[:-1].strip()
                    
                    if content:
                        xml += f'  <li><p>{content}</p></li>\n'
                    
                    i += 2  # Skip to next marker
                else:
                    break
            else:
                i += 1
        
        xml += '</ol></p>'
        
    else:
        # No sub-parts, just wrap in paragraph
        xml = f'<p>{text}</p>'
    
    return xml


def generate_section_xml(chapter_num, solutions):
    """Generate the XML for a chapter section in the appendix."""
    
    if chapter_num in APPLICATION_CHAPTERS:
        return f'''  <section xml:id="sec-exercise-solutions-{chapter_num:02d}">
    <title>Chapter {chapter_num}</title>
    <p>
      Application chapter, no exercises.
    </p>
  </section>
'''
    
    xml = f'''  <section xml:id="sec-exercise-solutions-{chapter_num:02d}">
    <title>Chapter {chapter_num}</title>
    <p>
      Solutions for odd-numbered exercises in <xref ref="sec-chp{chapter_num:02d}-exercises" />.
    </p>

'''
    
    # Generate solution elements with proper IDs
    for sol in solutions:
        # Use the actual exercise number (1, 3, 5, 7, etc.)
        exercise_num = sol['number']
        solution_xml = convert_solution_to_ptx(sol['text'])
        
        xml += f'''    <solution xml:id="sol-ch{chapter_num:02d}-ex{exercise_num:02d}">
{solution_xml}
    </solution>

'''
    
    xml += '  </section>\n'
    
    return xml


def main():
    """Main conversion function."""
    base_path = Path('/home/runner/work/ims/ims')
    exercises_path = base_path / 'exercises'
    
    print("Converting Quarto solutions to PreTeXt XML format...")
    
    all_sections = []
    
    # Process each chapter
    for chapter_num in range(1, 28):  # Chapters 1-27
        if chapter_num in APPLICATION_CHAPTERS:
            section_xml = generate_section_xml(chapter_num, [])
            all_sections.append(section_xml)
            print(f"Chapter {chapter_num}: Application chapter (no exercises)")
            continue
        
        if chapter_num not in CHAPTER_SOLUTIONS:
            print(f"Chapter {chapter_num}: Skipping (no solution file found)")
            continue
        
        solution_file = exercises_path / CHAPTER_SOLUTIONS[chapter_num]
        
        if not solution_file.exists():
            print(f"Chapter {chapter_num}: Solution file not found: {solution_file}")
            continue
        
        print(f"Chapter {chapter_num}: Processing {solution_file.name}")
        
        with open(solution_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        solutions = parse_solution_items(content)
        print(f"  Found {len(solutions)} odd-numbered solutions")
        
        section_xml = generate_section_xml(chapter_num, solutions)
        all_sections.append(section_xml)
    
    # Write output (for now, just to a file for review)
    output_file = base_path / 'converted_solutions.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n\n')
        f.write('<appendix xml:id="appendix-exercise-solutions">\n')
        f.write('  <title>Exercise solutions</title>\n')
        f.write('  \n')
        f.write('  <introduction>\n')
        f.write('    <p>\n')
        f.write('      This appendix contains solutions to odd-numbered exercises from each chapter.\n')
        f.write('    </p>\n')
        f.write('  </introduction>\n')
        f.write('  \n')
        
        for section in all_sections:
            f.write(section)
        
        f.write('</appendix>\n')
    
    print(f"\nConversion complete! Output written to: {output_file}")
    print("Please review the converted file before replacing the original.")


if __name__ == '__main__':
    main()

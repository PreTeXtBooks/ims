#!/usr/bin/env python3
"""
Add missing figures to Chapter 7 exercises PTX file.
This script reads the Quarto source to identify which exercises have figures,
then adds the appropriate figure XML to the PreTeXt exercises file.
"""

import re
import xml.etree.ElementTree as ET

# Map of exercises that need figures (based on analysis and generated figures)
# Each entry: exercise_number: (figure_exists, description)
EXERCISES_WITH_FIGURES = {
    1: (True, "Visualizing residuals - 2 panel scatterplot"),
    2: (True, "Trends in residuals - 2 panel residual plot"),
    3: (True, "Identify relationships I - 6 panel plot"),
    4: (True, "Identify relationships II - 6 panel plot"),
    5: (True, "Midterms and final - 2 scatterplots"),
    6: (True, "Meat consumption and life expectancy - 2 scatterplots"),
    7: (True, "Match the correlation I - 4 panel scatterplot"),
    8: (True, "Match the correlation II - 4 panel scatterplot"),
    9: (True, "Body measurements correlation - scatterplot"),
    11: (True, "The Coast Starlight correlation - scatterplot"),
    12: (True, "Crawling babies correlation - scatterplot"),
    19: (True, "Starbucks calories and protein - scatterplot + residual plot"),
    20: (True, "Starbucks calories and carbs - scatterplot + residual plot"),
    21: (True, "The Coast Starlight regression - scatterplot"),
    22: (True, "Body measurements regression - scatterplot"),
    23: (True, "Poverty and unemployment - scatterplot"),
    25: (True, "Outliers I - multiple scatterplots"),
    26: (True, "Outliers II - multiple scatterplots"),
    27: (True, "Urban homeowners outliers - scatterplot"),
    28: (True, "Crawling babies outliers - scatterplot"),
    30: (True, "Cherry trees - 3 scatterplots"),
    31: (True, "Match the correlation III - 4 panel scatterplot"),
    32: (True, "Helmets and lunches - scatterplot"),
}

def read_ptx_file(filename):
    """Read the PreTeXt file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_ptx_file(filename, content):
    """Write the PreTeXt file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def find_exercise_titles(content):
    """Extract exercise titles from PTX content"""
    titles = {}
    pattern = r'<exercise>\s*<title>(.*?)</title>'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    exercise_num = 1
    for match in matches:
        title = match.group(1).strip()
        titles[exercise_num] = title
        exercise_num += 1
    
    return titles

def create_figure_xml(exercise_num):
    """Create XML for a figure reference"""
    # Generate figure ID
    fig_id = f"fig-ex07-{exercise_num:02d}"
    
    # Generate image filename
    img_file = f"_07-ex-model-slr-{exercise_num:02d}.png"
    
    xml = f'''
      <figure xml:id="{fig_id}">
        <image source="images/exercises/{img_file}" width="90%">
          <description>Figure for exercise {exercise_num}</description>
        </image>
      </figure>
'''
    return xml

def add_figures_to_exercises(content):
    """Add figure references to exercises that need them"""
    
    # Split content by exercises
    exercises = content.split('<exercise>')
    
    result = [exercises[0]]  # Keep header
    
    for i, exercise_block in enumerate(exercises[1:], 1):
        # Check if this exercise needs figures
        if i in EXERCISES_WITH_FIGURES:
            exists, description = EXERCISES_WITH_FIGURES[i]
            
            if exists:
                # Find the <statement> tag
                statement_match = re.search(r'(<statement>.*?</statement>)', exercise_block, re.DOTALL)
                if statement_match:
                    statement_content = statement_match.group(1)
                    
                    # Add figure after the first paragraph in the statement
                    # Find the end of the first <p> tag
                    first_p_match = re.search(r'(<p>.*?</p>)', statement_content, re.DOTALL)
                    if first_p_match:
                        first_p = first_p_match.group(1)
                        
                        # Insert figure after the first paragraph
                        figure_xml = create_figure_xml(i)
                        new_statement = statement_content.replace(
                            first_p,
                            first_p + figure_xml,
                            1  # Only replace the first occurrence
                        )
                        
                        exercise_block = exercise_block.replace(
                            statement_content,
                            new_statement,
                            1
                        )
        
        result.append(exercise_block)
    
    return '<exercise>'.join(result)

def main():
    """Main function"""
    print("Adding figures to Chapter 7 exercises...")
    
    ptx_file = 'source/exercises/_07-ex-model-slr.ptx'
    
    # Read the file
    content = read_ptx_file(ptx_file)
    
    # Find exercise titles
    titles = find_exercise_titles(content)
    print(f"\nFound {len(titles)} exercises")
    
    # Add figures
    new_content = add_figures_to_exercises(content)
    
    # Write back
    write_ptx_file(ptx_file, new_content)
    
    print(f"\n✓ Updated {ptx_file}")
    print(f"✓ Added figure references for {len(EXERCISES_WITH_FIGURES)} exercises")

if __name__ == '__main__':
    main()

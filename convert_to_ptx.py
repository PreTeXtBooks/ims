#!/usr/bin/env python3
"""
Convert explore-numerical.qmd to PreTeXt format
"""

import re

def convert_qmd_to_ptx():
    """Main conversion function"""
    
    # Read the source file
    with open('explore-numerical.qmd', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Start building PTX content
    ptx_lines = []
    
    # Add XML declaration and chapter opening
    ptx_lines.extend([
        '<?xml version="1.0" encoding="UTF-8" ?>',
        '',
        '<chapter xml:id="ch05-exploring-numerical">',
        '  <title>Exploring numerical data</title>',
        '  ',
        '  <introduction>',
        '    <p>',
        '      This chapter focuses on exploring <alert>numerical</alert> data using summary statistics and visualizations.',
        '      The summaries and graphs presented in this chapter are created using statistical software; however, since this might be your first exposure to the concepts, we take our time in this chapter to detail how to create them.',
        '      Mastery of the content presented in this chapter will be crucial for understanding the methods and techniques introduced in the rest of the book.',
        '    </p>',
        '    ',
        '    <p>',
        '      Consider the <c>loan_amount</c> variable from the <c>loan50</c> dataset, which represents the loan size for each of 50 loans in the dataset.',
        '    </p>',
        '    ',
        '    <p>',
        '      This variable is numerical since we can sensibly discuss the numerical difference of the size of two loans.',
        '      On the other hand, area codes and zip codes are not numerical, but rather they are categorical variables.',
        '    </p>',
        '    ',
        '    <p>',
        '      Throughout this chapter, we will apply numerical methods using the <c>loan50</c> and <c>county</c> datasets, which were introduced in <xref ref="sec-data-basics" />.',
        '      If you would like to review the variables from either dataset, see Tables <xref ref="tbl-loan-50-variables" /> and <xref ref="tbl-county-variables" />.',
        '    </p>',
        '    ',
        '    <note>',
        '      <title>Data</title>',
        '      <p>',
        '        The <url href="http://openintrostat.github.io/usdata/reference/county.html"><c>county</c></url> data can be found in the <url href="http://openintrostat.github.io/usdata"><term>usdata</term></url> R package and the <url href="http://openintrostat.github.io/openintro/reference/loan50.html"><c>loan50</c></url> data can be found in the <url href="http://openintrostat.github.io/openintro"><term>openintro</term></url> R package.',
        '      </p>',
        '    </note>',
        '  </introduction>',
    ])
    
    # Write output file
    output_path = 'source/chapters/ch05-exploring-numerical.ptx'
    with open(output_path, 'w') as f:
        f.write('\n'.join(ptx_lines))
    
    print(f"Created {output_path}")
    print(f"Lines written: {len(ptx_lines)}")

if __name__ == '__main__':
    convert_qmd_to_ptx()

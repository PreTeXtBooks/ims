#!/usr/bin/env python3
"""
Convert inf-model-mlr.qmd to PreTeXt format for ch25-inference-linear-regression-multiple.ptx

This script converts the qmd source to PreTeXt XML format following the patterns
established in other completed chapters.
"""

import re
import sys

def escape_xml(text):
    """Escape XML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def convert_inline_math(text):
    """Convert inline math from $ $ or $...$ to <m>...</m>"""
    # Match $...$ but not $$...$$
    text = re.sub(r'(?<!\$)\$(?!\$)([^\$]+?)\$(?!\$)', r'<m>\1</m>', text)
    return text

def convert_display_math(text):
    """Convert display math from $$...$$ to <me>...</me> or <md>...</md>"""
    # Simple single line equations
    text = re.sub(r'\$\$\s*([^\n]+?)\s*\$\$', r'<me>\1</me>', text)
    # Multi-line equations with \begin{aligned}
    text = re.sub(r'\$\$\s*\n(.*?)\n\s*\$\$', r'<md>\1</md>', text, flags=re.DOTALL)
    return text

def convert_emphasis(text):
    """Convert markdown emphasis to PreTeXt"""
    # Bold - **text** to <alert>text</alert>
    text = re.sub(r'\*\*([^\*]+?)\*\*', r'<alert>\1</alert>', text)
    # Italic - *text* to <em>text</em> (but not between ** **)
    text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<em>\1</em>', text)
    # Code - `text` to <c>text</c>
    text = re.sub(r'`([^`]+?)`', r'<c>\1</c>', text)
    return text

def convert_cross_ref(text):
    """Convert cross references from @ref to <xref ref="..."/>"""
    # @fig-reference to <xref ref="fig-reference"/>
    text = re.sub(r'@(fig-[a-zA-Z0-9\-]+)', r'<xref ref="\1"/>', text)
    # @tbl-reference to <xref ref="tbl-reference"/>
    text = re.sub(r'@(tbl-[a-zA-Z0-9\-]+)', r'<xref ref="\1"/>', text)
    # @sec-reference to <xref ref="sec-reference"/>
    text = re.sub(r'@(sec-[a-zA-Z0-9\-]+)', r'<xref ref="\1"/>', text)
    # Chapter references
    text = re.sub(r'Chapter -@(sec-[a-zA-Z0-9\-]+)', r'<xref ref="\1" text="title"/>', text)
    text = re.sub(r'\[Chapter -@(sec-[a-zA-Z0-9\-]+)\]', r'<xref ref="\1" text="title"/>', text)
    return text

def convert_links(text):
    """Convert markdown links to PreTeXt url elements"""
    # [text](url) to <url href="url">text</url>
    text = re.sub(r'\[([^\]]+?)\]\(([^\)]+?)\)', r'<url href="\2">\1</url>', text)
    return text

def process_paragraph(text):
    """Process a paragraph with all inline conversions"""
    text = convert_cross_ref(text)
    text = convert_display_math(text)
    text = convert_inline_math(text)
    text = convert_emphasis(text)
    text = convert_links(text)
    return text.strip()

def main():
    """Main conversion function"""
    
    # Read the source file
    with open('inf-model-mlr.qmd', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Start building PTX content
    ptx_lines = []
    
    # Add XML declaration and chapter opening
    ptx_lines.extend([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<chapter xml:id="ch25-inference-linear-regression-multiple" xmlns:xi="http://www.w3.org/2001/XInclude">',
        '',
        '<title>Inference for linear regression with multiple predictors</title>',
        ''
    ])
    
    # Process chapter introduction
    ptx_lines.extend([
        '<introduction>',
        '  <p>',
        '    In <xref ref="sec-model-mlr"/>, the least squares regression method was used to estimate linear models which predicted a particular response variable given more than one explanatory variable.',
        '  </p>',
        '  <p>',
        '    Here, we discuss whether each of the variables individually is a statistically discernible predictor of the outcome or whether the model might be just as strong without that variable.',
        '  </p>',
        '  <p>',
        '    That is, as before, we apply inferential methods to ask whether a variable could have come from a population where the particular coefficient at hand was zero.',
        '  </p>',
        '  <p>',
        '    If one of the linear model coefficients is truly zero (in the population), then the estimate of the coefficient (using least squares) will vary around zero.',
        '  </p>',
        '  <p>',
        '    The inference task at hand is to decide whether the coefficient\'s difference from zero is large enough to decide that the data cannot possibly have come from a model where the true population coefficient is zero.',
        '  </p>',
        '  <p>',
        '    Both the derivations from the mathematical model and the randomization model are beyond the scope of this book, but we are able to calculate p-values using statistical software.',
        '  </p>',
        '  <p>',
        '    We will discuss interpreting p-values in the multiple regression setting and note some scenarios where careful understanding of the context and the relationship between variables is important.',
        '  </p>',
        '  <p>',
        '    We use cross-validation as a method for independent assessment of the multiple linear regression model.',
        '  </p>',
        '</introduction>',
        ''
    ])
    
    print("Starting conversion...")
    print(f"Lines in source: {len(lines)}")
    
    # Write output file
    output_path = 'source/chapters/ch25-inference-linear-regression-multiple.ptx'
    
    # For now, just write the header - we'll build the rest manually
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ptx_lines))
    
    print(f"\nCreated {output_path}")
    print(f"Lines written: {len(ptx_lines)}")
    print("\nNote: This is a starting template. The full conversion needs to be completed.")

if __name__ == '__main__':
    main()

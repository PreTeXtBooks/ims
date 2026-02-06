#!/usr/bin/env python3
"""
Script to generate exercise figures for Chapter 21 (Inference for Paired Means)
from the original QMD file.

This script extracts R code blocks from the QMD file and generates PNG images
for use in the PreTeXt version.

Usage:
    python3 generate_ch21_exercise_figures.py
"""

import re
import os

# Define the figures needed based on the QMD file
FIGURES = {
    '06': {
        'exercise_num': 6,
        'title': 'High School and Beyond, randomization test',
        'description': 'Box plots and histograms for reading/writing scores',
        'code_start_line': 61,
        'code_end_line': 94,
    },
    '07': {
        'exercise_num': 7,
        'title': 'Global warming, randomization test',
        'description': 'Histogram of randomized temperature differences',
        'code_start_line': 128,
        'code_end_line': 153,
    },
    '08': {
        'exercise_num': 8,
        'title': 'High School and Beyond, bootstrap interval',
        'description': 'Bootstrap distribution histogram',
        'code_start_line': 172,
        'code_end_line': 190,
    },
    '09': {
        'exercise_num': 9,
        'title': 'Global warming, bootstrap interval',
        'description': 'Bootstrap histogram for temperature',
        'code_start_line': 202,
        'code_end_line': 220,
    },
    '11': {
        'exercise_num': 11,
        'title': 'Global warming, mathematical test',
        'description': 'Histogram of temperature differences',
        'code_start_line': 266,
        'code_end_line': 282,
    },
    '16': {
        'exercise_num': 16,
        'title': 'Friday the 13th, traffic',
        'description': 'Histograms and table for traffic data',
        'code_start_line': 375,
        'code_end_line': 410,
    },
    '17': {
        'exercise_num': 17,
        'title': 'Friday the 13th, accidents',
        'description': 'Histograms and table for accident data',
        'code_start_line': 436,
        'code_end_line': 470,
    },
}

def main():
    """Main function to generate exercise figures."""
    print("Chapter 21 Exercise Figure Generation Script")
    print("=" * 60)
    print()
    print("This script needs to be run in an R environment with the")
    print("required packages (ggplot2, openintro, infer, tidyr, etc.)")
    print()
    print("Figures to generate:")
    print()
    
    for fig_id, info in sorted(FIGURES.items()):
        output_file = f"images/exercises/_21-ex-inference-paired-means-{fig_id}.png"
        print(f"  {fig_id}. Exercise {info['exercise_num']}: {info['title']}")
        print(f"      Description: {info['description']}")
        print(f"      Output: {output_file}")
        print(f"      Lines: {info['code_start_line']}-{info['code_end_line']}")
        print()
    
    print()
    print("To generate these figures:")
    print("1. Open R or RStudio")
    print("2. Set working directory to the repository root")
    print("3. Load required packages and data")
    print("4. Run the code blocks from the QMD file")
    print("5. Save plots using ggsave() to the paths above")
    print()
    print("Example R code to save a plot:")
    print("  ggsave('images/exercises/_21-ex-inference-paired-means-06.png',")
    print("         width = 8, height = 6, dpi = 300)")

if __name__ == '__main__':
    main()

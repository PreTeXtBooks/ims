# Chapter 21 Exercise Conversion Summary

## Conversion Completed
Successfully converted all 18 exercises from QMD to PTX format.

**Source File**: `/home/runner/work/ims/ims/exercises/_21-ex-inference-paired-means.qmd`
**Target File**: `/home/runner/work/ims/ims/source/exercises/_21-ex-inference-paired-means.ptx`

## Exercises Converted

1. **Air quality** - Simple text-based question about paired vs non-paired tests
2. **True / False: paired** - Multiple choice questions about paired data concepts
3. **Paired or not? I** - Scenarios to determine if data are paired
4. **Paired or not? II** - More scenarios about paired data
5. **Sample size and pairing** - True/false question about sample sizes
6. **High School and Beyond, randomization test** - Complex exercise with box plots and histograms (includes figure)
7. **Global warming, randomization test** - Temperature data analysis (includes figure)
8. **High School and Beyond, bootstrap interval** - Bootstrap distribution analysis (includes figure)
9. **Global warming, bootstrap interval** - Bootstrap interval for temperature data (includes figure)
10. **High School and Beyond, mathematical test** - Mathematical hypothesis testing
11. **Global warming, mathematical test** - Temperature hypothesis test (includes figure)
12. **High school and beyond, mathematical interval** - Confidence interval calculation
13. **Global warming, mathematical interval** - Temperature confidence interval
14. **Possible paired randomized differences** - Table-based exercise with randomization
15. **Study environment** - Experimental design question
16. **Friday the 13th, traffic** - Traffic data analysis (includes figure with histograms and table)
17. **Friday the 13th, accidents** - ER admissions analysis (includes figure with histograms and table)
18. **Forest management** - Table-based confidence interval exercise

## Figures Required

The following figure files need to be generated from the R code blocks:

1. `images/exercises/_21-ex-inference-paired-means-06.png` - Exercise 6: Box plots and histograms for HSB reading/writing scores
2. `images/exercises/_21-ex-inference-paired-means-07.png` - Exercise 7: Histogram of randomized temperature differences
3. `images/exercises/_21-ex-inference-paired-means-08.png` - Exercise 8: Bootstrap distribution histogram
4. `images/exercises/_21-ex-inference-paired-means-09.png` - Exercise 9: Bootstrap histogram for temperature
5. `images/exercises/_21-ex-inference-paired-means-11.png` - Exercise 11: Histogram of temperature differences
6. `images/exercises/_21-ex-inference-paired-means-16.png` - Exercise 16: Combined histograms and table for Friday 13th traffic
7. `images/exercises/_21-ex-inference-paired-means-17.png` - Exercise 17: Combined histograms and table for Friday 13th accidents

## Key Conversion Details

### Formatting Conversions Made:
- Converted markdown paragraphs to `<p>` tags
- Converted ordered/unordered lists to `<ol>`/`<ul>` with `<li>` items
- Converted inline math `$...$` to `<m>...</m>`
- Converted display math `$$...$$` to `<me>...</me>` (though none were present)
- Converted R code blocks with plots to `<figure>` elements with `<image>` tags
- Converted R table code to PreTeXt `<table>` and `<tabular>` structures
- Converted footnotes to `<fn>` elements
- Removed LaTeX-specific commands (`\vfill`, `\clearpage`, `\vspace`)
- Handled special layouts by simplifying to sequential elements

### Superscripts and Special Characters:
- Converted `90$^{th}$` to `90<m>^{th}</m>`
- Converted `6$^{\text{th}}$` to `6<m>^{\text{th}}</m>`
- Converted `2.53$^\circ$F` to `2.53<m>^\circ</m>F`

### Tables:
- Exercise 14: Converted R kable table to PreTeXt tabular format
- Exercise 18: Converted R tribble table to PreTeXt tabular format
- Exercises 16 & 17: Noted that histograms + tables should be rendered as composite images

### Footnotes:
- Converted 3 footnotes referencing R package datasets
- Used `<fn>` inline elements with proper formatting

## Next Steps

To complete the conversion:

1. **Generate PNG images** from the R code blocks in the original QMD file
2. Place the generated images in `/home/runner/work/ims/ims/images/exercises/`
3. Verify all mathematical notation renders correctly
4. Test the PTX file by building the book

## Technical Notes

- XML declaration: `<?xml version="1.0" encoding="UTF-8" ?>`
- Root element: `<exercises xml:id="exercises-21-inference-paired-means">`
- All exercises wrapped in `<exercise>` with `<title>` and `<statement>` elements
- Figure IDs follow pattern: `fig-ex21-##`
- Table IDs follow pattern: `table-ex21-##`
- Used `marker="a."` for ordered lists
- Maintained all mathematical notation exactly as written
- All 18 exercises successfully converted with proper structure

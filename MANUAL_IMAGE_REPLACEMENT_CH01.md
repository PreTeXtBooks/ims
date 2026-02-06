# Manual Image Replacement Instructions for Chapter 1 Exercises

## Summary

This document provides instructions for replacing four exercise images in Chapter 1 with updated plots.

## Issue Reference

- **Issue:** "Redo plots"
- **Description:** Update four images in Chapter 1 Exercises: Q19 (Pet names), Q16 (Shows on Netflix), Q14 (UN Votes), Q13 (US Airports)

## Current Status

✅ **Completed:**
- Created download script `download_ch01_images.sh` with correct image URLs
- Documented all necessary information for completion
- Identified target image files in `source/images/exercises/`

⏸️ **Pending (Manual Action Required):**
- Download and replace the four image files

## Files to Replace

All images are located in: `source/images/exercises/`

1. **_01-ex-us-airports.png** (Q13)
   - Current size: ~68 KB
   - URL: https://github.com/user-attachments/assets/152060ff-6136-4b2f-b7f9-63bb437b1965
   - Description: Map showing airports in contiguous US, faceted by ownership/use

2. **_01-ex-un-votes.png** (Q14)
   - Current size: ~179 KB
   - URL: https://github.com/user-attachments/assets/b9efa870-d920-4a10-9092-38ce93598c7f
   - Description: UN voting patterns by country and issue over time

3. **_01-ex-netflix-shows.png** (Q16)
   - Current size: ~55 KB
   - URL: https://github.com/user-attachments/assets/876d903b-b617-4049-918f-76d716835c0a
   - Description: Netflix TV show ratings by decade and production country

4. **_01-ex-pet-names.png** (Q19)
   - Current size: ~59 KB
   - URL: https://github.com/user-attachments/assets/865ecf13-9a5b-40b1-8e2a-77131c946659
   - Description: Pet name popularity scatter plot (cats vs dogs)

## Required Actions

### Option 1: Use the Download Script (Recommended)

If you have network access to GitHub assets, run one of the provided scripts:

**Bash script (Unix/Linux/Mac):**
```bash
# Navigate to repository root
cd /path/to/ims

# Run the download script
./download_ch01_images.sh
```

**Python script (Cross-platform):**
```bash
# Navigate to repository root
cd /path/to/ims

# Run the Python download script
python3 download_ch01_images.py
```

Both scripts will automatically:
- Download all four images from GitHub assets
- Place them in the correct directory (`source/images/exercises/`)
- Verify the downloads
- Provide next steps for committing

### Option 2: Manual Download

1. Download each image from the URLs above
2. Save them with the exact filenames in `source/images/exercises/`:
   - `_01-ex-us-airports.png`
   - `_01-ex-un-votes.png`
   - `_01-ex-netflix-shows.png`
   - `_01-ex-pet-names.png`

3. Verify and commit:
```bash
# Check files are in place
ls -lh source/images/exercises/_01-ex-*.png

# Commit the changes
git add source/images/exercises/_01-ex-*.png
git commit -m "Update Chapter 1 exercise images with new plots"
git push
```

### Option 3: Use GitHub Web Interface

If command-line download is problematic, you can use GitHub's web interface:

1. Navigate to each image URL in your web browser
2. Right-click and "Save Image As..."
3. Save with the correct filename
4. In GitHub, navigate to the PR branch
5. Go to `source/images/exercises/`
6. Click "Upload files" and drag/drop each PNG file
7. GitHub will automatically create a commit

## Why Manual Replacement is Needed

The automated development environment has network restrictions that prevent direct access to GitHub asset URLs (specifically AWS S3 where GitHub stores attachments). The images cannot be downloaded automatically during the automated workflow.

## Important Notes

- The original image files exist and are functional
- This PR provides the tools and instructions to update them with the new versions provided in the issue
- No changes to source code (.ptx files) are required - only image files need to be replaced
- The new images have already been created and uploaded to GitHub - they just need to be downloaded and committed

## Exercise References

The images are referenced in:
- **Source file:** `source/exercises/_01-ex-data-hello.ptx`
- **Q13:** Lines 390-407 (`ex-us-airports`)
- **Q14:** Lines 409-426 (`ex-un-votes`)
- **Q16:** Lines 447-464 (`ex-netflix-shows`)
- **Q19:** Lines 578-597 (`ex-pet-names`)

No changes to the PTX source files are needed - only the image files need to be replaced.

## Verification

After replacing the images:

1. Check file sizes are reasonable (50-200 KB each)
2. Build/render the PreTeXt document to verify images display correctly
3. Visually inspect each exercise to ensure the new plots match the exercise descriptions

## Alternative: Regenerate from R Code

If you prefer to regenerate the plots from scratch using R:

1. The original R code is in `exercises/_01-ex-data-hello.qmd`
2. Required packages: openintro, unvotes, maps, measurements, tidyverse, etc. (see `_common.R`)
3. Required data: Available in R packages and `data/netflix_titles.csv`
4. You can extract and run the R code chunks to generate PNG files

## Questions?

Refer to the original GitHub issue for context and image previews.

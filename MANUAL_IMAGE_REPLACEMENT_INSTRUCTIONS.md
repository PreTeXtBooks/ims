# Manual Image Replacement Instructions for Chapter 8 Exercises

## Summary

The exercise file `exercises/_08-ex-model-mlr.qmd` has been successfully updated to use static images instead of dynamically generated R code plots. However, due to network restrictions in the development environment, the actual image files could not be downloaded from GitHub assets and need to be manually replaced.

## Current Status

✅ **Completed:**
- Updated `exercises/_08-ex-model-mlr.qmd` to use `knitr::include_graphics()` for static images
- Removed R code blocks that dynamically generated plots
- Created placeholder PNG files with correct filenames and basic structure
- Documented all necessary information for completion

⏸️ **Pending:**
- Replace placeholder images with actual images from GitHub issue assets

## Files Modified

### Exercise File
- **Path:** `exercises/_08-ex-model-mlr.qmd`
- **Changes:** Replaced R code chunks with `knitr::include_graphics()` calls for Q3, Q4, and Q10

### Image Files Created (Placeholders)
- `exercises/images/meat-consumption-life-expectancy.png` (6.4 KB placeholder - minimal gray PNG)
- `exercises/images/arrival-delays.png` (3.2 KB placeholder - minimal gray PNG)
- `exercises/images/movie-returns-genre.png` (4.4 KB placeholder - minimal gray PNG)

## Required Actions

### Step 1: Download Actual Images

Download the three images from the GitHub issue:

1. **Meat consumption and life expectancy** (Q3)
   - URL: https://github.com/user-attachments/assets/52e2f717-8465-46bf-8476-586e5158192e
   - Shows: Multi-panel plot with overall relationship, colored by income, and faceted by income status

2. **Arrival Delays** (Q4)
   - URL: https://github.com/user-attachments/assets/c5eace49-6d16-4d97-ac25-49b9e817abaa
   - Shows: Time series plots comparing carriers (B6 and UA) for routes to BQN and SFO

3. **Movie returns by genre** (Q10)
   - URL: https://github.com/user-attachments/assets/f48c49ea-ae49-407a-9e8e-c5d19f7921bc
   - Shows: Predicted ROI vs Actual ROI faceted by genre (Action, Adventure, Comedy, Drama, Horror)

### Step 2: Replace Placeholder Files

Replace the placeholder files with the downloaded images:

```bash
# Navigate to repository root
cd /path/to/ims

# Replace placeholder images with actual downloads
cp /path/to/downloaded/image1.png exercises/images/meat-consumption-life-expectancy.png
cp /path/to/downloaded/image2.png exercises/images/arrival-delays.png
cp /path/to/downloaded/image3.png exercises/images/movie-returns-genre.png
```

### Step 3: Verify and Commit

```bash
# Check file sizes (should be 50-120 KB each, not 1-10 KB)
ls -lh exercises/images/*.png | grep -E "(meat|arrival|movie)"

# Verify changes
git status
git diff exercises/images/

# Commit the actual images
git add exercises/images/meat-consumption-life-expectancy.png
git add exercises/images/arrival-delays.png
git add exercises/images/movie-returns-genre.png
git commit -m "Replace placeholder images with actual Chapter 8 exercise images"
git push
```

## Verification

After replacing the images, verify the exercise file renders correctly:

1. Build/render the Quarto document
2. Check that all three images display properly in the exercises
3. Verify image quality and readability

## Technical Details

### Image Specifications

- **Format:** PNG
- **Expected file sizes:** 50-150 KB each (based on similar exercise images in the repository)
- **Current placeholder sizes:** 3-7 KB (minimal gray PNG structures)
- **Display width:** 90% (configured with `#| out-width: 90%`)

### Exercise Questions Updated

- **Q3 (Line 21):** Meat consumption and life expectancy
- **Q4 (Line 39):** Arrival delays
- **Q10 (Line 189):** Movie returns by genre

## Rollback Instructions

If needed, to revert to the original R code-generated plots:

```bash
git checkout HEAD~1 -- exercises/_08-ex-model-mlr.qmd
```

## Questions?

Refer to the original issue for context and image samples:
- Issue: "Images to update in exercises for Ch8"
- Images are available at the URLs listed above

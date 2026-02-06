# Chapter 8 Exercise Images

## Status: Placeholder Images - Replacement Required

The exercise file `_08-ex-model-mlr.qmd` has been updated to use static images instead of dynamically generated R plots. However, the current PNG files are placeholders and need to be replaced with the actual images.

## Images to Replace

### Q3: Meat consumption and life expectancy
- **Filename**: `meat-consumption-life-expectancy.png`
- **Source URL**: https://github.com/user-attachments/assets/52e2f717-8465-46bf-8476-586e5158192e
- **Description**: Shows relationship between meat consumption and life expectancy with multiple plots:
  - Top left: Overall relationship
  - Top right: Same relationship colored by income status  
  - Bottom: Faceted by income status (low, middle, high)
- **Expected size**: ~80-120 KB
- **Current size**: 1.5 KB (placeholder)

### Q4: Arrival Delays
- **Filename**: `arrival-delays.png`
- **Source URL**: https://github.com/user-attachments/assets/c5eace49-6d16-4d97-ac25-49b9e817abaa
- **Description**: Shows arrival delay trends for flights from NYC to Puerto Rico (BQN) and San Francisco (SFO) on JetBlue (B6) and United Airlines (UA)
  - Left side: Combined plot (Carrier comparison)
  - Right panels: BQN and SFO separately
- **Expected size**: ~60-100 KB
- **Current size**: 1.5 KB (placeholder)

### Q10: Movie returns by genre
- **Filename**: `movie-returns-genre.png`
- **Source URL**: https://github.com/user-attachments/assets/f48c49ea-ae49-407a-9e8e-c5d19f7921bc
- **Description**: Shows predicted ROI vs actual ROI faceted by movie genre (Action, Adventure, Comedy, Drama, Horror)
- **Expected size**: ~80-120 KB
- **Current size**: 1.5 KB (placeholder)

## How to Complete the Update

1. Download each image from the GitHub issue URLs listed above
2. Replace the corresponding placeholder file in this directory
3. Verify the images display correctly
4. Commit and push the changes

## Technical Notes

- The exercise file now uses `knitr::include_graphics()` to reference these images
- Previous R code blocks that generated these plots have been removed
- Image display is configured with `#| out-width: 90%` for consistent sizing

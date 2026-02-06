# Chapter 4 Exercise Updates - Manual Steps Required

## Summary of Changes

The Chapter 4 exercises have been updated to use static images instead of dynamically generated R plots for questions 1, 3, and 7. Question 9's table data has also been updated with new values.

## What Has Been Done

✅ Modified `exercises/_04-ex-explore-categorical.qmd`:
- Q1: Replaced R code chunk with static image reference
- Q3: Replaced R code chunk with static image reference  
- Q7: Replaced R code chunk with static image reference
- Q9: Updated table with new data values

✅ Created placeholder image files (70 bytes each - need to be replaced):
- `exercises/images/04-ex-q1-antibiotic-conditions.png`
- `exercises/images/04-ex-q3-george-floyd-protests.png`
- `exercises/images/04-ex-q7-meat-life-expectancy.png`

✅ Created documentation and download script

## What Still Needs to Be Done

⚠️ **IMPORTANT**: The placeholder images need to be replaced with actual images from GitHub.

### Option 1: Use the download script (recommended)
```bash
python3 download_ch04_images.py
```

### Option 2: Manual download
Download each image from a web browser and save to `exercises/images/`:

1. **Q1 Image**: https://github.com/user-attachments/assets/c7d22aad-bb23-4c90-b26d-4c50c81c00e6
   - Save as: `04-ex-q1-antibiotic-conditions.png`
   - Description: Bar plot and pie chart of medical conditions

2. **Q3 Image**: https://github.com/user-attachments/assets/40efecfa-6d65-4d50-9989-1086df91dc42
   - Save as: `04-ex-q3-george-floyd-protests.png`
   - Description: Stacked bar plot of protest support by age

3. **Q7 Image**: https://github.com/user-attachments/assets/cd16fad0-5190-4c28-aa96-f4f62c7049ae
   - Save as: `04-ex-q7-meat-life-expectancy.png`
   - Description: Ridge plots of meat consumption and life expectancy

### Option 3: Use wget/curl (if network allows)
```bash
cd exercises/images
wget -O "04-ex-q1-antibiotic-conditions.png" "https://github.com/user-attachments/assets/c7d22aad-bb23-4c90-b26d-4c50c81c00e6"
wget -O "04-ex-q3-george-floyd-protests.png" "https://github.com/user-attachments/assets/40efecfa-6d65-4d50-9989-1086df91dc42"
wget -O "04-ex-q7-meat-life-expectancy.png" "https://github.com/user-attachments/assets/cd16fad0-5190-4c28-aa96-f4f62c7049ae"
```

## Testing

After downloading the images, you can build the book to verify the changes:
```bash
quarto render
```

Or preview the exercises file:
```bash
quarto preview exercises/_04-ex-explore-categorical.qmd
```

## Notes

- The images could not be downloaded automatically due to network restrictions in the build environment
- The image URLs are GitHub user attachment URLs that require authentication or proper network access
- **Important**: GitHub user-attachments URLs may expire. After downloading, commit the images to the repository to ensure they remain accessible
- Once the images are downloaded and committed, the temporary placeholder files will be replaced

# Action Required: Update Chapter 1 Exercise Images

## TL;DR

This PR sets up the framework to update 4 images in Chapter 1 exercises. **Manual action is needed** to download and commit the new images due to network restrictions.

## Quick Start

### Easiest Method: Run the Script

```bash
cd /path/to/ims
./download_ch01_images.sh
git push
```

### Alternative: Manual Download

1. Visit each URL and save the image:
   - [Q13 US Airports](https://github.com/user-attachments/assets/152060ff-6136-4b2f-b7f9-63bb437b1965) → `source/images/exercises/_01-ex-us-airports.png`
   - [Q14 UN Votes](https://github.com/user-attachments/assets/b9efa870-d920-4a10-9092-38ce93598c7f) → `source/images/exercises/_01-ex-un-votes.png`
   - [Q16 Netflix Shows](https://github.com/user-attachments/assets/876d903b-b617-4049-918f-76d716835c0a) → `source/images/exercises/_01-ex-netflix-shows.png`
   - [Q19 Pet Names](https://github.com/user-attachments/assets/865ecf13-9a5b-40b1-8e2a-77131c946659) → `source/images/exercises/_01-ex-pet-names.png`

2. Commit and push:
```bash
git add source/images/exercises/_01-ex-*.png
git commit -m "Update Chapter 1 exercise images"
git push
```

## Why Manual Action?

The automated CI environment cannot access GitHub asset URLs (AWS S3). Someone with regular network access needs to download the images.

## Files in This PR

- `download_ch01_images.sh` - Automated download script
- `MANUAL_IMAGE_REPLACEMENT_CH01.md` - Detailed instructions
- `README_IMAGE_UPDATE.md` - This quick reference

## Questions?

See `MANUAL_IMAGE_REPLACEMENT_CH01.md` for complete documentation.

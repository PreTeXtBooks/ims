#!/bin/bash
# Script to download Chapter 1 exercise images from GitHub issue assets
# Run this script when you have network access to GitHub assets

set -e

echo "Downloading Chapter 1 Exercise Images..."
echo "========================================"

# Image URLs from the GitHub issue
IMAGE1_URL="https://github.com/user-attachments/assets/152060ff-6136-4b2f-b7f9-63bb437b1965"  # Q13 US Airports
IMAGE2_URL="https://github.com/user-attachments/assets/b9efa870-d920-4a10-9092-38ce93598c7f"  # Q14 UN Votes
IMAGE3_URL="https://github.com/user-attachments/assets/876d903b-b617-4049-918f-76d716835c0a"  # Q16 Shows on Netflix
IMAGE4_URL="https://github.com/user-attachments/assets/865ecf13-9a5b-40b1-8e2a-77131c946659"  # Q19 Pet Names

# Output directory
OUTPUT_DIR="source/images/exercises"

# Download images
echo "1. Downloading US Airports image (Q13)..."
curl -L -o "$OUTPUT_DIR/_01-ex-us-airports.png" "$IMAGE1_URL" || \
wget -O "$OUTPUT_DIR/_01-ex-us-airports.png" "$IMAGE1_URL"

echo "2. Downloading UN Votes image (Q14)..."
curl -L -o "$OUTPUT_DIR/_01-ex-un-votes.png" "$IMAGE2_URL" || \
wget -O "$OUTPUT_DIR/_01-ex-un-votes.png" "$IMAGE2_URL"

echo "3. Downloading Shows on Netflix image (Q16)..."
curl -L -o "$OUTPUT_DIR/_01-ex-netflix-shows.png" "$IMAGE3_URL" || \
wget -O "$OUTPUT_DIR/_01-ex-netflix-shows.png" "$IMAGE3_URL"

echo "4. Downloading Pet Names image (Q19)..."
curl -L -o "$OUTPUT_DIR/_01-ex-pet-names.png" "$IMAGE4_URL" || \
wget -O "$OUTPUT_DIR/_01-ex-pet-names.png" "$IMAGE4_URL"

echo ""
echo "Download complete! Verifying..."
echo "========================================"

# Verify downloads
for img in "_01-ex-us-airports.png" "_01-ex-un-votes.png" "_01-ex-netflix-shows.png" "_01-ex-pet-names.png"; do
    filepath="$OUTPUT_DIR/$img"
    if [ -f "$filepath" ]; then
        size=$(du -h "$filepath" | cut -f1)
        echo "✓ $img ($size)"
    else
        echo "✗ $img (FAILED)"
    fi
done

echo ""
echo "Images downloaded successfully!"
echo "You can now commit these changes:"
echo "  git add source/images/exercises/_01-ex-*.png"
echo "  git commit -m 'Update Chapter 1 exercise images with new plots'"
echo "  git push"

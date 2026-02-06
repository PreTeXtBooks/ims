#!/bin/bash
# Script to download Chapter 8 exercise images from GitHub issue assets
# Run this script when you have network access to GitHub assets

set -e

echo "Downloading Chapter 8 Exercise Images..."
echo "========================================"

# Image URLs from the GitHub issue
IMAGE1_URL="https://github.com/user-attachments/assets/52e2f717-8465-46bf-8476-586e5158192e"
IMAGE2_URL="https://github.com/user-attachments/assets/c5eace49-6d16-4d97-ac25-49b9e817abaa"
IMAGE3_URL="https://github.com/user-attachments/assets/f48c49ea-ae49-407a-9e8e-c5d19f7921bc"

# Output directory
OUTPUT_DIR="exercises/images"

# Download images
echo "1. Downloading meat consumption and life expectancy image..."
curl -L -o "$OUTPUT_DIR/meat-consumption-life-expectancy.png" "$IMAGE1_URL" || \
wget -O "$OUTPUT_DIR/meat-consumption-life-expectancy.png" "$IMAGE1_URL"

echo "2. Downloading arrival delays image..."
curl -L -o "$OUTPUT_DIR/arrival-delays.png" "$IMAGE2_URL" || \
wget -O "$OUTPUT_DIR/arrival-delays.png" "$IMAGE2_URL"

echo "3. Downloading movie returns by genre image..."
curl -L -o "$OUTPUT_DIR/movie-returns-genre.png" "$IMAGE3_URL" || \
wget -O "$OUTPUT_DIR/movie-returns-genre.png" "$IMAGE3_URL"

echo ""
echo "Download complete! Verifying..."
echo "========================================"

# Verify downloads
for img in "meat-consumption-life-expectancy.png" "arrival-delays.png" "movie-returns-genre.png"; do
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
echo "  git add exercises/images/*.png"
echo "  git commit -m 'Update Ch8 exercise images with actual data'"
echo "  git push"

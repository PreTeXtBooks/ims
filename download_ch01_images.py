#!/usr/bin/env python3
"""
Download Chapter 1 exercise images from GitHub issue assets.
Alternative to the bash script - may work better in some environments.
"""

import urllib.request
import sys
import os
from pathlib import Path

# Image URLs and target files
IMAGES = [
    {
        "name": "Q13: US Airports",
        "url": "https://github.com/user-attachments/assets/152060ff-6136-4b2f-b7f9-63bb437b1965",
        "file": "source/images/exercises/_01-ex-us-airports.png"
    },
    {
        "name": "Q14: UN Votes",
        "url": "https://github.com/user-attachments/assets/b9efa870-d920-4a10-9092-38ce93598c7f",
        "file": "source/images/exercises/_01-ex-un-votes.png"
    },
    {
        "name": "Q16: Shows on Netflix",
        "url": "https://github.com/user-attachments/assets/876d903b-b617-4049-918f-76d716835c0a",
        "file": "source/images/exercises/_01-ex-netflix-shows.png"
    },
    {
        "name": "Q19: Pet Names",
        "url": "https://github.com/user-attachments/assets/865ecf13-9a5b-40b1-8e2a-77131c946659",
        "file": "source/images/exercises/_01-ex-pet-names.png"
    }
]

def download_image(url, filepath):
    """Download an image from URL to filepath."""
    try:
        print(f"Downloading from {url}...", end=" ", flush=True)
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath) / 1024  # KB
        print(f"✓ ({size:.1f} KB)")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    print("Downloading Chapter 1 Exercise Images")
    print("=" * 60)
    print()
    
    # Ensure we're in the right directory
    if not os.path.exists("source/images/exercises"):
        print("ERROR: source/images/exercises directory not found!")
        print("Please run this script from the repository root.")
        sys.exit(1)
    
    success_count = 0
    fail_count = 0
    
    for img in IMAGES:
        print(f"{img['name']}:")
        if download_image(img["url"], img["file"]):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("=" * 60)
    print(f"Download complete: {success_count} succeeded, {fail_count} failed")
    print()
    
    if success_count > 0:
        print("Next steps:")
        print("  git add source/images/exercises/_01-ex-*.png")
        print("  git commit -m 'Update Chapter 1 exercise images'")
        print("  git push")
    
    if fail_count > 0:
        print("\nSome downloads failed. You may need to:")
        print("  - Check your internet connection")
        print("  - Try the bash script: ./download_ch01_images.sh")
        print("  - Manually download from the URLs above")
        sys.exit(1)

if __name__ == "__main__":
    main()

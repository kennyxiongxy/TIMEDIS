#!/usr/bin/env python3
import os
from PIL import Image
import shutil

def create_icon_set(source_path, output_path):
    sizes = [
        ('Icon-16.png', 16),
        ('Icon-16@2x.png', 32),
        ('Icon-32.png', 32),
        ('Icon-32@2x.png', 64),
        ('Icon-128.png', 128),
        ('Icon-128@2x.png', 256),
        ('Icon-256.png', 256),
        ('Icon-256@2x.png', 512),
        ('Icon-512.png', 512),
        ('Icon-512@2x.png', 1024),
    ]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        img = Image.open(source_path)
        print(f"Source image size: {img.size}")

        for filename, size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            output_file = os.path.join(output_path, filename)
            resized.save(output_file, 'PNG')
            print(f"Created {filename} ({size}x{size})")

        contents_json = '''{
  "images" : [
    {
      "filename" : "Icon-16.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "16x16"
    },
    {
      "filename" : "Icon-16@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "16x16"
    },
    {
      "filename" : "Icon-32.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "32x32"
    },
    {
      "filename" : "Icon-32@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "32x32"
    },
    {
      "filename" : "Icon-128.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "128x128"
    },
    {
      "filename" : "Icon-128@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "128x128"
    },
    {
      "filename" : "Icon-256.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "256x256"
    },
    {
      "filename" : "Icon-256@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "256x256"
    },
    {
      "filename" : "Icon-512.png",
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "512x512"
    },
    {
      "filename" : "Icon-512@2x.png",
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "512x512"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}'''

        with open(os.path.join(output_path, 'Contents.json'), 'w') as f:
            f.write(contents_json)

        print(f"\nIcon set created successfully at: {output_path}")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    source = 'app_icon.png'
    output = 'TimeDisplay/Assets.xcassets/AppIcon.appiconset'

    if os.path.exists(source):
        create_icon_set(source, output)
    else:
        print(f"Error: {source} not found")

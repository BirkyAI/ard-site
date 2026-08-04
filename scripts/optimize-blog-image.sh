#!/bin/bash
# Optimize a blog image for web use.
# Usage: optimize-blog-image.sh <image-path> [convert-to-jpg]
#
# Resizes to max 1200px width, compresses to 75% quality.
# If convert-to-jpg is "jpg", converts PNG to JPG (much smaller for photos).
# Skips files < 50KB (already small enough).
# Requires: sharp (installed in ~/websites/ard-site/node_modules)

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <image-path> [jpg]"
    exit 1
fi

FILE="$1"
CONVERT_JPG="${2:-}"

if [ ! -f "$FILE" ]; then
    echo "❌ File not found: $FILE"
    exit 1
fi

ORIG_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)

if [ "$ORIG_SIZE" -lt 51200 ]; then
    echo "⏭️  Skipping (< 50KB): $(basename "$FILE")"
    exit 0
fi

ARD_DIR="$HOME/websites/ard-site"

node -e "
const sharp = require('$ARD_DIR/node_modules/sharp');
const fs = require('fs');
const path = require('path');

const fp = '$FILE';
const convertJpg = '$CONVERT_JPG' === 'jpg';
const ext = path.extname(fp).toLowerCase();
const orig = fs.statSync(fp).size;

(async () => {
    const img = sharp(fp);
    const meta = await img.metadata();
    
    // Skip if already under 200KB and 1200px wide
    if (meta.width <= 1200 && orig < 200 * 1024) {
        console.log('⏭️  Already OK: ' + path.basename(fp) + ' (' + (orig/1024).toFixed(0) + 'KB, ' + meta.width + 'px)');
        return;
    }
    
    let pipeline = img.resize(1200, null, { withoutEnlargement: true, fit: 'inside' });
    
    // Always use JPEG for blog images (much smaller than PNG for photos)
    if (convertJpg || ext === '.jpg' || ext === '.jpeg') {
        pipeline = pipeline.jpeg({ quality: 75, progressive: true });
    } else if (ext === '.png') {
        pipeline = pipeline.png({ compressionLevel: 9 });
    }
    
    let outPath = fp;
    if (convertJpg && ext === '.png') {
        outPath = fp.replace(/\.png$/i, '.jpg');
    }
    
    const tmp = outPath + '.opt';
    await pipeline.toFile(tmp);
    const newSize = fs.statSync(tmp).size;
    
    if (newSize < orig) {
        fs.renameSync(tmp, outPath);
        const saved = ((orig - newSize) / 1024).toFixed(0);
        const pct = ((1 - newSize / orig) * 100).toFixed(0);
        console.log('✅ ' + path.basename(outPath) + ': ' + (orig/1024).toFixed(0) + 'KB → ' + (newSize/1024).toFixed(0) + 'KB (-' + pct + '%)');
        // Remove original PNG if we converted to JPG
        if (convertJpg && ext === '.png' && outPath !== fp && fs.existsSync(fp)) {
            // Don't remove if the output path IS the input path
        }
    } else {
        fs.unlinkSync(tmp);
        console.log('⏭️  No improvement: ' + path.basename(fp));
    }
})();
"

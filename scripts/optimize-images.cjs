#!/usr/bin/env node
/**
 * Batch Image Optimization Script for ARD Site
 * Compresses all JPG/PNG images to reasonable web sizes
 * Preserves directory structure, overwrites originals
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const IMAGES_DIR = path.join(__dirname, '../public/images');
const MAX_WIDTH = 1200; // Max width for web display
const JPEG_QUALITY = 75;
const PNG_QUALITY = 75;

// Track stats
let processed = 0;
let saved = 0;
let errors = 0;

async function optimizeImage(filePath) {
  try {
    const ext = path.extname(filePath).toLowerCase();
    const originalSize = fs.statSync(filePath).size;
    
    // Skip tiny files (<50KB)
    if (originalSize < 50 * 1024) return;
    
    const image = sharp(filePath);
    const metadata = await image.metadata();
    
    // Skip if already small enough
    if (metadata.width <= MAX_WIDTH && originalSize < 200 * 1024) return;
    
    let pipeline = image.resize(MAX_WIDTH, null, { 
      withoutEnlargement: true,
      fit: 'inside'
    });
    
    if (ext === '.jpg' || ext === '.jpeg') {
      pipeline = pipeline.jpeg({ quality: JPEG_QUALITY, mozjpeg: true });
    } else if (ext === '.png') {
      pipeline = pipeline.png({ quality: PNG_QUALITY, compressionLevel: 9 });
    }
    
    const tempPath = filePath + '.tmp';
    await pipeline.toFile(tempPath);
    
    const newSize = fs.statSync(tempPath).size;
    
    // Only replace if smaller
    if (newSize < originalSize) {
      fs.renameSync(tempPath, filePath);
      const savedKB = Math.round((originalSize - newSize) / 1024);
      console.log(`✅ ${path.basename(filePath)}: ${Math.round(originalSize/1024)}KB → ${Math.round(newSize/1024)}KB (saved ${savedKB}KB)`);
      saved += savedKB;
    } else {
      fs.unlinkSync(tempPath);
    }
    
    processed++;
  } catch (err) {
    console.error(`❌ ${path.basename(filePath)}: ${err.message}`);
    errors++;
  }
}

async function processDirectory(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      await processDirectory(fullPath);
    } else if (/\.(jpg|jpeg|png)$/i.test(entry.name)) {
      await optimizeImage(fullPath);
    }
  }
}

async function main() {
  console.log('🖼️  Optimizing images in', IMAGES_DIR);
  console.log('Target: max ' + MAX_WIDTH + 'px width, JPEG quality ' + JPEG_QUALITY + '%\n');
  
  await processDirectory(IMAGES_DIR);
  
  console.log('\n📊 Summary:');
  console.log(`   Processed: ${processed} images`);
  console.log(`   Total saved: ${Math.round(saved/1024)}MB`);
  console.log(`   Errors: ${errors}`);
}

main().catch(console.error);

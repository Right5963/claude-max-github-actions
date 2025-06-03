# Quick Implementation Guide: Image Tagging for Yahoo Auction Analysis

## Recommended Solution Stack

Based on the research, here's the optimal implementation for automated image tagging in your Yahoo auction workflow:

### Primary Stack
1. **WD14 Standalone** - Main tagging engine
2. **CLIP Interrogator** - Description generation
3. **Custom aggregation script** - Result combination

## Step-by-Step Implementation

### 1. WD14 Standalone Setup (15 minutes)

```bash
# Create project directory
mkdir yahoo-auction-tagger
cd yahoo-auction-tagger

# Clone WD14 standalone
git clone https://github.com/corkborg/wd14-tagger-standalone.git
cd wd14-tagger-standalone

# Set up environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. CLIP Interrogator Setup (10 minutes)

```bash
# Return to main directory
cd ..

# Set up CLIP environment
python -m venv clip_env
source clip_env/bin/activate

# Install CLIP Interrogator
pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu117
pip install clip-interrogator==0.5.4
```

### 3. Create Unified Processing Script

```python
#!/usr/bin/env python3
# yahoo_image_analyzer.py

import subprocess
import json
import os
import sys
from pathlib import Path

class YahooImageAnalyzer:
    def __init__(self):
        self.wd14_path = "./wd14-tagger-standalone"
        self.models = {
            'general': 'wd-vit-large-tagger-v3',
            'anime': 'wd-v1-4-vit-tagger.v3',
            'fast': 'wd14-convnextv2.v1'
        }
    
    def analyze_image(self, image_path, model_type='general', threshold=0.35):
        """Analyze single image with WD14 tagger"""
        model = self.models.get(model_type, self.models['general'])
        
        cmd = [
            'python', f'{self.wd14_path}/run.py',
            '--file', image_path,
            '--model', model,
            '--threshold', str(threshold),
            '--rawtag'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.wd14_path)
        
        if result.returncode == 0:
            # Parse WD14 output
            tags = self.parse_wd14_output(image_path)
            return {
                'image': image_path,
                'wd14_tags': tags,
                'model_used': model,
                'threshold': threshold
            }
        else:
            return {'error': result.stderr}
    
    def parse_wd14_output(self, image_path):
        """Parse WD14 tag output file"""
        tag_file = Path(image_path).with_suffix('.txt')
        if tag_file.exists():
            with open(tag_file, 'r', encoding='utf-8') as f:
                tags = f.read().strip()
                return [tag.strip() for tag in tags.split(',')]
        return []
    
    def analyze_batch(self, image_dir, model_type='general', threshold=0.35):
        """Analyze all images in directory"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        results = []
        
        for img_path in Path(image_dir).rglob('*'):
            if img_path.suffix.lower() in image_extensions:
                result = self.analyze_image(str(img_path), model_type, threshold)
                results.append(result)
                print(f"Processed: {img_path.name}")
        
        return results
    
    def export_results(self, results, output_file):
        """Export results to JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: python yahoo_image_analyzer.py <image_path_or_directory> [model_type] [threshold]")
        print("Model types: general, anime, fast")
        sys.exit(1)
    
    analyzer = YahooImageAnalyzer()
    input_path = sys.argv[1]
    model_type = sys.argv[2] if len(sys.argv) > 2 else 'general'
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35
    
    if os.path.isfile(input_path):
        # Single image
        result = analyzer.analyze_image(input_path, model_type, threshold)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif os.path.isdir(input_path):
        # Batch processing
        results = analyzer.analyze_batch(input_path, model_type, threshold)
        output_file = f"yahoo_analysis_{Path(input_path).name}.json"
        analyzer.export_results(results, output_file)
        print(f"Results saved to: {output_file}")
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    main()
```

### 4. Usage Examples

```bash
# Activate WD14 environment
cd yahoo-auction-tagger
source wd14-tagger-standalone/venv/bin/activate

# Single image analysis
python yahoo_image_analyzer.py /path/to/auction_image.jpg

# Batch analysis with anime model
python yahoo_image_analyzer.py /path/to/auction_images/ anime 0.3

# Fast processing for large batches
python yahoo_image_analyzer.py /path/to/auction_images/ fast 0.4
```

### 5. Advanced Integration Script

```python
#!/usr/bin/env python3
# advanced_yahoo_analyzer.py

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class AdvancedYahooAnalyzer:
    def __init__(self):
        self.wd14_path = "./wd14-tagger-standalone"
        self.clip_env = "./clip_env"
        
    def detect_image_type(self, image_path):
        """Detect if image is anime/manga style or real photo"""
        # Quick WD14 analysis to detect anime content
        cmd = [
            'python', f'{self.wd14_path}/run.py',
            '--file', image_path,
            '--model', 'wd14-convnextv2.v1',
            '--threshold', '0.5'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.wd14_path)
        
        if result.returncode == 0:
            tag_file = Path(image_path).with_suffix('.txt')
            if tag_file.exists():
                with open(tag_file, 'r') as f:
                    tags = f.read().lower()
                    anime_indicators = ['anime', 'manga', '1girl', '1boy', 'anime_style']
                    if any(indicator in tags for indicator in anime_indicators):
                        return 'anime'
        return 'general'
    
    def analyze_with_optimal_model(self, image_path):
        """Analyze image with automatically selected optimal model"""
        image_type = self.detect_image_type(image_path)
        
        if image_type == 'anime':
            model = 'wd-v1-4-vit-tagger.v3'
            threshold = 0.35
        else:
            model = 'wd-vit-large-tagger-v3'
            threshold = 0.4
        
        cmd = [
            'python', f'{self.wd14_path}/run.py',
            '--file', image_path,
            '--model', model,
            '--threshold', str(threshold)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.wd14_path)
        
        return {
            'image_type': image_type,
            'model_used': model,
            'threshold': threshold,
            'tags': self.parse_wd14_output(image_path)
        }
    
    def parse_wd14_output(self, image_path):
        """Parse WD14 output and return structured data"""
        tag_file = Path(image_path).with_suffix('.txt')
        if tag_file.exists():
            with open(tag_file, 'r', encoding='utf-8') as f:
                raw_tags = f.read().strip()
                tags = [tag.strip() for tag in raw_tags.split(',')]
                
                # Categorize tags
                character_tags = [t for t in tags if any(x in t for x in ['girl', 'boy', 'woman', 'man'])]
                object_tags = [t for t in tags if not any(x in t for x in ['girl', 'boy', 'woman', 'man', 'solo'])]
                
                return {
                    'all_tags': tags,
                    'character_tags': character_tags,
                    'object_tags': object_tags,
                    'tag_count': len(tags),
                    'confidence_level': 'high' if len(tags) > 10 else 'medium' if len(tags) > 5 else 'low'
                }
        return {}
    
    def generate_auction_summary(self, analysis_result):
        """Generate Yahoo auction optimized summary"""
        tags = analysis_result.get('tags', {})
        all_tags = tags.get('all_tags', [])
        
        # Extract key information for auction listings
        summary = {
            'main_subject': self.identify_main_subject(all_tags),
            'condition_indicators': self.extract_condition_tags(all_tags),
            'category_suggestions': self.suggest_categories(all_tags),
            'keyword_tags': all_tags[:15],  # Top 15 tags for keywords
            'description_text': self.generate_description(all_tags)
        }
        
        return summary
    
    def identify_main_subject(self, tags):
        """Identify the main subject/item in the image"""
        # Priority keywords for auction items
        priority_items = ['bag', 'watch', 'camera', 'book', 'toy', 'figure', 'electronics', 'clothing']
        
        for tag in tags:
            for item in priority_items:
                if item in tag.lower():
                    return tag
        
        return tags[0] if tags else 'unknown'
    
    def extract_condition_tags(self, tags):
        """Extract tags that indicate item condition"""
        condition_keywords = ['new', 'used', 'vintage', 'damaged', 'mint', 'worn', 'scratched']
        return [tag for tag in tags if any(keyword in tag.lower() for keyword in condition_keywords)]
    
    def suggest_categories(self, tags):
        """Suggest Yahoo auction categories based on tags"""
        category_mapping = {
            'anime': ['Collectibles', 'Anime'],
            'figure': ['Collectibles', 'Figures'],
            'book': ['Books', 'Manga'],
            'camera': ['Electronics', 'Cameras'],
            'watch': ['Accessories', 'Watches'],
            'bag': ['Fashion', 'Bags'],
            'toy': ['Toys', 'Games']
        }
        
        suggestions = []
        for tag in tags:
            for keyword, categories in category_mapping.items():
                if keyword in tag.lower():
                    suggestions.extend(categories)
        
        return list(set(suggestions))  # Remove duplicates
    
    def generate_description(self, tags):
        """Generate auction description from tags"""
        if not tags:
            return "Item for auction. Please see photos for details."
        
        # Create natural description from tags
        description_parts = []
        
        # Subject
        main_items = [t for t in tags[:5] if not any(x in t for x in ['solo', '1girl', '1boy'])]
        if main_items:
            description_parts.append(f"Features: {', '.join(main_items[:3])}")
        
        # Additional details
        detail_tags = tags[5:10]
        if detail_tags:
            description_parts.append(f"Details: {', '.join(detail_tags)}")
        
        return ". ".join(description_parts) + "."

def main():
    analyzer = AdvancedYahooAnalyzer()
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_yahoo_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Perform analysis
    analysis = analyzer.analyze_with_optimal_model(image_path)
    
    # Generate auction summary
    summary = analyzer.generate_auction_summary(analysis)
    
    # Create final report
    report = {
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path,
        'analysis': analysis,
        'auction_summary': summary
    }
    
    # Save report
    output_file = f"auction_analysis_{Path(image_path).stem}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Report saved to: {output_file}")
    print(f"\nMain Subject: {summary['main_subject']}")
    print(f"Categories: {', '.join(summary['category_suggestions'])}")
    print(f"Keywords: {', '.join(summary['keyword_tags'][:5])}...")

if __name__ == "__main__":
    import sys
    main()
```

### 6. Batch Processing Script

```bash
#!/bin/bash
# batch_yahoo_analysis.sh

WATCH_DIR="$1"
OUTPUT_DIR="$2"

if [ -z "$WATCH_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <watch_directory> <output_directory>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Starting batch analysis of $WATCH_DIR"
echo "Output will be saved to $OUTPUT_DIR"

# Process all images in directory
find "$WATCH_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) | while read -r image; do
    echo "Processing: $(basename "$image")"
    
    # Run analysis
    python advanced_yahoo_analyzer.py "$image"
    
    # Move result to output directory
    result_file="auction_analysis_$(basename "${image%.*}").json"
    if [ -f "$result_file" ]; then
        mv "$result_file" "$OUTPUT_DIR/"
    fi
    
    # Clean up temporary tag files
    rm -f "${image%.*}.txt"
done

echo "Batch processing complete. Results in $OUTPUT_DIR"
```

### 7. API Service (Optional)

```python
#!/usr/bin/env python3
# yahoo_tagger_api.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import tempfile
import os
from advanced_yahoo_analyzer import AdvancedYahooAnalyzer

app = FastAPI(title="Yahoo Auction Image Tagger API")
analyzer = AdvancedYahooAnalyzer()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image for Yahoo auction"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name
    
    try:
        # Perform analysis
        analysis = analyzer.analyze_with_optimal_model(tmp_path)
        summary = analyzer.generate_auction_summary(analysis)
        
        result = {
            'filename': file.filename,
            'analysis': analysis,
            'auction_summary': summary
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary files
        os.unlink(tmp_path)
        tag_file = tmp_path.replace(os.path.splitext(tmp_path)[1], '.txt')
        if os.path.exists(tag_file):
            os.unlink(tag_file)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Testing the Implementation

### Test with Sample Images

```bash
# Test single image
python yahoo_image_analyzer.py test_images/sample_auction_item.jpg

# Test batch processing
python yahoo_image_analyzer.py test_images/ general 0.35

# Test advanced analyzer
python advanced_yahoo_analyzer.py test_images/anime_figure.jpg
```

### Performance Expectations

- **Single Image**: 1-5 seconds
- **Batch (100 images)**: 5-15 minutes
- **Memory Usage**: 2-4GB RAM
- **GPU Acceleration**: 3-5x faster with CUDA

## Next Steps

1. **Test with your auction images**
2. **Adjust thresholds based on results**
3. **Customize category mappings**
4. **Integrate with your existing workflow**
5. **Consider deploying API service for real-time processing**

This implementation provides a solid foundation for automated Yahoo auction image analysis with minimal setup time and maximum flexibility.
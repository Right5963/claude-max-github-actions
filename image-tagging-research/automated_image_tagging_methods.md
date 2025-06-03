# Automated Image Tagging and Feature Extraction Methods

## Overview
This document provides a comprehensive analysis of available methods for automated image tagging and feature extraction, with focus on implementation for Yahoo auction image analysis workflows.

## 1. Stable Diffusion WebUI Tagger Extensions

### 1.1 WD14 Tagger Extension (Primary Recommendation)

**Repository**: `https://github.com/toriato/stable-diffusion-webui-wd14-tagger`

#### Installation Requirements
- AUTOMATIC1111 WebUI or Reforge WebUI
- Python 3.7-3.12
- GPU with CUDA support (recommended)

#### Features
- Multi-model support (WD14, DeepDanbooru v3/v4, E621)
- Automatic model downloading from HuggingFace
- Booru-style tag generation
- Single and batch image processing

#### API Integration
```bash
# Extension URL installation
Extensions -> Install from URL -> https://github.com/toriato/stable-diffusion-webui-wd14-tagger
```

#### Input/Output Formats
- **Input**: JPEG, PNG, WebP images
- **Output**: Comma-separated Danbooru tags with confidence scores
- **Example Output**: "1girl, solo, smile, bow, jacket, :d, controller, hairband, holding, bowtie, bangs, blazer, shirt, purple eyes"

#### Accuracy & Speed
- **Speed**: 2-5 seconds per image (GPU), 10-20 seconds (CPU)
- **Accuracy**: High for anime/illustration content, moderate for real photos
- **Confidence Scores**: Available for tag relevance assessment

#### Automation Potential
- **High**: WebUI API integration possible
- **Batch Processing**: Built-in support for multiple images
- **Real-time**: Possible via API calls

#### Integration Complexity
- **Low-Medium**: Requires WebUI installation
- **API Access**: Via WebUI's standard HTTP API

### 1.2 Reforge/A1111 WebUI Integration

#### Features
- Compatible with both AUTOMATIC1111 and Reforge
- Extension ecosystem support
- API endpoint access via WebUI

#### API Endpoints
```python
# Example API call structure
POST /api/v1/interrogate
{
    "image": "base64_encoded_image",
    "model": "wd14-convnextv2-v1"
}
```

## 2. WD14 (Waifu Diffusion 14) Standalone Implementations

### 2.1 wd14-tagger-standalone (Recommended)

**Repository**: `https://github.com/corkborg/wd14-tagger-standalone`

#### Installation Requirements
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Command Syntax
```bash
python run.py [options] --file FILE | --dir DIR

# Options:
--threshold THRESHOLD     # Prediction threshold (default: 0.35)
--ext EXT                # Caption file extension (default: .txt)
--overwrite              # Overwrite existing caption files
--cpu                    # Use CPU only
--rawtag                 # Raw model output
--recursive              # Recursive directory search
--exclude-tag t1,t2,t3   # Exclude specific tags
--model MODELNAME        # Model selection
```

#### Available Models
```bash
# Latest models (2025)
--model camie-tagger

# Large models (2024)
--model wd-vit-large-tagger-v3
--model wd-eva02-large-tagger-v3

# Standard v3 models (2024)
--model wd-v1-4-vit-tagger.v3
--model wd-v1-4-convnext-tagger.v3
--model wd-v1-4-swinv2-tagger.v3

# v2 models (2023)
--model wd-v1-4-moat-tagger.v2
--model wd14-vit.v2
--model wd14-convnext.v2

# v1 models (2022)
--model wd14-convnextv2.v1  # Default, most popular
```

#### Accuracy & Speed Characteristics
- **Speed**: 1-3 seconds per image (GPU), 5-15 seconds (CPU)
- **Accuracy**: Excellent for anime content, good for general images
- **Model Size**: 50-500MB depending on model variant

#### Batch Processing Example
```bash
# Process entire directory
python run.py --dir /path/to/images --recursive --threshold 0.4

# Single file processing
python run.py --file image.jpg --model wd-vit-large-tagger-v3
```

### 2.2 wd14-tagger-server (API Server)

**Repository**: `https://github.com/LlmKira/wd14-tagger-server`

#### Features
- FastAPI-based web service
- PM2 deployment support
- REST API interface

#### API Usage
```bash
curl -X 'POST' \
  'http://127.0.0.1:5010/upload?general_threshold=0.35&character_threshold=0.85' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.png;type=image/png'
```

## 3. CLIP-Based Interrogation Methods

### 3.1 CLIP Interrogator

**Repository**: `https://github.com/pharmapsychotic/clip-interrogator`

#### Installation
```bash
python3 -m venv ci_env
source ci_env/bin/activate
pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu117
pip install clip-interrogator==0.5.4
```

#### Features
- BLIP + CLIP model combination
- Text prompt optimization for given images
- Multiple model support via OpenCLIP

#### Configuration Options
```python
from clip_interrogator import Config, Interrogator

config = Config()
config.clip_model_name = 'ViT-L-14/openai'
config.cache_path = 'cache'
config.apply_low_vram_defaults()  # Reduces VRAM from 6.3GB to 2.7GB

ci = Interrogator(config)
```

#### Command Line Usage
```python
# Basic interrogation
result = ci.interrogate(image)
```

#### Accuracy & Speed
- **Speed**: 3-8 seconds per image (depends on model)
- **VRAM**: 2.7GB (low VRAM mode) to 6.3GB (full mode)
- **Accuracy**: Excellent for natural language descriptions

### 3.2 OpenCLIP

**Repository**: `https://github.com/mlfoundations/open_clip`

#### Installation & Usage
```python
import open_clip

# List available models
open_clip.list_pretrained()

# Load model from HuggingFace
model, preprocess = open_clip.create_model_from_pretrained(
    'hf-hub:laion/CLIP-ViT-g-14-laion2B-s12B-b42K'
)
tokenizer = open_clip.get_tokenizer(
    'hf-hub:laion/CLIP-ViT-g-14-laion2B-s12B-b42K'
)
```

#### Command Line Training
```bash
python -m open_clip_train.main \
    --save-frequency 1 \
    --zeroshot-frequency 1 \
    --report-to tensorboard \
    --train-data="/path/to/train_data.csv" \
    --val-data="/path/to/validation_data.csv"
```

## 4. DeepDanbooru and Anime-Focused Taggers

### 4.1 DeepDanbooru-Tagger (Simplified CLI)

**Repository**: `https://github.com/ShinChven/deepdanbooru-tagger`

#### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Download deepdanbooru-v4-20200814-sgd-e30 model manually
```

#### Command Syntax
```bash
python cli.py /path/to/image/or/folder \
    --size 10 \
    --append "custom,tags" \
    --prepend "prefix,tags" \
    --interrogate
```

#### Features
- Simplified command-line interface
- Custom tag addition/prepending
- Detailed interrogation files
- Model: DeepDanbooru v4

### 4.2 Official DeepDanbooru

**Repository**: `https://github.com/KichangKim/DeepDanbooru`

#### Installation
```bash
# Basic installation
pip install deepdanbooru

# With TensorFlow
pip install deepdanbooru[tensorflow]
```

#### Setup Process
```bash
# 1. Create project
deepdanbooru create-project [project_folder]

# 2. Download tags (requires Danbooru account)
deepdanbooru download-tags [project_folder] \
    --username [username] \
    --api-key [api_key]

# 3. Evaluate images
deepdanbooru evaluate [image_path] \
    --project-path [project_folder] \
    --allow-folder
```

#### Docker Installation
```bash
docker run --rm -it -v /local/images/:/app/data \
    kamuri/deepdanbooru evaluate \
    --project-path "/app/model" \
    "/app/data/" \
    --allow-folder
```

#### Accuracy & Speed
- **Speed**: 2-5 seconds per image
- **Accuracy**: Excellent for anime/manga content
- **Specialization**: Danbooru tag system

## 5. Commercial APIs and Cloud Services

### 5.1 Imagga API

**Website**: `https://imagga.com/`

#### Features
- Comprehensive tagging API
- Batch processing support
- 50+ language support
- Color extraction

#### Command Line Usage
```bash
python tag_images.py <input_folder> <output_folder> \
    --language=<language> \
    --verbose=<verbose> \
    --merged-output=<merged_output> \
    --include-colors=<include_colors>
```

#### API Functions
- `upload_image()`: Image upload
- `tag_image()`: Tag generation
- `extract_colors()`: Color analysis

#### Pricing
- Free tier: 1,000 API calls/month
- Paid plans: $19-$299/month

### 5.2 Google Cloud Vision API

#### Features
- Enterprise-scale batch processing
- Multiple annotation types
- Offline/asynchronous processing
- JSON output to Cloud Storage

#### Batch Processing
```python
# Batch annotation request
{
    "requests": [
        {
            "image": {"source": {"imageUri": "gs://bucket/image1.jpg"}},
            "features": [{"type": "LABEL_DETECTION", "maxResults": 50}]
        }
    ],
    "outputConfig": {
        "gcsDestination": {"uri": "gs://output-bucket/"}
    }
}
```

#### Pricing
- $1.50 per 1,000 images (Label Detection)
- Free tier: 1,000 units/month

## 6. Integration and Workflow Recommendations

### 6.1 For Yahoo Auction Image Analysis

#### Recommended Stack
1. **Primary**: WD14 Standalone + CLIP Interrogator
2. **Backup**: DeepDanbooru for anime items
3. **Commercial**: Imagga API for high-volume processing

#### Workflow Implementation
```bash
#!/bin/bash
# image_analysis_pipeline.sh

IMAGE_PATH=$1
OUTPUT_DIR=$2

# 1. WD14 Tagging
python wd14-tagger/run.py --file "$IMAGE_PATH" \
    --model wd-vit-large-tagger-v3 \
    --threshold 0.3

# 2. CLIP Interrogation for descriptions
python clip_interrogate.py "$IMAGE_PATH"

# 3. Combine results
python combine_tags.py "$IMAGE_PATH" "$OUTPUT_DIR"
```

### 6.2 Real-time Processing Setup

#### FastAPI Service Example
```python
from fastapi import FastAPI, File, UploadFile
import subprocess

app = FastAPI()

@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    # Save uploaded file
    with open(f"temp/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    
    # Run WD14 tagger
    result = subprocess.run([
        "python", "wd14-tagger/run.py",
        "--file", f"temp/{file.filename}",
        "--model", "wd-vit-large-tagger-v3"
    ], capture_output=True, text=True)
    
    return {"tags": result.stdout}
```

### 6.3 Batch Processing Automation

#### Directory Monitoring
```python
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_file and event.src_path.endswith(('.jpg', '.png')):
            # Process new image
            subprocess.run([
                "python", "wd14-tagger/run.py",
                "--file", event.src_path
            ])

observer = Observer()
observer.schedule(ImageHandler(), "/watch/directory", recursive=True)
observer.start()
```

## 7. Performance Comparison

| Method | Speed (GPU) | Speed (CPU) | Accuracy | Setup Complexity | Cost |
|--------|------------|------------|----------|------------------|------|
| WD14 Standalone | 1-3s | 5-15s | Excellent | Low | Free |
| CLIP Interrogator | 3-8s | 15-30s | Very Good | Medium | Free |
| DeepDanbooru | 2-5s | 10-20s | Excellent (Anime) | Medium | Free |
| Imagga API | <1s | <1s | Good | Very Low | $19+/month |
| Google Vision | <1s | <1s | Very Good | Low | $1.50/1k |

## 8. Implementation Roadmap

### Phase 1: Basic Setup (1-2 days)
1. Install WD14 standalone tagger
2. Set up CLIP Interrogator
3. Test with sample Yahoo auction images

### Phase 2: Integration (2-3 days)
1. Create unified processing script
2. Implement batch processing
3. Set up result aggregation

### Phase 3: Automation (3-5 days)
1. Deploy FastAPI service
2. Implement directory monitoring
3. Create real-time processing pipeline

### Phase 4: Optimization (Ongoing)
1. Fine-tune model selection based on image types
2. Implement caching for repeated analyses
3. Add quality control and validation

## Conclusion

For Yahoo auction image analysis, the recommended approach is:

1. **Primary Engine**: WD14 Standalone (wd-vit-large-tagger-v3) for comprehensive tagging
2. **Secondary Engine**: CLIP Interrogator for natural language descriptions
3. **Specialized Cases**: DeepDanbooru for anime/manga items
4. **High-Volume Fallback**: Imagga API for commercial scalability

This combination provides the best balance of accuracy, speed, cost-effectiveness, and automation potential for the specific use case of auction image analysis.
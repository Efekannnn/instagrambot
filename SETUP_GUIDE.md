# 🚀 Setup Guide for Industrial Defect Detection System

This guide will walk you through setting up the project step-by-step.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) NVIDIA GPU with CUDA for better performance
- (Optional) Webcam for real-time demos

---

## 🔧 Installation Steps

### 1. System Preparation

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

#### On macOS:
```bash
brew install python@3.10
brew install opencv
```

#### On Windows:
- Download and install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### 2. Clone or Download Project

```bash
# If using git
git clone https://github.com/yourusername/industrial-defect-detection.git
cd industrial-defect-detection

# Or download and extract the ZIP file
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This may take several minutes as it downloads PyTorch and other large packages.

### 5. Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "from ultralytics import YOLO; print('YOLO: OK')"
```

If all commands succeed without errors, you're ready to go!

---

## 🎯 Quick Start

### Test 1: Run Image Processing Demo

```bash
python demo.py --processing
```

This will:
- Generate sample defect images
- Apply advanced OpenCV processing
- Save results to `output/image_processing/`

### Test 2: Run Image Comparison Demo

```bash
python demo.py --comparison
```

This demonstrates image difference detection.

### Test 3: Basic Detection Script

Create a simple test script:

```python
# test_basic.py
from src.image_processor import ImageProcessor
import cv2
import numpy as np

# Create sample image
image = np.ones((480, 640, 3), dtype=np.uint8) * 200
cv2.circle(image, (320, 240), 50, (100, 100, 100), -1)

# Process
processor = ImageProcessor()
result = processor.segment_defects(image)

print(f"Found {len(result.contours)} defects")
print("Setup successful!")
```

Run it:
```bash
python test_basic.py
```

---

## 🤖 Setting Up YOLO Detection

### Option 1: Use Pretrained YOLO (For Testing)

The system will automatically download YOLOv8 weights on first use:

```python
from src.defect_detector import DefectDetector

detector = DefectDetector("config.yaml")
# First run downloads yolov8n.pt automatically
```

### Option 2: Train Custom Model (For Production)

#### Step 1: Prepare Your Dataset

Organize your dataset in YOLO format:
```
dataset/
├── images/
│   ├── train/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    ├── val/
    └── test/
```

Each label file contains: `class_id center_x center_y width height`

#### Step 2: Run Training

```bash
python train.py
```

Follow the prompts and monitor training progress.

#### Step 3: Update Configuration

After training, update `config.yaml`:
```yaml
model:
  weights: "runs/detect/defect_detection/weights/best.pt"
```

---

## 🎮 Running Demos

### All Demos
```bash
python demo.py --all
```

### Individual Demos

**Image Processing:**
```bash
python demo.py --processing
```

**YOLO Detection:**
```bash
python demo.py --yolo
```

**Batch Processing:**
```bash
python demo.py --batch
```

**Real-time Webcam:**
```bash
python demo.py --realtime
```

**Image Comparison:**
```bash
python demo.py --comparison
```

---

## 🔧 Configuration

### Basic Configuration

Edit `config.yaml` to adjust settings:

```yaml
# Lower confidence for more detections (may have false positives)
model:
  confidence_threshold: 0.15

# Higher confidence for fewer, more certain detections
model:
  confidence_threshold: 0.5

# Adjust defect size filters
detection:
  min_area: 50      # Smaller defects
  max_area: 100000  # Larger defects
```

### Performance Tuning

For **faster processing** (lower quality):
```yaml
model:
  architecture: "yolov8n"  # Nano - fastest
  image_size: 416           # Smaller size

preprocessing:
  denoise: false
  enhance_contrast: false
```

For **better accuracy** (slower):
```yaml
model:
  architecture: "yolov8l"  # Large - most accurate
  image_size: 1280          # Larger size

preprocessing:
  denoise: true
  enhance_contrast: true
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'torch'"
**Solution:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

For GPU support:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Issue: "Could not open video source"
**Solution:**
- Make sure webcam is connected
- Try different source indices: `source=0`, `source=1`, etc.
- Check camera permissions

### Issue: "CUDA out of memory"
**Solution:**
- Reduce batch size in config
- Use smaller model (yolov8n instead of yolov8l)
- Reduce image size

### Issue: Import errors on Linux
**Solution:**
```bash
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

### Issue: Slow CPU performance
**Solution:**
- Install with GPU support if you have NVIDIA GPU
- Use smaller model (yolov8n)
- Disable preprocessing in config

---

## 📊 Testing Your Setup

### Complete System Test

Create `test_system.py`:

```python
import cv2
import numpy as np
from src.defect_detector import DefectDetector
from src.image_processor import ImageProcessor
from src.inference import InferenceEngine

print("Testing Industrial Defect Detection System\n")

# Test 1: Image Processor
print("Test 1: Image Processor...")
processor = ImageProcessor()
test_img = np.ones((480, 640, 3), dtype=np.uint8) * 200
result = processor.segment_defects(test_img)
print(f"  ✓ Image processing working\n")

# Test 2: Defect Detector
print("Test 2: Defect Detector...")
try:
    detector = DefectDetector("config.yaml")
    print(f"  ✓ Detector initialized")
    print(f"  ✓ Using device: {detector.device}\n")
except Exception as e:
    print(f"  ⚠ Warning: {e}\n")

# Test 3: Inference Engine
print("Test 3: Inference Engine...")
try:
    engine = InferenceEngine(detector)
    print(f"  ✓ Inference engine ready\n")
except Exception as e:
    print(f"  ⚠ Warning: {e}\n")

print("="*50)
print("Setup test completed!")
print("="*50)
```

Run:
```bash
python test_system.py
```

---

## 🚀 Next Steps

1. **Explore Examples**: Check out the demo scripts
2. **Customize Config**: Adjust `config.yaml` for your use case
3. **Prepare Dataset**: Gather and label your defect images
4. **Train Model**: Run `train.py` with your dataset
5. **Deploy**: Integrate into your application

---

## 📚 Additional Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

## 💡 Tips for Best Results

1. **Lighting**: Ensure consistent lighting in your images
2. **Image Quality**: Use high-resolution images for training
3. **Dataset Balance**: Have similar numbers of examples for each defect type
4. **Augmentation**: Use data augmentation to improve robustness
5. **Fine-tuning**: Start with pretrained weights and fine-tune on your data

---

## 📧 Need Help?

If you encounter issues:
1. Check this guide first
2. Review the main README.md
3. Search existing issues on GitHub
4. Create a new issue with details about your problem

---

**Happy Detecting! 🎯**
"""
Training Script for Custom Defect Detection Model
This script demonstrates how to train a YOLO model on custom defect dataset
"""

import yaml
from pathlib import Path
from ultralytics import YOLO
import torch


def prepare_dataset_yaml(dataset_path: str, classes: list):
    """
    Create dataset YAML file for YOLO training.
    
    Args:
        dataset_path: Root path of dataset
        classes: List of class names
    """
    dataset_config = {
        'path': str(Path(dataset_path).absolute()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(classes),
        'names': classes
    }
    
    with open('dataset.yaml', 'w') as f:
        yaml.dump(dataset_config, f)
    
    print("Dataset configuration created: dataset.yaml")


def train_model(
    model_size: str = 'yolov8n',
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    device: str = None
):
    """
    Train YOLO model on custom defect dataset.
    
    Args:
        model_size: Model size (yolov8n/s/m/l/x)
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size
        device: Device to use (None for auto-detect)
    """
    # Auto-detect device
    if device is None:
        device = '0' if torch.cuda.is_available() else 'cpu'
    
    print(f"Training Configuration:")
    print(f"  Model: {model_size}")
    print(f"  Epochs: {epochs}")
    print(f"  Image Size: {imgsz}")
    print(f"  Batch Size: {batch}")
    print(f"  Device: {device}")
    
    # Initialize model
    model = YOLO(f'{model_size}.pt')
    
    # Train model
    results = model.train(
        data='dataset.yaml',
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        name='defect_detection',
        pretrained=True,
        optimizer='AdamW',
        lr0=0.001,
        momentum=0.9,
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
        copy_paste=0.0,
        save=True,
        save_period=10,
        val=True,
        plots=True
    )
    
    print("\nTraining completed!")
    print(f"Best model saved to: runs/detect/defect_detection/weights/best.pt")
    
    return results


def validate_model(model_path: str):
    """
    Validate trained model.
    
    Args:
        model_path: Path to trained model weights
    """
    print(f"\nValidating model: {model_path}")
    
    model = YOLO(model_path)
    
    # Validate on test set
    results = model.val(
        data='dataset.yaml',
        split='test',
        save_json=True,
        save_hybrid=True
    )
    
    print("\nValidation Results:")
    print(f"  mAP@0.5: {results.box.map50:.4f}")
    print(f"  mAP@0.5:0.95: {results.box.map:.4f}")
    print(f"  Precision: {results.box.mp:.4f}")
    print(f"  Recall: {results.box.mr:.4f}")


def export_model(model_path: str, format: str = 'onnx'):
    """
    Export trained model to various formats.
    
    Args:
        model_path: Path to trained model
        format: Export format (onnx, torchscript, tflite, etc.)
    """
    print(f"\nExporting model to {format}...")
    
    model = YOLO(model_path)
    model.export(format=format, imgsz=640, optimize=True)
    
    print(f"Model exported successfully!")


def main():
    """
    Main training pipeline.
    
    This is a template script. Modify according to your dataset structure.
    """
    print("="*60)
    print("Custom Defect Detection Model - Training Pipeline")
    print("="*60)
    
    # Configuration
    DATASET_PATH = "./dataset"  # Update with your dataset path
    CLASSES = [
        "scratch",
        "dent", 
        "crack",
        "discoloration",
        "missing_part",
        "deformation"
    ]
    
    # Step 1: Prepare dataset configuration
    print("\nStep 1: Preparing dataset configuration...")
    prepare_dataset_yaml(DATASET_PATH, CLASSES)
    
    # Step 2: Train model
    print("\nStep 2: Training model...")
    print("\nNote: This requires a properly formatted dataset in YOLO format:")
    print("  dataset/")
    print("    ├── images/")
    print("    │   ├── train/")
    print("    │   ├── val/")
    print("    │   └── test/")
    print("    └── labels/")
    print("        ├── train/")
    print("        ├── val/")
    print("        └── test/")
    
    response = input("\nDo you have a prepared dataset? (y/n): ")
    
    if response.lower() == 'y':
        # Train model
        results = train_model(
            model_size='yolov8n',  # Use 'yolov8s' or 'yolov8m' for better accuracy
            epochs=100,
            imgsz=640,
            batch=16
        )
        
        # Step 3: Validate
        print("\nStep 3: Validating model...")
        validate_model('runs/detect/defect_detection/weights/best.pt')
        
        # Step 4: Export
        print("\nStep 4: Exporting model...")
        export_model('runs/detect/defect_detection/weights/best.pt', format='onnx')
        
        print("\n" + "="*60)
        print("Training pipeline completed!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review training plots in: runs/detect/defect_detection/")
        print("2. Update config.yaml to use your trained model")
        print("3. Test the model with: python demo.py --yolo")
    else:
        print("\nPlease prepare your dataset first.")
        print("Refer to the README for dataset preparation guidelines.")


if __name__ == "__main__":
    main()
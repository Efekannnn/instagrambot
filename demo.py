"""
Demo Script for Industrial Defect Detection System
Demonstrates the capabilities of the defect detection system
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
import sys

from src.defect_detector import DefectDetector
from src.image_processor import ImageProcessor
from src.inference import InferenceEngine


def create_sample_defect_images(output_dir: str = "sample_images"):
    """
    Create sample images with simulated defects for demonstration.
    
    Args:
        output_dir: Directory to save sample images
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("Generating sample defect images...")
    
    # Sample 1: Scratch defect
    img1 = np.ones((480, 640, 3), dtype=np.uint8) * 200
    cv2.line(img1, (100, 100), (400, 300), (50, 50, 50), 3)
    cv2.line(img1, (200, 150), (500, 250), (60, 60, 60), 2)
    cv2.imwrite(str(output_path / "scratch_defect.jpg"), img1)
    
    # Sample 2: Circular defect (dent/hole)
    img2 = np.ones((480, 640, 3), dtype=np.uint8) * 180
    cv2.circle(img2, (320, 240), 50, (100, 100, 100), -1)
    cv2.circle(img2, (450, 150), 30, (90, 90, 90), -1)
    cv2.imwrite(str(output_path / "dent_defect.jpg"), img2)
    
    # Sample 3: Crack defect
    img3 = np.ones((480, 640, 3), dtype=np.uint8) * 190
    pts = np.array([[100, 240], [200, 250], [300, 230], [400, 245], [500, 240]], np.int32)
    cv2.polylines(img3, [pts], False, (40, 40, 40), 2)
    # Add some noise
    noise = np.random.randint(-20, 20, img3.shape, dtype=np.int16)
    img3 = np.clip(img3.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(str(output_path / "crack_defect.jpg"), img3)
    
    # Sample 4: Discoloration defect
    img4 = np.ones((480, 640, 3), dtype=np.uint8) * 170
    cv2.ellipse(img4, (320, 240), (100, 60), 0, 0, 360, (120, 100, 80), -1)
    cv2.ellipse(img4, (150, 350), (80, 50), 45, 0, 360, (140, 110, 90), -1)
    cv2.imwrite(str(output_path / "discoloration_defect.jpg"), img4)
    
    # Sample 5: Complex multi-defect
    img5 = np.ones((480, 640, 3), dtype=np.uint8) * 185
    cv2.circle(img5, (150, 150), 40, (80, 80, 80), -1)
    cv2.line(img5, (300, 100), (500, 400), (50, 50, 50), 3)
    cv2.rectangle(img5, (400, 300), (550, 400), (100, 100, 100), -1)
    cv2.imwrite(str(output_path / "multi_defect.jpg"), img5)
    
    print(f"Sample images saved to: {output_dir}/")
    return list(output_path.glob("*.jpg"))


def demo_image_processing():
    """Demonstrate advanced image processing capabilities."""
    print("\n" + "="*60)
    print("DEMO 1: Advanced Image Processing with OpenCV")
    print("="*60)
    
    processor = ImageProcessor()
    
    # Create sample images
    sample_paths = create_sample_defect_images()
    
    # Process each image
    for img_path in sample_paths[:3]:  # Process first 3
        print(f"\nProcessing: {img_path.name}")
        
        image = cv2.imread(str(img_path))
        
        # Apply full segmentation pipeline
        result = processor.segment_defects(image)
        
        # Visualize
        vis = processor.visualize_segmentation(result)
        
        # Save results
        output_dir = Path("output/image_processing")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"processed_{img_path.name}"
        cv2.imwrite(str(output_path), vis)
        
        print(f"  Found {len(result.contours)} potential defects")
        print(f"  Result saved to: {output_path}")


def demo_yolo_detection():
    """Demonstrate YOLO-based defect detection."""
    print("\n" + "="*60)
    print("DEMO 2: YOLO-based Defect Detection")
    print("="*60)
    
    # Initialize detector
    try:
        detector = DefectDetector("config.yaml")
    except Exception as e:
        print(f"Note: Using pretrained YOLO for demo (custom training needed for actual defects)")
        print(f"Error: {e}")
        return
    
    # Create sample images if not exist
    sample_dir = Path("sample_images")
    if not sample_dir.exists() or not list(sample_dir.glob("*.jpg")):
        sample_paths = create_sample_defect_images()
    else:
        sample_paths = list(sample_dir.glob("*.jpg"))
    
    # Process images
    for img_path in sample_paths:
        print(f"\nProcessing: {img_path.name}")
        
        try:
            annotated, detections = detector.process_image(str(img_path))
            print(f"  Detected {len(detections)} defects")
            
            for i, det in enumerate(detections):
                print(f"    Defect {i+1}: {det['class_name']} (confidence: {det['confidence']:.2f})")
        except Exception as e:
            print(f"  Error: {e}")


def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n" + "="*60)
    print("DEMO 3: Batch Processing & Performance Metrics")
    print("="*60)
    
    try:
        detector = DefectDetector("config.yaml")
        engine = InferenceEngine(detector)
        
        # Process directory
        sample_dir = "sample_images"
        if not Path(sample_dir).exists():
            create_sample_defect_images(sample_dir)
        
        results = engine.process_directory(sample_dir, save_results=True)
        
        # Generate report
        engine.generate_report(results, "detection_report.json")
        
    except Exception as e:
        print(f"Demo requires YOLO model setup: {e}")


def demo_real_time():
    """Demonstrate real-time detection capabilities."""
    print("\n" + "="*60)
    print("DEMO 4: Real-time Detection (Webcam)")
    print("="*60)
    
    print("\nThis demo requires a webcam.")
    response = input("Do you want to proceed? (y/n): ")
    
    if response.lower() != 'y':
        print("Skipping real-time demo.")
        return
    
    try:
        detector = DefectDetector("config.yaml")
        engine = InferenceEngine(detector)
        
        print("\nStarting real-time detection...")
        print("Press 'q' to quit, 's' to save screenshot")
        
        engine.real_time_inference(source=0, display=True)
        
    except Exception as e:
        print(f"Error in real-time demo: {e}")


def demo_comparison():
    """Demonstrate image comparison for defect detection."""
    print("\n" + "="*60)
    print("DEMO 5: Image Comparison for Defect Detection")
    print("="*60)
    
    processor = ImageProcessor()
    
    # Create reference and test images
    reference = np.ones((480, 640, 3), dtype=np.uint8) * 200
    test = reference.copy()
    
    # Add defects to test image
    cv2.circle(test, (320, 240), 40, (100, 100, 100), -1)
    cv2.line(test, (100, 100), (400, 300), (50, 50, 50), 3)
    
    # Compare
    diff, similarity = processor.compare_images(reference, test)
    
    print(f"\nSimilarity Score: {similarity:.4f}")
    print(f"Difference: {(1-similarity)*100:.2f}%")
    
    # Save results
    output_dir = Path("output/comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cv2.imwrite(str(output_dir / "reference.jpg"), reference)
    cv2.imwrite(str(output_dir / "test.jpg"), test)
    cv2.imwrite(str(output_dir / "difference.jpg"), diff)
    
    print(f"Results saved to: {output_dir}/")


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(
        description="Industrial Defect Detection System - Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo.py --all                    # Run all demos
  python demo.py --processing             # Image processing demo
  python demo.py --yolo                   # YOLO detection demo
  python demo.py --batch                  # Batch processing demo
  python demo.py --realtime               # Real-time webcam demo
  python demo.py --comparison             # Image comparison demo
        """
    )
    
    parser.add_argument('--all', action='store_true', 
                       help='Run all demos')
    parser.add_argument('--processing', action='store_true',
                       help='Run image processing demo')
    parser.add_argument('--yolo', action='store_true',
                       help='Run YOLO detection demo')
    parser.add_argument('--batch', action='store_true',
                       help='Run batch processing demo')
    parser.add_argument('--realtime', action='store_true',
                       help='Run real-time detection demo')
    parser.add_argument('--comparison', action='store_true',
                       help='Run image comparison demo')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print("\n" + "="*60)
    print("Industrial Defect Detection System - Demonstration")
    print("="*60)
    
    # Run selected demos
    if args.all or args.processing:
        demo_image_processing()
    
    if args.all or args.yolo:
        demo_yolo_detection()
    
    if args.all or args.batch:
        demo_batch_processing()
    
    if args.all or args.realtime:
        demo_real_time()
    
    if args.all or args.comparison:
        demo_comparison()
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)


if __name__ == "__main__":
    main()
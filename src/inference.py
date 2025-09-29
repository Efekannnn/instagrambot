"""
Real-time Inference Module
Provides utilities for batch processing and real-time inference
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Union
import time
from tqdm import tqdm
import json


class InferenceEngine:
    """
    High-performance inference engine for defect detection.
    
    Features:
    - Batch processing
    - Performance metrics
    - Result logging
    - Multi-threaded processing
    """
    
    def __init__(self, detector):
        """
        Initialize inference engine.
        
        Args:
            detector: DefectDetector instance
        """
        self.detector = detector
        self.results_history = []
        
    def process_image_batch(self, image_paths: List[str],
                           save_results: bool = True) -> List[Dict]:
        """
        Process a batch of images.
        
        Args:
            image_paths: List of image file paths
            save_results: Whether to save annotated images
            
        Returns:
            List of detection results for each image
        """
        results = []
        
        print(f"Processing {len(image_paths)} images...")
        for img_path in tqdm(image_paths):
            try:
                # Load image
                image = cv2.imread(img_path)
                if image is None:
                    print(f"Warning: Could not load {img_path}")
                    continue
                
                # Detect defects
                start_time = time.time()
                detections = self.detector.detect_defects(image)
                inference_time = time.time() - start_time
                
                # Visualize
                annotated = self.detector.visualize_detections(image, detections)
                
                # Save if requested
                if save_results:
                    output_dir = Path(self.detector.config['visualization']['output_dir'])
                    output_dir.mkdir(exist_ok=True)
                    output_path = output_dir / f"result_{Path(img_path).name}"
                    cv2.imwrite(str(output_path), annotated)
                
                # Store results
                result = {
                    'image_path': img_path,
                    'num_defects': len(detections),
                    'detections': detections,
                    'inference_time': inference_time,
                    'timestamp': time.time()
                }
                results.append(result)
                self.results_history.append(result)
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                continue
        
        return results
    
    def process_directory(self, directory: str,
                         extensions: List[str] = None,
                         save_results: bool = True) -> List[Dict]:
        """
        Process all images in a directory.
        
        Args:
            directory: Directory path
            extensions: List of file extensions to process
            save_results: Whether to save results
            
        Returns:
            List of detection results
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        # Find all images
        image_paths = []
        dir_path = Path(directory)
        for ext in extensions:
            image_paths.extend(dir_path.glob(f"*{ext}"))
            image_paths.extend(dir_path.glob(f"*{ext.upper()}"))
        
        image_paths = [str(p) for p in image_paths]
        
        if not image_paths:
            print(f"No images found in {directory}")
            return []
        
        return self.process_image_batch(image_paths, save_results)
    
    def real_time_inference(self, source: Union[int, str] = 0,
                          display: bool = True) -> None:
        """
        Run real-time inference on video stream.
        
        Args:
            source: Video source (0 for webcam, or video file path)
            display: Whether to display output
        """
        cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video source: {source}")
        
        print("Starting real-time inference. Press 'q' to quit, 's' to save screenshot.")
        
        fps_history = []
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Measure FPS
                start_time = time.time()
                
                # Detect defects
                detections = self.detector.detect_defects(frame, preprocess=False)
                
                # Visualize
                annotated = self.detector.visualize_detections(frame, detections)
                
                # Calculate FPS
                end_time = time.time()
                fps = 1.0 / (end_time - start_time)
                fps_history.append(fps)
                
                # Display FPS
                fps_text = f"FPS: {fps:.1f}"
                cv2.putText(
                    annotated,
                    fps_text,
                    (annotated.shape[1] - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
                
                # Display
                if display:
                    cv2.imshow('Real-time Defect Detection', annotated)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        # Save screenshot
                        output_dir = Path(self.detector.config['visualization']['output_dir'])
                        output_dir.mkdir(exist_ok=True)
                        screenshot_path = output_dir / f"screenshot_{frame_count}.jpg"
                        cv2.imwrite(str(screenshot_path), annotated)
                        print(f"Screenshot saved: {screenshot_path}")
                
                frame_count += 1
                
        finally:
            cap.release()
            if display:
                cv2.destroyAllWindows()
            
            # Print statistics
            if fps_history:
                avg_fps = np.mean(fps_history)
                print(f"\nProcessed {frame_count} frames")
                print(f"Average FPS: {avg_fps:.2f}")
    
    def generate_report(self, results: List[Dict], 
                       output_path: str = "detection_report.json") -> None:
        """
        Generate a detailed report of detection results.
        
        Args:
            results: List of detection results
            output_path: Output file path for report
        """
        # Calculate statistics
        total_images = len(results)
        total_defects = sum(r['num_defects'] for r in results)
        avg_defects = total_defects / total_images if total_images > 0 else 0
        avg_inference_time = np.mean([r['inference_time'] for r in results]) if results else 0
        
        # Count defects by class
        defect_counts = {}
        for result in results:
            for det in result['detections']:
                cls_name = det['class_name']
                defect_counts[cls_name] = defect_counts.get(cls_name, 0) + 1
        
        # Create report
        report = {
            'summary': {
                'total_images': total_images,
                'total_defects': total_defects,
                'average_defects_per_image': avg_defects,
                'average_inference_time': avg_inference_time,
                'defect_distribution': defect_counts
            },
            'detailed_results': results
        }
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nReport Summary:")
        print(f"  Total Images: {total_images}")
        print(f"  Total Defects: {total_defects}")
        print(f"  Avg Defects/Image: {avg_defects:.2f}")
        print(f"  Avg Inference Time: {avg_inference_time*1000:.2f}ms")
        print(f"\nDefect Distribution:")
        for cls_name, count in defect_counts.items():
            print(f"  {cls_name}: {count}")
        print(f"\nFull report saved to: {output_path}")
    
    def benchmark(self, test_images: List[str], 
                 num_runs: int = 10) -> Dict:
        """
        Benchmark the detector performance.
        
        Args:
            test_images: List of test image paths
            num_runs: Number of runs for averaging
            
        Returns:
            Dictionary with benchmark results
        """
        print(f"Running benchmark with {len(test_images)} images, {num_runs} runs each...")
        
        inference_times = []
        
        for img_path in tqdm(test_images):
            image = cv2.imread(img_path)
            if image is None:
                continue
            
            # Run multiple times
            for _ in range(num_runs):
                start_time = time.time()
                _ = self.detector.detect_defects(image)
                inference_time = time.time() - start_time
                inference_times.append(inference_time)
        
        # Calculate statistics
        results = {
            'mean_time': np.mean(inference_times),
            'std_time': np.std(inference_times),
            'min_time': np.min(inference_times),
            'max_time': np.max(inference_times),
            'fps': 1.0 / np.mean(inference_times),
            'total_runs': len(inference_times)
        }
        
        print(f"\nBenchmark Results:")
        print(f"  Mean Inference Time: {results['mean_time']*1000:.2f}ms")
        print(f"  Std Dev: {results['std_time']*1000:.2f}ms")
        print(f"  Min/Max: {results['min_time']*1000:.2f}ms / {results['max_time']*1000:.2f}ms")
        print(f"  Average FPS: {results['fps']:.2f}")
        
        return results
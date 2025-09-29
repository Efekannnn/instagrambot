"""
YOLO-based Defect Detection Module
Implements real-time defect detection using YOLO architecture
"""

import torch
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from ultralytics import YOLO
import yaml


class DefectDetector:
    """
    Industrial defect detection system using YOLO.
    
    This class provides comprehensive defect detection capabilities including:
    - Real-time object detection
    - Image preprocessing
    - Post-processing and filtering
    - Visualization of results
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the defect detector.
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.device = self._setup_device()
        self.model = self._load_model()
        self.class_names = self.config['classes']
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup_device(self) -> str:
        """Setup computation device (GPU/CPU)."""
        if self.config['performance']['use_gpu'] and torch.cuda.is_available():
            device = 'cuda'
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = 'cpu'
            print("Using CPU")
        return device
    
    def _load_model(self) -> YOLO:
        """Load YOLO model with specified weights."""
        model_name = self.config['model']['architecture']
        weights = self.config['model']['weights']
        
        try:
            model = YOLO(weights)
            model.to(self.device)
            print(f"Loaded model: {model_name}")
            return model
        except Exception as e:
            print(f"Error loading custom weights, using pretrained: {e}")
            model = YOLO(f'{model_name}.pt')
            model.to(self.device)
            return model
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing to enhance defect detection.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Preprocessed image
        """
        processed = image.copy()
        
        # Denoise if enabled
        if self.config['preprocessing']['denoise']:
            processed = cv2.fastNlMeansDenoisingColored(processed, None, 10, 10, 7, 21)
        
        # Enhance contrast if enabled
        if self.config['preprocessing']['enhance_contrast']:
            lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            processed = cv2.merge([l, a, b])
            processed = cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)
        
        return processed
    
    def detect_defects(self, image: np.ndarray, 
                      preprocess: bool = True) -> List[Dict]:
        """
        Detect defects in the input image.
        
        Args:
            image: Input image in BGR format
            preprocess: Whether to apply preprocessing
            
        Returns:
            List of detection dictionaries containing bbox, class, confidence
        """
        # Preprocess if enabled
        if preprocess:
            image = self.preprocess_image(image)
        
        # Run inference
        results = self.model.predict(
            image,
            conf=self.config['model']['confidence_threshold'],
            iou=self.config['model']['iou_threshold'],
            imgsz=self.config['model']['image_size'],
            device=self.device,
            verbose=False
        )
        
        # Parse results
        detections = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            
            for i in range(len(boxes)):
                bbox = boxes.xyxy[i].cpu().numpy()
                conf = float(boxes.conf[i].cpu().numpy())
                cls = int(boxes.cls[i].cpu().numpy())
                
                # Calculate defect area
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                
                # Filter by area
                min_area = self.config['detection']['min_area']
                max_area = self.config['detection']['max_area']
                
                if min_area <= area <= max_area:
                    detection = {
                        'bbox': bbox.tolist(),
                        'confidence': conf,
                        'class_id': cls,
                        'class_name': self.class_names[cls] if cls < len(self.class_names) else f'class_{cls}',
                        'area': area
                    }
                    detections.append(detection)
        
        return detections
    
    def apply_edge_detection(self, image: np.ndarray) -> np.ndarray:
        """
        Apply edge detection for additional defect analysis.
        
        Args:
            image: Input image
            
        Returns:
            Edge-detected image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    def visualize_detections(self, image: np.ndarray, 
                            detections: List[Dict],
                            show_edges: bool = False) -> np.ndarray:
        """
        Visualize detections on the image.
        
        Args:
            image: Input image
            detections: List of detections
            show_edges: Whether to show edge detection overlay
            
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        # Color map for different defect types
        colors = [
            (0, 255, 0),    # Green
            (0, 165, 255),  # Orange
            (0, 0, 255),    # Red
            (255, 0, 255),  # Magenta
            (255, 255, 0),  # Cyan
            (128, 0, 128),  # Purple
        ]
        
        # Draw detections
        for det in detections:
            bbox = det['bbox']
            cls_id = det['class_id']
            conf = det['confidence']
            cls_name = det['class_name']
            
            # Get color for this class
            color = colors[cls_id % len(colors)]
            
            # Draw bounding box
            x1, y1, x2, y2 = map(int, bbox)
            thickness = self.config['visualization']['box_thickness']
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label
            if self.config['visualization']['show_labels']:
                label = f"{cls_name}"
                if self.config['visualization']['show_confidence']:
                    label += f" {conf:.2f}"
                
                font_scale = self.config['visualization']['font_scale']
                font_thickness = max(1, thickness - 1)
                
                # Calculate label size
                (label_w, label_h), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
                )
                
                # Draw label background
                cv2.rectangle(
                    annotated,
                    (x1, y1 - label_h - baseline - 5),
                    (x1 + label_w, y1),
                    color,
                    -1
                )
                
                # Draw label text
                cv2.putText(
                    annotated,
                    label,
                    (x1, y1 - baseline - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),
                    font_thickness
                )
        
        # Add edge detection overlay if requested
        if show_edges and self.config['detection']['edge_detection']:
            edges = self.apply_edge_detection(image)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            annotated = cv2.addWeighted(annotated, 0.8, edges_colored, 0.2, 0)
        
        # Add summary text
        summary = f"Defects Found: {len(detections)}"
        cv2.putText(
            annotated,
            summary,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2
        )
        
        return annotated
    
    def process_image(self, image_path: str, 
                     save_output: bool = True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process a single image for defect detection.
        
        Args:
            image_path: Path to input image
            save_output: Whether to save the output
            
        Returns:
            Tuple of (annotated image, detections list)
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Detect defects
        detections = self.detect_defects(image)
        
        # Visualize
        annotated = self.visualize_detections(
            image, 
            detections,
            show_edges=self.config['detection']['edge_detection']
        )
        
        # Save if requested
        if save_output and self.config['visualization']['save_results']:
            output_dir = Path(self.config['visualization']['output_dir'])
            output_dir.mkdir(exist_ok=True)
            
            output_path = output_dir / f"detected_{Path(image_path).name}"
            cv2.imwrite(str(output_path), annotated)
            print(f"Saved result to: {output_path}")
        
        return annotated, detections
    
    def process_video(self, video_path: str, 
                     save_output: bool = True,
                     display: bool = True) -> None:
        """
        Process video for real-time defect detection.
        
        Args:
            video_path: Path to input video or 0 for webcam
            save_output: Whether to save the output video
            display: Whether to display the video in real-time
        """
        # Open video
        if video_path == 'webcam' or video_path == '0':
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer if saving
        writer = None
        if save_output:
            output_dir = Path(self.config['visualization']['output_dir'])
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "output_video.mp4"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        print("Processing video... Press 'q' to quit")
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect defects
                detections = self.detect_defects(frame)
                
                # Visualize
                annotated = self.visualize_detections(frame, detections)
                
                # Add FPS counter
                frame_count += 1
                fps_text = f"Frame: {frame_count}"
                cv2.putText(
                    annotated,
                    fps_text,
                    (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )
                
                # Save frame
                if writer is not None:
                    writer.write(annotated)
                
                # Display
                if display:
                    cv2.imshow('Defect Detection', annotated)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        finally:
            cap.release()
            if writer is not None:
                writer.release()
            if display:
                cv2.destroyAllWindows()
            
            print(f"Processed {frame_count} frames")
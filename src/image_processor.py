"""
Advanced Image Processing Module
Implements various OpenCV-based image processing techniques for defect analysis
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class ProcessingResult:
    """Container for image processing results."""
    original: np.ndarray
    processed: np.ndarray
    mask: Optional[np.ndarray] = None
    contours: Optional[List] = None
    features: Optional[dict] = None


class ImageProcessor:
    """
    Advanced image processing for industrial defect detection.
    
    Provides various computer vision techniques including:
    - Adaptive thresholding
    - Morphological operations
    - Contour detection
    - Feature extraction
    - Image enhancement
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.kernels = {
            'small': cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),
            'medium': cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
            'large': cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        }
    
    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply comprehensive enhancement to improve defect visibility.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            Enhanced image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        return enhanced
    
    def adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """
        Apply adaptive thresholding for defect segmentation.
        
        Args:
            image: Input image
            
        Returns:
            Binary threshold image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to preserve edges
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            filtered,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )
        
        return thresh
    
    def morphological_operations(self, binary_image: np.ndarray,
                                 kernel_size: str = 'medium') -> np.ndarray:
        """
        Apply morphological operations to clean up binary image.
        
        Args:
            binary_image: Binary input image
            kernel_size: Size of structuring element ('small', 'medium', 'large')
            
        Returns:
            Processed binary image
        """
        kernel = self.kernels.get(kernel_size, self.kernels['medium'])
        
        # Remove noise with opening
        opened = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
        
        # Fill gaps with closing
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        
        return closed
    
    def detect_contours(self, binary_image: np.ndarray) -> List[np.ndarray]:
        """
        Detect contours in binary image.
        
        Args:
            binary_image: Binary input image
            
        Returns:
            List of contours
        """
        contours, _ = cv2.findContours(
            binary_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter small contours (noise)
        min_area = 50
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        return filtered_contours
    
    def extract_features(self, contour: np.ndarray) -> dict:
        """
        Extract features from a contour.
        
        Args:
            contour: Input contour
            
        Returns:
            Dictionary of features
        """
        # Basic features
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Bounding box
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h if h > 0 else 0
        
        # Convex hull
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area if hull_area > 0 else 0
        
        # Moments
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else 0
        cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else 0
        
        # Extent
        extent = float(area) / (w * h) if (w * h) > 0 else 0
        
        # Approximate polygon
        epsilon = 0.01 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)
        
        return {
            'area': area,
            'perimeter': perimeter,
            'aspect_ratio': aspect_ratio,
            'solidity': solidity,
            'extent': extent,
            'centroid': (cx, cy),
            'bbox': (x, y, w, h),
            'vertices': vertices
        }
    
    def detect_edges_multi_scale(self, image: np.ndarray) -> np.ndarray:
        """
        Multi-scale edge detection for robust defect boundary detection.
        
        Args:
            image: Input image
            
        Returns:
            Combined edge image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Multiple scales
        edges = []
        for sigma in [0.5, 1.0, 2.0]:
            blurred = cv2.GaussianBlur(gray, (0, 0), sigma)
            edge = cv2.Canny(blurred, 50, 150)
            edges.append(edge)
        
        # Combine edges
        combined = cv2.bitwise_or(edges[0], edges[1])
        combined = cv2.bitwise_or(combined, edges[2])
        
        return combined
    
    def segment_defects(self, image: np.ndarray) -> ProcessingResult:
        """
        Complete defect segmentation pipeline.
        
        Args:
            image: Input image
            
        Returns:
            ProcessingResult object with all processing outputs
        """
        # Enhance image
        enhanced = self.enhance_image(image)
        
        # Create binary mask
        binary = self.adaptive_threshold(enhanced)
        
        # Clean up with morphological operations
        cleaned = self.morphological_operations(binary)
        
        # Detect contours
        contours = self.detect_contours(cleaned)
        
        # Extract features from each contour
        features = []
        for cnt in contours:
            feat = self.extract_features(cnt)
            features.append(feat)
        
        return ProcessingResult(
            original=image,
            processed=enhanced,
            mask=cleaned,
            contours=contours,
            features=features
        )
    
    def visualize_segmentation(self, result: ProcessingResult) -> np.ndarray:
        """
        Visualize segmentation results.
        
        Args:
            result: ProcessingResult object
            
        Returns:
            Visualization image
        """
        vis = result.original.copy()
        
        # Draw contours
        if result.contours:
            cv2.drawContours(vis, result.contours, -1, (0, 255, 0), 2)
            
            # Draw features
            if result.features:
                for feat in result.features:
                    # Draw centroid
                    cx, cy = feat['centroid']
                    cv2.circle(vis, (cx, cy), 5, (0, 0, 255), -1)
                    
                    # Draw bounding box
                    x, y, w, h = feat['bbox']
                    cv2.rectangle(vis, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    
                    # Add area text
                    area_text = f"A:{int(feat['area'])}"
                    cv2.putText(vis, area_text, (x, y - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        return vis
    
    def compare_images(self, image1: np.ndarray, 
                      image2: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Compare two images to detect differences (useful for defect detection).
        
        Args:
            image1: First image (reference/template)
            image2: Second image (test image)
            
        Returns:
            Tuple of (difference image, similarity score)
        """
        # Convert to grayscale
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
        # Ensure same size
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
        
        # Compute absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Threshold difference
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate similarity score
        similarity = 1.0 - (np.count_nonzero(thresh) / thresh.size)
        
        # Create colored difference visualization
        diff_colored = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
        
        return diff_colored, similarity
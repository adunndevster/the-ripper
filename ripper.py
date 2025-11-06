#!/usr/bin/env python3
"""
The Ripper - Video Background Removal Tool
Extracts frames from video and removes background color, outputting transparent PNGs.
"""

import cv2
import numpy as np
from PIL import Image
import os
import argparse
from pathlib import Path


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_color_range(color_str, tolerance):
    """
    Parse color string and return lower/upper bounds for color keying.
    
    Args:
        color_str: Hex color (e.g., '#00FF00') or RGB tuple string (e.g., '0,255,0')
        tolerance: Tolerance value for color matching (0-255)
    
    Returns:
        Tuple of (lower_bound, upper_bound) as numpy arrays in BGR format
    """
    if color_str.startswith('#'):
        r, g, b = hex_to_rgb(color_str)
    else:
        r, g, b = map(int, color_str.split(','))
    
    # OpenCV uses BGR format
    color_bgr = np.array([b, g, r], dtype=np.uint8)
    
    lower_bound = np.clip(color_bgr - tolerance, 0, 255).astype(np.uint8)
    upper_bound = np.clip(color_bgr + tolerance, 0, 255).astype(np.uint8)
    
    return lower_bound, upper_bound


def create_alpha_mask(frame, lower_bound, upper_bound, feather=2):
    """
    Create an alpha mask for the frame based on color range.
    
    Args:
        frame: BGR image frame
        lower_bound: Lower color bound (BGR)
        upper_bound: Upper color bound (BGR)
        feather: Edge smoothing amount (pixels)
    
    Returns:
        Alpha mask (0-255)
    """
    # Create initial mask
    mask = cv2.inRange(frame, lower_bound, upper_bound)
    
    # Invert mask (we want to keep non-background pixels)
    mask = cv2.bitwise_not(mask)
    
    # Optional: Apply morphological operations to clean up mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Feather edges for smoother transparency
    if feather > 0:
        mask = cv2.GaussianBlur(mask, (feather * 2 + 1, feather * 2 + 1), 0)
    
    return mask


def process_video(video_path, output_dir, color, tolerance=30, fps=12, feather=2):
    """
    Process video and extract frames with transparent background.
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save PNG frames
        color: Background color to remove (hex or RGB string)
        tolerance: Color matching tolerance (0-255)
        fps: Frames per second to extract
        feather: Edge smoothing amount
    """
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / original_fps
    
    print(f"Video Info:")
    print(f"  Original FPS: {original_fps:.2f}")
    print(f"  Total Frames: {total_frames}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Target FPS: {fps}")
    
    # Calculate frame interval
    frame_interval = original_fps / fps
    expected_frames = int(duration * fps)
    
    print(f"  Expected output frames: {expected_frames}")
    print()
    
    # Parse color range
    lower_bound, upper_bound = parse_color_range(color, tolerance)
    print(f"Color range (BGR): {lower_bound} to {upper_bound}")
    print()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process frames
    frame_count = 0
    saved_count = 0
    next_frame_to_save = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Check if this frame should be saved
        if frame_count >= next_frame_to_save:
            # Create alpha mask
            alpha_mask = create_alpha_mask(frame, lower_bound, upper_bound, feather)
            
            # Convert BGR to RGBA
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgba = np.dstack([frame_rgb, alpha_mask])
            
            # Save as PNG with PIL (preserves alpha channel)
            img = Image.fromarray(frame_rgba)
            output_file = output_path / f"frame_{saved_count:04d}.png"
            img.save(output_file, 'PNG')
            
            saved_count += 1
            next_frame_to_save += frame_interval
            
            if saved_count % 10 == 0:
                print(f"Processed {saved_count} frames...")
        
        frame_count += 1
    
    cap.release()
    
    print()
    print(f"Complete! Saved {saved_count} frames to {output_dir}")
    print(f"Average FPS: {saved_count / duration:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract frames from video with background color removal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove green background with default tolerance
  python ripper.py input.mp4 output/ --color "#00FF00"
  
  # Remove blue background with custom tolerance and FPS
  python ripper.py input.mp4 output/ --color "0,0,255" --tolerance 40 --fps 24
  
  # Remove green screen with more edge smoothing
  python ripper.py greenscreen.mp4 frames/ --color "#00FF00" --tolerance 35 --feather 3
        """
    )
    
    parser.add_argument('video', help='Input video file path')
    parser.add_argument('output', help='Output directory for PNG frames')
    parser.add_argument('--color', '-c', required=True,
                        help='Background color to remove (hex like "#00FF00" or RGB like "0,255,0")')
    parser.add_argument('--tolerance', '-t', type=int, default=30,
                        help='Color matching tolerance (0-255, default: 30)')
    parser.add_argument('--fps', '-f', type=int, default=12,
                        help='Output frames per second (default: 12)')
    parser.add_argument('--feather', type=int, default=2,
                        help='Edge feathering amount in pixels (default: 2)')
    
    args = parser.parse_args()
    
    # Validate inputs
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"Error: Video file not found: {args.video}")
        return 1
    
    if args.tolerance < 0 or args.tolerance > 255:
        print("Error: Tolerance must be between 0 and 255")
        return 1
    
    if args.fps <= 0:
        print("Error: FPS must be positive")
        return 1
    
    # Process video
    try:
        process_video(
            video_path,
            args.output,
            args.color,
            args.tolerance,
            args.fps,
            args.feather
        )
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())


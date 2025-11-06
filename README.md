# The Ripper 🎬

A Python tool for extracting frames from video with background color removal (chroma keying). Perfect for creating sprite sheets, animated sequences, or removing green/blue screens.

## Features

- 🎨 Remove background by color range (chroma keying)
- 🖼️ Export frames as transparent PNGs
- ⚙️ Configurable frame rate (default: 12 fps)
- 🎯 Adjustable color tolerance for better keying
- ✨ Edge feathering for smoother transparency
- 📊 Progress tracking and video info display

## Installation

1. **Install Python 3.8 or higher**
   - macOS: Python 3 is usually pre-installed, or install via Homebrew: `brew install python3`

2. **Install dependencies:**

```bash
pip3 install -r requirements.txt
```

### Troubleshooting Installation

If you encounter SSL certificate errors on macOS:
```bash
# Try installing Python certificates
/Applications/Python\ 3.*/Install\ Certificates.command

# Or install packages individually
pip3 install opencv-python numpy Pillow
```

If you get permission errors:
```bash
pip3 install --user -r requirements.txt
```

To verify dependencies are installed:
```bash
python3 -c "import cv2, numpy, PIL; print('All dependencies installed!')"
```

## Usage

Basic usage:
```bash
python3 ripper.py input.mp4 output_folder/ --color "#00FF00"
```

### Command Line Arguments

- `video` - Path to input video file (required)
- `output` - Directory to save PNG frames (required)
- `--color, -c` - Background color to remove (required)
  - Hex format: `"#00FF00"` (green)
  - RGB format: `"0,255,0"` (green)
- `--tolerance, -t` - Color matching tolerance (0-255, default: 30)
  - Higher values = more aggressive keying
  - Lower values = more precise color matching
- `--fps, -f` - Output frames per second (default: 12)
- `--feather` - Edge smoothing in pixels (default: 2)
  - Higher values = softer edges
  - 0 = no smoothing

### Examples

Remove green screen from video at 12 fps:
```bash
python3 ripper.py greenscreen.mp4 frames/ --color "#00FF00"
```

Remove blue background with higher tolerance:
```bash
python3 ripper.py video.mpeg output/ --color "#0000FF" --tolerance 40
```

Extract at 24 fps with more edge smoothing:
```bash
python3 ripper.py input.mp4 sprites/ --color "0,255,0" --fps 24 --feather 3
```

## How It Works

1. **Frame Extraction**: Reads video and extracts frames at specified FPS
2. **Color Keying**: Identifies pixels within the color tolerance range
3. **Mask Creation**: Creates alpha mask with morphological operations to clean edges
4. **Edge Feathering**: Applies gaussian blur for smooth transparency transitions
5. **PNG Export**: Saves frames as RGBA PNGs with transparency

## Tips for Best Results

- **Green Screen**: Use `--color "#00FF00"` with tolerance 30-40
- **Blue Screen**: Use `--color "#0000FF"` with tolerance 30-40
- **Uniform Backgrounds**: Lower tolerance (15-25) for solid color backgrounds
- **Varied Lighting**: Higher tolerance (35-50) when lighting isn't uniform
- **Soft Edges**: Increase `--feather` value (3-5) for characters/objects with fine details
- **Hard Edges**: Use `--feather 0` or `--feather 1` for sharp cutouts

## Output Format

Frames are saved as:
- `frame_0000.png`
- `frame_0001.png`
- `frame_0002.png`
- ...

Each frame is a PNG with full RGBA (transparency) support.

## Requirements

- Python 3.8+
- OpenCV (opencv-python)
- NumPy
- Pillow

## License

MIT License - Feel free to use and modify as needed!


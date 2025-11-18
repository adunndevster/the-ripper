# Usage Examples

## Quick Start

After installing dependencies with `pip3 install -r requirements.txt`, you can use The Ripper like this:

## Common Use Cases

### 1. Green Screen Removal (Most Common)
```bash
python3 ripper.py my_video.mp4 output/ --color "#00FF00"
```
This will:
- Extract frames at 12 fps
- Remove green background (#00FF00)
- Save transparent PNGs to `output/` folder

### 2. Blue Screen Removal
```bash
python3 ripper.py my_video.mpeg output/ --color "#0000FF" --tolerance 35
```

### 3. Custom Color Background
If your background is a specific color, you can specify it in hex or RGB:
```bash
# Hex color
python3 ripper.py video.mp4 output/ --color "#FF69B4"

# RGB color (pink)
python3 ripper.py video.mp4 output/ --color "255,105,180"
```

### 4. High Frame Rate Export
For smoother animations, increase the FPS:
```bash
python3 ripper.py video.mp4 sprites/ --color "#00FF00" --fps 24
```

### 5. Lower Frame Rate (Smaller File Count)
For simpler animations or storage savings:
```bash
python3 ripper.py video.mp4 sprites/ --color "#00FF00" --fps 6
```

### 6. Fine-Tuning the Keying

#### Tighter color matching (less aggressive):
```bash
python3 ripper.py video.mp4 output/ --color "#00FF00" --tolerance 20
```
Use this when your background is very uniform and you want to preserve colors close to green.

#### More aggressive keying:
```bash
python3 ripper.py video.mp4 output/ --color "#00FF00" --tolerance 50
```
Use this when your green screen has varied lighting or shadows.

### 7. Edge Quality Control

#### Soft, feathered edges (good for characters/organic shapes):
```bash
python3 ripper.py video.mp4 output/ --color "#00FF00" --feather 4
```

#### Sharp, hard edges (good for graphics/logos):
```bash
python3 ripper.py video.mp4 output/ --color "#00FF00" --feather 0
```

## Complete Example

The ultimate command with all options tuned:
```bash
python3 ripper.py greenscreen_footage.mp4 character_sprites/ \
  --color "#00FF00" \
  --tolerance 35 \
  --fps 12 \
  --feather 2
```

## Output

For an 8-second video at 12 fps, you'll get:
```
character_sprites/
├── frame_0000.png
├── frame_0001.png
├── frame_0002.png
├── ...
└── frame_0095.png
```

Each PNG has full transparency (RGBA format) and can be used in:
- Game engines (Unity, Unreal, Godot)
- Animation software
- Video editing tools
- Web applications
- Sprite sheets

## Testing Your Color Range

Not sure what tolerance to use? Try this approach:

1. Start with default tolerance (30):
```bash
python3 ripper.py test.mp4 test_output/ --color "#00FF00"
```

2. Check a few frames - if too much background remains, increase tolerance:
```bash
python3 ripper.py test.mp4 test_output/ --color "#00FF00" --tolerance 40
```

3. If it's removing parts of your subject, decrease tolerance:
```bash
python3 ripper.py test.mp4 test_output/ --color "#00FF00" --tolerance 25
```

## Performance Tips

- Processing time depends on video resolution and length
- Higher FPS = more frames to process = longer time
- A 1080p 8-second video at 12 fps typically processes in 10-30 seconds
- The tool shows progress every 10 frames

## Next Steps

After generating your transparent PNGs, you can:
1. Import them into game engines as sprite sequences
2. Combine them into sprite sheets using tools like TexturePacker
3. Create GIF animations with transparency
4. Use them in video compositing software



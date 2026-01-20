# Utility Scripts Usage Guide
This folder contains utilities for converting fonts and images to MicroPython-compatible Python files.

## Font Conversion (`fonts/font_to_py.py`)
Converts TTF/OTF/BDF/PCF font files to Python modules for use with MicroPython displays.

**Author:** Peter Hinch
**Source:** [micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py)
**License:** MIT

### Requirements
```bash
pip install freetype-py
```

### Basic Syntax
```bash
./font_to_py.py <font_file> <height> <output.py> [options]
```

### Example
```bash
cd utility/fonts
./font_to_py.py Jersey25-Regular.ttf 28 jersey28_de.py -k charset_de.txt
```

This converts the Jersey25 font at 28 pixels height, using a custom German character set.
### Common Options

| Option | Description |
|--------|-------------|
| `-k <file>` | Load character set from file (e.g., `charset_de.txt`) |
| `-c <chars>` | Specify characters directly (e.g., `-c "0123456789:"` for a clock) |
| `-f` | Fixed width (monospaced) font |
| `-x` | Horizontal (x) mapping (default) |
| `-y` | Vertical (y) mapping |
| `-r` | Bit reversal |
| `-s <ord>` | Smallest character ordinal (default: 32, space) |
| `-l <ord>` | Largest character ordinal (default: 126, ~) |
| `-e <ord>` | Error character ordinal (default: 63, ?) |
| `-b` | Produce binary (random access) font file |
| `-i` | Include generator function to iterate over character set |

### Character Set File Format
The `charset_de.txt` contains all characters, standard ASCII + umlauts, to include in the font:

```
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
äöüßÄÖÜ
```

---

## Image/Icon Conversion (`icons/img_to_py.py`)
Converts PNG/image files to Python modules for e-paper or monochrome displays.

**Author:** phoreglad
**Source:** [epaper-img-converter](https://github.com/phoreglad/epaper-img-converter)

### Requirements
```bash
pip install Pillow
```

### Basic Syntax
```bash
python img_to_py.py <source_image> [output.py] [options]
```

### Examples
```bash
cd utility/icons

# Basic conversion (output defaults to source filename with .py extension)
python img_to_py.py run_24.png

# With explicit output file
python img_to_py.py run_24.png run_icon.py

# Scale to specific dimensions
python img_to_py.py walk.svg run_24.py --width 24 --height 24

# Preview before saving
python img_to_py.py run_24.png -p

# Preview only (no file output)
python img_to_py.py run_24.png --preview-only

# With dithering for better gradients
python img_to_py.py walk_24.png -d
```

### Options

| Option | Description |
|--------|-------------|
| `-m {L1,L2}` | Output mode: L1 = binary/BW (default), L2 = 4-level grayscale |
| `-p, --preview` | Show image preview after conversion |
| `--preview-only` | Show preview and exit without saving |
| `-d, --dither` | Enable dithering (better for gradients) |
| `--width <px>` | Scale to target width (maintains aspect ratio if height not set) |
| `--height <px>` | Scale to target height (maintains aspect ratio if width not set) |
| `-t <values>` | Threshold values (1 for L1, 3 for L2 mode) |

### Output Format
The generated Python file contains:

```python
width = 24
height = 24
img_bw = bytearray(...)  # Black/white data in HLSB format
img_red = bytearray(...) # Only present in L2 mode
```

### Notes
- Image width is automatically padded to be divisible by 8 (required for HLSB format)
- Alpha channels are converted to white background
- Output is compatible with MicroPython's `framebuf.FrameBuffer` in HLSB mode
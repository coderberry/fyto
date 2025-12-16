# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fyto is a Raspberry Pi Zero 2W-based plant monitoring system that displays animated emotions on a 2-inch IPS LCD screen based on real-time sensor readings. The project uses a socket-based client-server architecture where sensor readings drive emotion display changes.

## System Architecture

### Two-Process Communication Model

The system consists of two Python processes that communicate via TCP sockets on port 1013:

1. **Display Server** (`Code/main.py`):
   - Listens on `0.0.0.0:1013`
   - Controls the 2-inch LCD display via SPI
   - Receives 5-byte emotion codes from the sensor client
   - Plays 180-frame animations by loading PNG files sequentially
   - Uses interrupt flag `doInterrupt` to stop current animation when new emotion arrives
   - All images are rotated 180° before display

2. **Sensor Client** (`Code/sensors.py`):
   - Connects to the display server on `0.0.0.0:1013`
   - Reads from ADS1115 16-bit ADC via I2C
   - Sends 5-byte emotion strings: `'happy'`, `'sleep'`, `'thirs'`, `'savor'`, `'hotty'`, `'freez'`
   - Uses state flags to prevent redundant emotion transmissions
   - Continuously loops reading sensors (no delay between readings)

### Emotion Trigger Logic

The sensor client evaluates conditions in this priority order (first match wins):
1. **Light level** → `'sleep'` (<20%) or `'happy'` (>20%)
2. **Moisture level** → `'thirs'` (<10%), `'savor'` (10-90% rising), or `'savor'` (>90%)
3. **Temperature** → `'hotty'` (>30°C) or `'freez'` (<22°C)

### Hardware Communication

- **LCD Display**: SPI interface via `spidev` (90MHz frequency)
  - Uses GPIO pins: RST=27, DC=25, BL=18
  - Driven by `lib/LCD_2inch.py` (240x320 resolution)

- **ADS1115 ADC**: I2C interface at address 0x48
  - A0: Unused/Open
  - A1: LM35 temperature sensor (analog)
  - A2: Capacitive moisture sensor
  - A3: LDR light sensor

### Emotion Animation System

- Animations stored in `Code/emotion/[emotion_name]/frame[0-179].png`
- Folder names: `happy`, `sleepy`, `hot`, `freeze`, `savory`, `thirsty`
- Note: Code sends shortened names (`'sleep'`, `'thirs'`, etc.) but expects full folder names
- Each animation loops through 180 PNG frames loaded sequentially
- Current animation can be interrupted by setting `doInterrupt=1` flag

## Development Commands

### Running the System

**Terminal 1 (Display Server):**
```bash
cd Code
python3 main.py
```

**Terminal 2 (Sensor Client):**
```bash
cd Code
python3 sensors.py
```

Note: The display server must start first to establish the socket listener.

### Sensor Calibration

Edit `Code/calibration.py` to change which ADC channel to read:
```python
chan = AnalogIn(ads, ADS.P2)  # Moisture sensor
chan = AnalogIn(ads, ADS.P3)  # Light sensor
chan = AnalogIn(ads, ADS.P1)  # Temperature sensor
```

Run calibration:
```bash
cd Code
python3 calibration.py
```

Record the min/max raw ADC values, then update the `_map()` function calls in `sensors.py`:
```python
LDR_Percent = _map(LDR_Value, 22500, 50, 0, 100)      # Dark to bright
Moisture_Percent = _map(Moisture_Value, 31000, 15500, 0, 100)  # Dry to wet
```

### Documentation Website

Generate schemdraw-based wiring diagrams:
```bash
uv run docs/generate_schematic.py
```

Preview the GitHub Pages website locally:
```bash
cd docs
python3 -m http.server 8000
# Open http://localhost:8000
```

The website includes:
- Interactive wiring diagrams with tabbed views
- Hover-animated emotion previews (loads every 6th frame via Canvas API)
- Hardware requirements and setup guide
- Bash-highlighted quick start commands

## Critical Hardware Details

### ADS1115 Channel Assignments

The code expects this specific wiring (matches `sensors.py` lines 10-12):
- **A0**: Open/Unused
- **A1**: LM35 Temperature Sensor
- **A2**: Capacitive Moisture Sensor
- **A3**: LDR Light Sensor

⚠️ **Warning**: The original Instructables tutorial shows different channel assignments. If wiring differs from above, you must modify `sensors.py` channel definitions.

### Temperature Sensor Requirement

- **Must use LM35** analog sensor (outputs analog voltage)
- **Do NOT use DS18B20** digital sensor (requires completely different code)

### I2C Configuration

Before running, ensure I2C is enabled and Serial is disabled:
```bash
sudo raspi-config
# Interface Options → I2C → Enable
# Interface Options → Serial → Disable
```

Verify ADS1115 is detected at address 0x48:
```bash
sudo i2cdetect -y 1
```

### Voltage Protection

Strongly recommended: Use a 5V-to-3.3V bidirectional logic level converter for all sensor connections. The Raspberry Pi GPIO pins are 3.3V only and can be permanently damaged by 5V signals.

## Code Modification Patterns

### Adding New Emotions

1. Create new folder in `Code/emotion/[new_emotion]/` with 180 frames (frame0.png - frame179.png)
2. Add emotion logic to `sensors.py` (send 5-byte string)
3. Update `main.py` if folder name differs from sent string
4. For documentation website: Copy every 6th frame to `docs/emotions/[new_emotion]/`

### Adjusting Sensor Thresholds

Edit the condition checks in `sensors.py`:
- Light thresholds: Lines 50, 57 (currently 20%)
- Moisture thresholds: Lines 65, 74, 83 (currently 10%, 90%)
- Temperature thresholds: Lines 93, 99 (currently 30°C, 22°C)

### Changing Display Rotation

Modify line 46 in `main.py`:
```python
image = image.rotate(180)  # Change angle or remove
```

## Project Structure

```
Code/
├── main.py              # Display server (SPI LCD control)
├── sensors.py           # Sensor client (I2C ADC reading)
├── calibration.py       # Sensor calibration utility
├── emotion/             # 180-frame PNG animations per emotion
│   ├── happy/
│   ├── sleepy/
│   ├── hot/
│   ├── freeze/
│   ├── savory/
│   └── thirsty/
└── lib/                 # LCD driver libraries
    ├── LCD_2inch.py     # Main 2" display driver
    ├── lcdconfig.py     # GPIO/SPI hardware interface
    └── LCD_*.py         # Other display drivers (unused)

docs/                    # GitHub Pages website
├── index.html           # Main landing page with Canvas animations
├── wiring-diagram.html  # Full-screen interactive wiring guide
├── generate_schematic.py # PEP 723 script for schemdraw diagrams
├── diagrams/            # SVG schematics and wiring diagrams
└── emotions/            # Subset of animation frames (every 6th frame)

3D/                      # STL files for 3D-printed enclosure
```

## Dependency Management

### Raspberry Pi Dependencies
```bash
sudo apt-get install python3-pip python3-pil python3-numpy
pip3 install adafruit-circuitpython-ads1x15 spidev
```

### Documentation Dependencies
The `generate_schematic.py` script uses PEP 723 inline script metadata for `uv run`:
```python
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "schemdraw>=0.18",
# ]
# ///
```

No virtual environment or manual package installation needed—just run `uv run docs/generate_schematic.py`.

## Common Issues

### Emotion Folder Name Mismatch
The code sends abbreviated emotion names but looks for full folder names:
- Sent: `'thirs'`, `'savor'`, `'sleep'`, `'hotty'`, `'freez'`
- Expected folders: `thirsty`, `savory`, `sleepy`, `hot`, `freeze`

The display server handles this mapping, but folder names must match exactly.

### Socket Connection Refused
- Ensure `main.py` (display server) is running before `sensors.py` (client)
- Check no other process is using port 1013: `lsof -i :1013`

### Erratic Sensor Readings
- Use ADS1115 modules with pre-soldered headers (breadboard connections create noise)
- Verify I2C is enabled and Serial is disabled in `raspi-config`
- Add logic level converter for cleaner 5V-to-3.3V signal conversion

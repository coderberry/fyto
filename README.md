# Fyto - Turn Your Plant Into a Pet

Fyto is an intelligent planter that transforms your houseplant into an interactive companion. It monitors your plant's environment through sensors and displays animated emotions on a color LCD screen, helping you understand your plant's needs at a glance.

**📱 [View the Project Website](https://yourname.github.io/fyto/)** - Interactive wiring diagrams, full documentation, and build guide.

## Features

Fyto expresses **six distinct emotions** based on sensor readings:

| Emotion | Trigger | Folder |
|---------|---------|--------|
| **Thirsty** | Soil moisture < 10% | `thirsty` |
| **Savory** | Recently watered (moisture rising) | `savory` |
| **Happy** | Optimal conditions | `happy` |
| **Sleepy** | Low light (< 20%) | `sleepy` |
| **Hot** | Temperature > 30°C | `hot` |
| **Freeze** | Temperature < 22°C | `freeze` |

## Hardware Requirements

### Core Components
- **Raspberry Pi Zero 2W** - Main controller (1GHz quad-core ARM Cortex-A53)
- **240x320 2-inch IPS LCD Display** - For displaying emotions
- **ADS1115 16-bit ADC** - Analog-to-digital converter (Pi lacks native analog inputs)

### Sensors
- **Capacitive Soil Moisture Sensor** - Prevents corrosion unlike resistive sensors
- **LM35 Temperature Sensor** - Analog temperature sensor (**Important:** Do NOT use DS18B20 - see Troubleshooting)
- **LDR Light Sensor Module** - Detects ambient light levels

### Power & Accessories
- 5V 2A Power Adapter
- Micro USB Breadboard Power Supply Module
- 30AWG Silicone Wires (5m recommended)
- Perforated Board (for soldering)
- 2mm Transparent Acrylic Sheet (display cover)

### Recommended Addition
- **I2C 4-Channel Bi-Directional 5V to 3.3V Logic Level Converter** - Protects GPIO pins from voltage differences. Highly recommended to avoid damaging your Pi.

## Wiring Diagram

**Visual diagrams are available in the [docs](docs/) folder:**
- [Interactive Wiring Diagram (HTML)](docs/wiring-diagram.html) - Open in browser for full interactive view
- [SVG Wiring Diagram](docs/diagrams/fyto-wiring.svg) - Printable vector diagram
- [Schemdraw Schematic](docs/diagrams/fyto_schematic.svg) - Generated circuit schematic
- [Pinout Reference](docs/diagrams/fyto_pinout.svg) - GPIO pin reference diagram

To regenerate the schemdraw diagrams:
```bash
uv run docs/generate_schematic.py
```

### LCD to Raspberry Pi Zero 2W

| LCD Pin | Pi Zero Pin | GPIO |
|---------|-------------|------|
| VCC | Pin 1 | 3.3V |
| GND | Pin 9 | Ground |
| DIN | Pin 21 | GPIO 9 (MOSI) |
| CLK | Pin 23 | GPIO 11 (SCLK) |
| CS | Pin 24 | GPIO 8 (CE0) |
| DC | Pin 37 | GPIO 26 |
| RST | Pin 36 | GPIO 16 |
| BL | Pin 19 | GPIO 10 |

### ADS1115 ADC Connections

| ADS1115 Pin | Connection |
|-------------|------------|
| VCC | 3.3V |
| GND | Ground |
| SCL | Pi SCL (Pin 5 / GPIO 3) |
| SDA | Pi SDA (Pin 3 / GPIO 2) |
| A0 | (Open) |
| A1 | LM35 Temperature Sensor |
| A2 | Capacitive Moisture Sensor |
| A3 | LDR Light Sensor |

> **Important:** The original Instructables wiring diagram shows different channel assignments. The wiring above matches what the code expects. If you wire according to the original diagram, you'll need to modify `sensors.py`.

## Raspberry Pi Setup

### 1. Enable I2C

```bash
sudo raspi-config
```

Navigate to: **Interface Options** → **I2C** → **Enable**

> **Important:** Make sure I2C is enabled and Serial connection is **disabled**.

### 2. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy

pip3 install adafruit-circuitpython-ads1x15
pip3 install spidev
```

### 3. Clone the Repository

```bash
git clone https://github.com/CodersCafeTech/Fyto.git
cd Fyto/Code
```

## Calibration

Before running the main program, calibrate your sensors to get accurate readings.

### 1. Test Individual Sensors

Edit `calibration.py` to test each sensor channel:

```python
# For Moisture sensor (A2):
chan = AnalogIn(ads, ADS.P2)

# For Light sensor (A3):
chan = AnalogIn(ads, ADS.P3)

# For Temperature sensor (A1):
chan = AnalogIn(ads, ADS.P1)
```

Run the calibration script:
```bash
python3 calibration.py
```

### 2. Record Min/Max Values

For each sensor, record the raw ADC values at:
- **Moisture:** Dry soil (max) and wet soil (min)
- **Light:** Dark room (max ~22500) and bright light (min ~50)

### 3. Update sensors.py

Update the `_map()` function calls with your calibrated values:

```python
# Current defaults - adjust based on your calibration
LDR_Percent = _map(LDR_Value, 22500, 50, 0, 100)
Moisture_Percent = _map(Moisture_Value, 31000, 15500, 0, 100)
```

## Running Fyto

Fyto uses two Python scripts that communicate via sockets:

### Terminal 1 - Start the Display Server
```bash
cd Code
python3 main.py
```

### Terminal 2 - Start the Sensor Reader
```bash
cd Code
python3 sensors.py
```

### Auto-Start on Boot (Optional)

Create a systemd service or add to `/etc/rc.local`:

```bash
cd /path/to/Fyto/Code && python3 main.py &
sleep 5
cd /path/to/Fyto/Code && python3 sensors.py &
```

## 3D Printing

The enclosure consists of three parts:
- Outer cover
- Base
- Plant container (water-tight)

### Files
- Original STEP file: `3D/Flower_Latest v16.step`
- Pre-sliced STL files: [Google Drive](https://drive.google.com/drive/folders/1KikgjQQ0zHyn-Ojjpr6-c6RQJZTwspdg?usp=sharing) (community contribution)

### Print Settings
- Material: PLA
- Infill: 10%
- The vase design is water-tight even at faster print speeds

## Project Structure

```
Fyto/
├── Code/
│   ├── main.py           # Display server - shows emotions on LCD
│   ├── sensors.py        # Reads sensors and sends emotion triggers
│   ├── calibration.py    # Sensor calibration utility
│   ├── emotion/          # Animation frames for each emotion
│   │   ├── happy/        # 180 frames (frame0.png - frame179.png)
│   │   ├── thirsty/
│   │   ├── savory/
│   │   ├── sleepy/
│   │   ├── hot/
│   │   └── freeze/
│   └── lib/              # LCD driver libraries
│       ├── LCD_2inch.py  # 2-inch display driver
│       ├── lcdconfig.py  # GPIO/SPI configuration
│       └── ...
└── 3D/
    └── Flower_Latest v16.step
```

## Troubleshooting

### Common Issues

#### "Folder not found" errors
The emotion folder names in the code use shortened names. Ensure these match:
- Code sends: `thirs`, `savor`, `happy`, `sleep`, `hotty`, `freez`
- Folder names: `thirsty`, `savory`, `happy`, `sleepy`, `hot`, `freeze`

The current code has been updated to handle this, but if you see errors, check that the folder names match exactly.

#### Temperature sensor not working
**Use the LM35 analog sensor, NOT the DS18B20.** The DS18B20 is digital and won't work with this code without modifications. The LM35 outputs an analog voltage proportional to temperature.

#### Erratic sensor readings during calibration
- Use an ADS1115 module with **pre-soldered headers** if possible
- Breadboard connections can create noise
- Consider using a logic level converter for cleaner signals

#### GPIO pins not responding / damaged
Always use a **5V to 3.3V logic level converter** when connecting 5V sensors to the Pi. The Pi's GPIO pins are 3.3V only and can be permanently damaged by 5V signals.

#### I2C device not detected
```bash
sudo i2cdetect -y 1
```
You should see the ADS1115 at address `0x48`. If not:
- Check wiring
- Ensure I2C is enabled in `raspi-config`
- Ensure Serial is disabled

#### Adafruit library import errors
If you have a fresh Raspberry Pi OS install (2023+), Adafruit libraries have been updated. Make sure you're using:
```python
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
```

### Sensor Quality Note
Capacitive moisture sensors can vary in quality. Some arrive damaged or incorrectly manufactured. Consider purchasing from reputable sellers and testing before final assembly.

## Emotion Thresholds

Current thresholds in `sensors.py`:

| Condition | Threshold | Emotion Triggered |
|-----------|-----------|-------------------|
| Low light | < 20% | Sleepy |
| Adequate light | > 20% | Happy |
| Low moisture | < 10% | Thirsty |
| Rising moisture | 10-90% (increasing) | Savory |
| High moisture | > 90% | Savory |
| High temperature | > 30°C | Hot |
| Low temperature | < 22°C | Freeze |

Adjust these values in `sensors.py` based on your plant's needs and local climate.

## GitHub Pages Website

This project includes a complete documentation website that can be hosted on GitHub Pages.

### Setup GitHub Pages

1. Go to your GitHub repository settings
2. Navigate to **Pages** (under "Code and automation")
3. Under **Source**, select "Deploy from a branch"
4. Under **Branch**, select `main` and `/docs` folder
5. Click **Save**

Your site will be available at: `https://[username].github.io/[repository-name]/`

The website includes:
- Interactive wiring diagrams
- Complete hardware list
- Step-by-step setup guide
- Emotion showcase
- Embedded SVG schematics

### Local Preview

To preview the website locally:
```bash
# Using Python's built-in server
cd docs
python3 -m http.server 8000

# Open http://localhost:8000 in your browser
```

## Credits

- Original project by [Coders Cafe](https://github.com/CodersCafeTech)
- [Instructables Tutorial](https://www.instructables.com/Fyt%C3%B3-Turn-Your-Plant-Into-Pet/)
- Community contributions and troubleshooting tips

## License

See [LICENSE.md](LICENSE.md) for details.

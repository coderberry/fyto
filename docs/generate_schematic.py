#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "schemdraw>=0.18",
# ]
# ///
"""
Fyto Project - Schematic Diagram Generator

Generates wiring schematics for the Fyto plant monitoring project using schemdraw.
This creates a clean schematic showing all connections between:
- Raspberry Pi Zero 2W
- ADS1115 ADC
- 2-inch LCD Display
- LM35 Temperature Sensor
- Capacitive Moisture Sensor
- LDR Light Sensor

Usage:
    cd docs
    uv run generate_schematic.py

    # Or from project root:
    uv run docs/generate_schematic.py
"""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import intcircuits as ic

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "diagrams"


def create_fyto_schematic():
    """Generate the main Fyto wiring schematic."""

    schemdraw.theme('monokai')
    with schemdraw.Drawing() as d:
        d.config(unit=2, fontsize=10)

        # Title
        d += elm.Label().at((0, 12)).label('Fyto - Plant Monitor Schematic', fontsize=14, halign='left')
        d += elm.Label().at((0, 11.2)).label('Raspberry Pi Zero 2W + Sensors', fontsize=10, halign='left', color='gray')

        # ============================================
        # Raspberry Pi Zero 2W (as custom IC)
        # ============================================
        pi_pins = [
            ic.IcPin(name='3V3', pin='1', side='left'),
            ic.IcPin(name='SDA', pin='3', side='left'),
            ic.IcPin(name='SCL', pin='5', side='left'),
            ic.IcPin(name='GND', pin='9', side='left'),
            ic.IcPin(name='GPIO10', pin='19', side='left'),
            ic.IcPin(name='MOSI', pin='21', side='left'),
            ic.IcPin(name='SCLK', pin='23', side='left'),
            ic.IcPin(name='CE0', pin='24', side='right'),
            ic.IcPin(name='RST', pin='36', side='right'),
            ic.IcPin(name='DC', pin='37', side='right'),
            ic.IcPin(name='5V', pin='2', side='right'),
        ]

        d += (pi := ic.Ic(pins=pi_pins, size=(4, 6),
                         label='Raspberry Pi\nZero 2W').at((0, 5)))

        # ============================================
        # ADS1115 ADC (as custom IC)
        # ============================================
        ads_pins = [
            ic.IcPin(name='VDD', pin='VDD', side='left'),
            ic.IcPin(name='GND', pin='GND', side='left'),
            ic.IcPin(name='SCL', pin='SCL', side='left'),
            ic.IcPin(name='SDA', pin='SDA', side='left'),
            ic.IcPin(name='A0', pin='A0', side='right'),
            ic.IcPin(name='A1', pin='A1', side='right'),
            ic.IcPin(name='A2', pin='A2', side='right'),
            ic.IcPin(name='A3', pin='A3', side='right'),
        ]

        d += (ads := ic.Ic(pins=ads_pins, size=(3, 4),
                          label='ADS1115\n16-bit ADC').at((10, 6)))

        # ============================================
        # LCD Display (as custom IC)
        # ============================================
        lcd_pins = [
            ic.IcPin(name='VCC', pin='VCC', side='left'),
            ic.IcPin(name='GND', pin='GND', side='left'),
            ic.IcPin(name='DIN', pin='DIN', side='left'),
            ic.IcPin(name='CLK', pin='CLK', side='left'),
            ic.IcPin(name='CS', pin='CS', side='right'),
            ic.IcPin(name='DC', pin='DC', side='right'),
            ic.IcPin(name='RST', pin='RST', side='right'),
            ic.IcPin(name='BL', pin='BL', side='right'),
        ]

        d += (lcd := ic.Ic(pins=lcd_pins, size=(3, 4),
                          label='2" IPS LCD\n240x320').at((10, 0)))

        # ============================================
        # Sensors (simplified representations)
        # ============================================

        # LM35 Temperature Sensor
        lm35_pins = [
            ic.IcPin(name='VCC', pin='+', side='left'),
            ic.IcPin(name='OUT', pin='OUT', side='right'),
            ic.IcPin(name='GND', pin='-', side='left'),
        ]
        d += (lm35 := ic.Ic(pins=lm35_pins, size=(2, 1.5),
                           label='LM35\nTemp').at((18, 7)))

        # Moisture Sensor
        moist_pins = [
            ic.IcPin(name='VCC', pin='+', side='left'),
            ic.IcPin(name='OUT', pin='OUT', side='right'),
            ic.IcPin(name='GND', pin='-', side='left'),
        ]
        d += (moist := ic.Ic(pins=moist_pins, size=(2, 1.5),
                            label='Moisture\nSensor').at((18, 5)))

        # LDR Light Sensor
        ldr_pins = [
            ic.IcPin(name='VCC', pin='+', side='left'),
            ic.IcPin(name='OUT', pin='OUT', side='right'),
            ic.IcPin(name='GND', pin='-', side='left'),
        ]
        d += (ldr := ic.Ic(pins=ldr_pins, size=(2, 1.5),
                          label='LDR\nLight').at((18, 3)))

        # ============================================
        # Power Rails
        # ============================================

        # 3.3V Rail (red)
        d += elm.Line().at((-3, 9)).right().length(24).color('red').linewidth(2)
        d += elm.Label().at((-3, 9.3)).label('3.3V', fontsize=9, color='red')

        # GND Rail (black)
        d += elm.Line().at((-3, -2)).right().length(24).color('black').linewidth(2)
        d += elm.Label().at((-3, -1.7)).label('GND', fontsize=9, color='black')

        # ============================================
        # I2C Connections (Pi to ADS1115)
        # ============================================

        # SDA connection (blue)
        d += elm.Wire('c', k=0.5).at(pi.SDA).to(ads.SDA).color('blue')

        # SCL connection (orange)
        d += elm.Wire('c', k=0.5).at(pi.SCL).to(ads.SCL).color('orange')

        # ============================================
        # SPI Connections (Pi to LCD)
        # ============================================

        # MOSI to DIN (green)
        d += elm.Wire('c', k=-0.3).at(pi.MOSI).to(lcd.DIN).color('green')

        # SCLK to CLK (purple)
        d += elm.Wire('c', k=-0.4).at(pi.SCLK).to(lcd.CLK).color('purple')

        # CE0 to CS (brown)
        d += elm.Wire('c', k=0.3).at(pi.CE0).to(lcd.CS).color('brown')

        # DC connection
        d += elm.Wire('c', k=0.4).at(pi.DC).to(lcd.DC).color('gray')

        # RST connection
        d += elm.Wire('c', k=0.5).at(pi.RST).to(lcd.RST).color('pink')

        # BL (Backlight) connection
        d += elm.Wire('c', k=-0.2).at(pi.GPIO10).to(lcd.BL).color('cyan')

        # ============================================
        # Sensor to ADS1115 Connections
        # ============================================

        # LM35 OUT to A1
        d += elm.Wire('c', k=0.3).at(lm35.OUT).to(ads.A1).color('red')

        # Moisture OUT to A2
        d += elm.Wire('c', k=0.3).at(moist.OUT).to(ads.A2).color('brown')

        # LDR OUT to A3
        d += elm.Wire('c', k=0.3).at(ldr.OUT).to(ads.A3).color('yellow')

        # ============================================
        # Power Connections
        # ============================================

        # Pi 3V3 to power rail
        d += elm.Line().at(pi.inL1).up().toy(9).color('red')

        # Pi GND to ground rail
        d += elm.Line().at(pi.GND).down().toy(-2).color('black')

        # ADS1115 VDD to power rail
        d += elm.Line().at(ads.VDD).up().toy(9).color('red')

        # ADS1115 GND to ground rail
        d += elm.Line().at(ads.GND).down().toy(-2).color('black')

        # LCD VCC to power rail
        d += elm.Line().at(lcd.VCC).up().toy(9).color('red')

        # LCD GND to ground rail
        d += elm.Line().at(lcd.GND).down().toy(-2).color('black')

        # Sensor power connections
        d += elm.Line().at(lm35.VCC).up().toy(9).color('red')
        d += elm.Line().at(lm35.GND).down().toy(-2).color('black')

        d += elm.Line().at(moist.VCC).up().toy(9).color('red')
        d += elm.Line().at(moist.GND).down().toy(-2).color('black')

        d += elm.Line().at(ldr.VCC).up().toy(9).color('red')
        d += elm.Line().at(ldr.GND).down().toy(-2).color('black')

        # ============================================
        # Legend
        # ============================================
        legend_x = -3
        legend_y = -4

        d += elm.Label().at((legend_x, legend_y)).label('Wire Color Legend:', fontsize=10, halign='left')
        d += elm.Line().at((legend_x, legend_y - 0.5)).right().length(0.5).color('red').linewidth(2)
        d += elm.Label().at((legend_x + 0.7, legend_y - 0.5)).label('3.3V Power', fontsize=8, halign='left')

        d += elm.Line().at((legend_x, legend_y - 1)).right().length(0.5).color('black').linewidth(2)
        d += elm.Label().at((legend_x + 0.7, legend_y - 1)).label('Ground', fontsize=8, halign='left')

        d += elm.Line().at((legend_x, legend_y - 1.5)).right().length(0.5).color('blue').linewidth(2)
        d += elm.Label().at((legend_x + 0.7, legend_y - 1.5)).label('I2C SDA', fontsize=8, halign='left')

        d += elm.Line().at((legend_x, legend_y - 2)).right().length(0.5).color('orange').linewidth(2)
        d += elm.Label().at((legend_x + 0.7, legend_y - 2)).label('I2C SCL', fontsize=8, halign='left')

        d += elm.Line().at((legend_x + 5, legend_y - 0.5)).right().length(0.5).color('green').linewidth(2)
        d += elm.Label().at((legend_x + 5.7, legend_y - 0.5)).label('SPI MOSI', fontsize=8, halign='left')

        d += elm.Line().at((legend_x + 5, legend_y - 1)).right().length(0.5).color('purple').linewidth(2)
        d += elm.Label().at((legend_x + 5.7, legend_y - 1)).label('SPI SCLK', fontsize=8, halign='left')

        d += elm.Line().at((legend_x + 5, legend_y - 1.5)).right().length(0.5).color('brown').linewidth(2)
        d += elm.Label().at((legend_x + 5.7, legend_y - 1.5)).label('SPI CS / Moisture', fontsize=8, halign='left')

        d += elm.Line().at((legend_x + 5, legend_y - 2)).right().length(0.5).color('yellow').linewidth(2)
        d += elm.Label().at((legend_x + 5.7, legend_y - 2)).label('LDR Signal', fontsize=8, halign='left')

        # Save the schematic (SVG only - use browser/Inkscape to convert to PNG)
        svg_path = OUTPUT_DIR / 'fyto_schematic.svg'
        d.save(str(svg_path))
        print(f"Schematic saved to {svg_path}")


def create_connection_table():
    """Generate a simple connection reference diagram."""

    with schemdraw.Drawing() as d:
        d.config(unit=1.5, fontsize=9)

        # Title
        d += elm.Label().at((0, 16)).label('Fyto - Pin Connection Reference', fontsize=14, halign='left')

        # Pi Zero header representation
        d += elm.Label().at((0, 14)).label('Raspberry Pi Zero 2W GPIO Header', fontsize=11, halign='left')

        # Create a simplified 40-pin header visualization
        header_x = 1
        header_y = 12

        # Draw pin header outline
        d += elm.Line().at((header_x - 0.3, header_y + 0.3)).right().length(5)
        d += elm.Line().at((header_x - 0.3, header_y + 0.3)).down().length(10.6)
        d += elm.Line().at((header_x - 0.3, header_y - 10.3)).right().length(5)
        d += elm.Line().at((header_x + 4.7, header_y + 0.3)).down().length(10.6)

        # Pin definitions (physical pin number: function)
        left_pins = {
            1: ('3V3', 'red'),
            3: ('SDA', 'blue'),
            5: ('SCL', 'orange'),
            9: ('GND', 'black'),
            19: ('BL', 'cyan'),
            21: ('MOSI', 'green'),
            23: ('SCLK', 'purple'),
        }

        right_pins = {
            2: ('5V', 'red'),
            24: ('CE0', 'brown'),
            36: ('RST', 'pink'),
            37: ('DC', 'gray'),
        }

        # Draw left side pins (odd numbers)
        for pin_num in range(1, 40, 2):
            y_pos = header_y - ((pin_num - 1) / 2) * 0.5
            d += elm.Dot(radius=0.08).at((header_x, y_pos))
            d += elm.Label().at((header_x - 0.2, y_pos)).label(str(pin_num), fontsize=7, halign='right')

            if pin_num in left_pins:
                name, color = left_pins[pin_num]
                d += elm.Line().at((header_x, y_pos)).left().length(1).color(color).linewidth(2)
                d += elm.Label().at((header_x - 1.2, y_pos)).label(name, fontsize=8, halign='right', color=color)

        # Draw right side pins (even numbers)
        for pin_num in range(2, 41, 2):
            y_pos = header_y - ((pin_num - 2) / 2) * 0.5
            d += elm.Dot(radius=0.08).at((header_x + 0.5, y_pos))
            d += elm.Label().at((header_x + 0.7, y_pos)).label(str(pin_num), fontsize=7, halign='left')

            if pin_num in right_pins:
                name, color = right_pins[pin_num]
                d += elm.Line().at((header_x + 0.5, y_pos)).right().length(1).color(color).linewidth(2)
                d += elm.Label().at((header_x + 1.7, y_pos)).label(name, fontsize=8, halign='left', color=color)

        # Connection tables
        table_x = 8

        # LCD Connections
        d += elm.Label().at((table_x, 14)).label('LCD Display Connections', fontsize=11, halign='left')
        lcd_connections = [
            ('VCC', '->', 'Pin 1 (3V3)'),
            ('GND', '->', 'Pin 9 (GND)'),
            ('DIN', '->', 'Pin 21 (MOSI)'),
            ('CLK', '->', 'Pin 23 (SCLK)'),
            ('CS', '->', 'Pin 24 (CE0)'),
            ('DC', '->', 'Pin 37 (GPIO26)'),
            ('RST', '->', 'Pin 36 (GPIO16)'),
            ('BL', '->', 'Pin 19 (GPIO10)'),
        ]
        for i, (src, arrow, dst) in enumerate(lcd_connections):
            d += elm.Label().at((table_x, 13 - i * 0.5)).label(f'{src} {arrow} {dst}', fontsize=8, halign='left')

        # ADS1115 Connections
        d += elm.Label().at((table_x, 8)).label('ADS1115 ADC Connections', fontsize=11, halign='left')
        ads_connections = [
            ('VDD', '->', 'Pin 1 (3V3)'),
            ('GND', '->', 'Pin 9 (GND)'),
            ('SCL', '->', 'Pin 5 (SCL)'),
            ('SDA', '->', 'Pin 3 (SDA)'),
            ('A1', '->', 'LM35 OUT'),
            ('A2', '->', 'Moisture OUT'),
            ('A3', '->', 'LDR OUT'),
        ]
        for i, (src, arrow, dst) in enumerate(ads_connections):
            d += elm.Label().at((table_x, 7 - i * 0.5)).label(f'{src} {arrow} {dst}', fontsize=8, halign='left')

        # Sensor Connections
        d += elm.Label().at((table_x, 3)).label('Sensor Connections', fontsize=11, halign='left')
        sensor_info = [
            'All sensors: VCC -> 3V3, GND -> GND',
            'LM35 Temp: OUT -> ADS1115 A1',
            'Moisture: OUT -> ADS1115 A2',
            'LDR Light: OUT -> ADS1115 A3',
        ]
        for i, info in enumerate(sensor_info):
            d += elm.Label().at((table_x, 2.3 - i * 0.5)).label(info, fontsize=8, halign='left')

        svg_path = OUTPUT_DIR / 'fyto_pinout.svg'
        d.save(str(svg_path))
        print(f"Pinout reference saved to {svg_path}")


if __name__ == '__main__':
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Fyto schematics...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    create_fyto_schematic()
    create_connection_table()

    print()
    print("Done! Generated files:")
    for f in OUTPUT_DIR.iterdir():
        print(f"  - {f.name}")

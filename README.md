# Raspberry Pi Antenna Analyzer - One-Click Testing System

A comprehensive antenna testing system for Raspberry Pi that provides **one-click frequency sweep and automatic antenna rating**. Built for ham radio operators, antenna designers, and RF engineers.

## 🚀 Features

- **One-Click Operation**: Single button to perform complete frequency sweep and rate antenna performance
- **Automatic Rating**: Intelligent scoring system (A+ to F) based on SWR measurements
- **Real-time Visualization**: Live SWR plots with reference lines
- **Comprehensive Analysis**: Detailed performance metrics and recommendations
- **Multiple Interfaces**: GUI application and command-line quick test
- **Data Export**: Save results in JSON format for further analysis

## 🛠 Hardware Requirements

### Main Components

- **Raspberry Pi 4GB** (already owned)
- **AD9850 DDS Module** (~$15) - Signal generator (1Hz to 40MHz)
- **AD8302 RF Detector** (~$20) - Measures signal phase and magnitude
- **MCP3008 ADC** (~$3) - Analog to digital converter
- **Directional Coupler** (~$10) - Separates forward/reflected signals

**Total cost: ~$48**

### Connections

```
AD9850 → Raspberry Pi:
VCC     → 3.3V (Pin 1)
GND     → GND (Pin 6)
DATA    → GPIO 23 (Pin 16)
W_CLK   → GPIO 18 (Pin 12)
FQ_UD   → GPIO 24 (Pin 18)
RESET   → GPIO 25 (Pin 22)

AD8302 → MCP3008:
VMAG    → CH0
VPHS    → CH1

MCP3008 → Raspberry Pi:
VDD     → 3.3V
GND     → GND
CLK     → SPI0 SCLK (Pin 23)
DOUT    → SPI0 MISO (Pin 21)
DIN     → SPI0 MOSI (Pin 19)
CS      → SPI0 CE0 (Pin 24)

RF Signal Path:
AD9850 OUT → Directional Coupler INPUT
           → Coupler FWD → AD8302 INPA
           → Coupler REF → AD8302 INPB
           → Coupler OUT → Antenna Under Test
```

## 📦 Installation

### 1. Setup Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python packages
sudo apt install python3-pip python3-numpy python3-matplotlib python3-tk

# Install Python dependencies
pip3 install -r requirements.txt

# Enable SPI interface
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable
sudo reboot
```

### 2. Install Application

```bash
# Clone or download the files
git clone <repository-url>
cd rapsi_antenna_tester

# Make scripts executable
chmod +x antenna_tester.py
chmod +x quick_test.py
```

## 🎯 Usage

### GUI Application (Recommended)

```bash
python3 antenna_tester.py
```

**Features:**
- Set frequency range (start/stop) and number of measurement points
- Click "🚀 ONE-CLICK SWEEP & RATE" button
- Real-time progress bar and status updates
- Automatic antenna rating with color-coded results
- Live SWR plot with reference lines
- Detailed analysis and recommendations
- Save/load results functionality

### Command Line Quick Test

```bash
python3 quick_test.py
```

**Features:**
- Predefined test parameters (1-30 MHz, 50 points)
- Progress bar with percentage completion
- Comprehensive text-based results
- Automatic file saving
- Perfect for automated testing

## 📊 Understanding Results

### Rating System

| Grade | Score | Performance |
|-------|-------|-------------|
| **A+** | 90-100 | Excellent - No adjustment needed |
| **A**  | 85-89  | Excellent - Minor tuning possible |
| **A-** | 80-84  | Very Good - Small improvements possible |
| **B+** | 75-79  | Good - Some tuning recommended |
| **B**  | 70-74  | Good - Moderate adjustments |
| **B-** | 65-69  | Acceptable - Tuning needed |
| **C+** | 60-64  | Poor - Significant adjustment required |
| **C**  | 55-59  | Poor - Major tuning needed |
| **C-** | 50-54  | Very Poor - Redesign recommended |
| **D**  | 40-49  | Bad - Complete redesign needed |
| **F**  | 0-39   | Failed - Antenna not functional |

### SWR Guidelines

- **SWR ≤ 1.5**: Excellent performance
- **SWR ≤ 2.0**: Good performance  
- **SWR ≤ 3.0**: Acceptable for most applications
- **SWR > 3.0**: Poor performance, adjustment needed

### Key Metrics

- **Minimum SWR**: Best resonance point
- **Usable Bandwidth**: Frequency range with SWR ≤ 2.0
- **Resonant Frequency**: Frequency with lowest SWR
- **Coverage Ratio**: Percentage of frequencies with good SWR

## 🔧 Calibration

For accurate measurements, perform calibration:

1. **Short Circuit**: Connect short to antenna port
2. **Open Circuit**: Leave antenna port open  
3. **50Ω Load**: Connect known 50Ω load

*Note: Calibration feature will be added in future version*

## 📁 File Outputs

### GUI Results (JSON format)
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "parameters": {
    "start_freq_mhz": 1.0,
    "stop_freq_mhz": 30.0,
    "points": 100
  },
  "measurements": [...],
  "rating": {
    "rating": "A",
    "score": 87,
    "analysis": "..."
  }
}
```

### Quick Test Results (Text format)
```
ANTENNA QUICK TEST RESULTS
==================================================

Test Date: 2024-01-15 10:30:00
Rating: A (87/100)

ANALYSIS:
Minimum SWR: 1.45
Average SWR: 2.1
...
```

## 🛠 Troubleshooting

### Hardware Issues

**"Hardware not ready" error:**
- Check all GPIO connections
- Verify SPI is enabled: `ls /dev/spi*`
- Ensure modules are powered correctly
- Check for loose connections

**Inconsistent readings:**
- Add RF shielding to sensitive circuits
- Use shorter connection cables
- Ensure proper grounding
- Check for interference sources

### Software Issues

**Import errors:**
```bash
# Install missing packages
pip3 install RPi.GPIO spidev numpy matplotlib
```

**Permission errors:**
```bash
# Add user to SPI group
sudo usermod -a -G spi pi
```

## 🔬 Technical Specifications

- **Frequency Range**: 1 Hz - 40 MHz (AD9850 limitation)
- **Frequency Resolution**: 32-bit (0.029 Hz steps)
- **SWR Range**: 1.0 - 50+ (software limited)
- **Measurement Speed**: ~100ms per frequency point
- **ADC Resolution**: 10-bit (1024 levels)
- **Voltage Reference**: 3.3V

## 🎯 Applications

- **Ham Radio**: Antenna tuning and analysis
- **RF Design**: Prototype antenna evaluation  
- **Education**: Learning antenna principles
- **QC Testing**: Production antenna verification
- **Field Work**: Portable antenna measurement

## 🔮 Future Enhancements

- [ ] Calibration system implementation
- [ ] Impedance measurement (R + jX)
- [ ] Return loss calculations
- [ ] Smith chart display
- [ ] Frequency band presets
- [ ] Remote operation via web interface
- [ ] Data logging and trends

## 📝 License

Open source - Feel free to modify and distribute

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Calibration algorithms
- Additional measurement parameters
- UI/UX enhancements
- Hardware compatibility
- Documentation improvements

---

**Happy antenna testing! 📡** 
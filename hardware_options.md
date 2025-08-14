# Simple Antenna Analyzer

## Hardware Setup

### Components Needed:

#### **Raspberry Pi 4GB** (already owned)
- **Purpose**: Main processing unit running the analyzer software
- **Function**: Controls all modules, processes measurements, generates user interface, and performs calculations
- **Connections**: Provides GPIO pins for digital control signals, SPI interface for ADC communication, and power supply for connected modules
- **Role in System**: Acts as the central controller coordinating frequency generation, signal measurement, and data analysis

#### **AD9850 DDS Module**
- **Purpose**: Digital Direct Synthesis signal generator that creates precise test frequencies
- **Function**: Generates clean sine wave signals from 1Hz to 40MHz for antenna testing
- **Technical Details**: Uses phase accumulator and DAC to create frequencies with 32-bit resolution
- **Connection to System**: Connected to Raspberry Pi GPIO pins for digital control (DATA, W_CLK, FQ_UD, RESET)
- **Signal Output**: RF output connects to directional coupler input to inject test signal into antenna
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4682284022-s27000512992.html)

#### **AD8302 RF Detector**
- **Purpose**: Dual logarithmic amplifier for measuring RF signal magnitude and phase
- **Function**: Simultaneously measures forward and reflected signal levels to calculate SWR
- **Technical Details**: Provides linear voltage outputs proportional to signal magnitude and phase difference
- **Input Connections**: 
  - INPA receives forward signal from directional coupler
  - INPB receives reflected signal from directional coupler
- **Output Connections**: 
  - VMAG (magnitude) and VPHS (phase) connect to MCP3008 ADC inputs
- **Power Requirements**: Requires +5V supply (external power recommended)
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4931232200-s28732350592.html)

#### **Directional Coupler**
- **Purpose**: RF component that separates forward and reflected signals
- **Function**: Allows simultaneous measurement of power going to antenna and power reflected back
- **Technical Details**: Uses coupled transmission lines to sample forward and reverse power
- **Connection Points**:
  - INPUT: Receives test signal from AD9850 DDS module
  - OUTPUT: Connects to antenna under test
  - FWD (Forward): Samples forward power, connects to AD8302 INPA
  - REF (Reflected): Samples reflected power, connects to AD8302 INPB
- **Frequency Range**: Typically operates from HF through VHF frequencies
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4871092638-s28286101362.html)

#### **Battery Power Supply**
- **Purpose**: Provides portable power for field antenna testing
- **Function**: 18650 battery shield supplies power to Raspberry Pi and connected modules
- **Connection**: Powers Raspberry Pi via USB or GPIO power pins
- **Advantage**: Enables antenna testing in remote locations without AC power
- [Battery Shield Link](https://www.lazada.com.ph/products/pdp-i4758996149-s27482027236.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Abattery%252Bshield%252Bf%252B18650%253Bnid%253A4758996149%253Bsrc%253ALazadaMainSrp%253Brn%253Afa7b5cf8e6fcf47df4401609a0dd8c62%253Bregion%253Aph%253Bsku%253A4758996149_PH%253Bprice%253A481%253Bclient%253Adesktop%253Bsupplier_id%253A1000253703%253Bbiz_source%253Ah5_internal%253Bslot%253A1%253Butlog_bucket_id%253A470687%253Basc_category_id%253A22654%253Bitem_id%253A4758996149%253Bsku_id%253A27482027236%253Bshop_id%253A426832%253BtemplateInfo%253A107881_A3_D_E%25231103_L%2523-1_C%2523&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=China&price=481&priceCompare=skuId%3A27482027236%3Bsource%3Alazada-search-voucher%3Bsn%3Afa7b5cf8e6fcf47df4401609a0dd8c62%3BoriginPrice%3A48100%3BdisplayPrice%3A48100%3BsinglePromotionId%3A900000052234180%3BsingleToolCode%3ApromPrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1749886401090&ratingscore=&request_id=fa7b5cf8e6fcf47df4401609a0dd8c62&review=&sale=0&search=1&source=search&spm=a2o4l.searchlist.list.1&stock=1)

#### **Display Screen (Optional)**
- **Purpose**: Provides local display for antenna analyzer readings
- **Function**: Shows real-time SWR measurements, frequency sweeps, and graphs
- **Options**: 3.5", 5", or 7" HDMI touchscreen displays
- **Connection**: HDMI output from Raspberry Pi
- **Benefit**: Enables standalone operation without external computer
- [Display Options](https://www.lazada.com.ph/products/for-raspberry-pi-3b3b4b-display-35-inch-display-5-inch-raspberry-7-inch-hdmi-touch-screen-i299354170-s6934658106.html?)

#### **MCP3008 ADC**
- **Purpose**: 8-channel 10-bit Analog-to-Digital Converter
- **Function**: Converts analog voltage outputs from AD8302 to digital values for Raspberry Pi
- **Technical Details**: 
  - 10-bit resolution (1024 levels)
  - 8 single-ended input channels
  - SPI interface for communication
- **Connection to System**:
  - CH0 connects to AD8302 VMAG (magnitude measurement)
  - CH1 connects to AD8302 VPHS (phase measurement)
  - SPI interface connects to Raspberry Pi SPI0 port
- **Power Supply**: 3.3V from Raspberry Pi
- **Role**: Critical interface between analog RF measurements and digital processing

---

## Component Pinouts

### AD8302 RF Detector Pinout:
**Purpose**: Each pin serves a specific function in the logarithmic amplifier operation

```
AD8302 Module:
Pin 1  - COMM     (Common/Ground) - Reference ground for all signals
Pin 2  - INPA     (RF Input A - Forward signal) - Receives forward power sample
Pin 3  - OFSA     (Offset A) - Magnitude offset adjustment for calibration
Pin 4  - VPOS     (+5V Power) - Positive power supply input
Pin 5  - OFST     (Offset) - Phase offset adjustment for calibration  
Pin 6  - INPB     (RF Input B - Reflected signal) - Receives reflected power sample
Pin 7  - COMM     (Common/Ground) - Additional ground connection

Pin 8  - VFLT     (Filter voltage) - External filter capacitor connection
Pin 9  - VPHS     (Phase output voltage) - Linear voltage proportional to phase difference
Pin 10 - VREF     (Reference voltage) - Internal reference voltage output
Pin 11 - MSET     (Magnitude set) - Magnitude measurement range setting
Pin 12 - VMAG     (Magnitude output voltage) - Linear voltage proportional to signal ratio
Pin 13 - MFLT     (Magnitude filter) - Magnitude output filter connection
Pin 14 - VCC      (+5V Power) - Secondary power input
```

### AD9850 DDS Module Pinout:
**Purpose**: Digital control interface for frequency synthesis

```
AD9850 Module:
VCC    - +3.3V or +5V Power - Powers the DDS chip and supporting circuitry
GND    - Ground - Reference ground for all signals
DATA   - Serial data input - Receives 32-bit frequency control word serially
W_CLK  - Word clock - Clock signal for shifting in data bits
FQ_UD  - Frequency update - Latches new frequency setting when pulsed
RESET  - Reset (active high) - Resets DDS to default state when high
OUT    - RF signal output - Sine wave output at programmed frequency
OUTB   - Inverted RF output (not used) - Complementary output (unused)
```

### MCP3008 ADC Pinout:
**Purpose**: Analog-to-digital conversion with SPI interface

```
MCP3008:
Pin 1  - CH0     (Analog input 0) - Connected to AD8302 VMAG for magnitude
Pin 2  - CH1     (Analog input 1) - Connected to AD8302 VPHS for phase
Pin 3  - CH2     (Analog input 2) - Unused analog input
Pin 4  - CH3     (Analog input 3) - Unused analog input
Pin 5  - CH4     (Analog input 4) - Unused analog input  
Pin 6  - CH5     (Analog input 5) - Unused analog input
Pin 7  - CH6     (Analog input 6) - Unused analog input
Pin 8  - CH7     (Analog input 7) - Unused analog input
Pin 9  - DGND    (Digital ground) - Ground reference for digital signals
Pin 10 - CS      (Chip select) - SPI chip select (active low)
Pin 11 - DIN     (Data input) - SPI data input from Raspberry Pi
Pin 12 - DOUT    (Data output) - SPI data output to Raspberry Pi
Pin 13 - CLK     (Clock) - SPI clock signal
Pin 14 - AGND    (Analog ground) - Ground reference for analog signals
Pin 15 - VREF    (Reference voltage) - ADC reference voltage (3.3V)
Pin 16 - VDD     (Power supply) - Digital power supply (3.3V)
```

### Raspberry Pi GPIO Pinout (relevant pins):
**Purpose**: Interface connections between Raspberry Pi and modules

```
Physical Pin → GPIO → Function → Connected To
Pin 1        → 3.3V → Power → MCP3008 VDD, VREF; AD9850 VCC
Pin 6        → GND  → Ground → All module ground connections
Pin 12       → 18   → W_CLK (AD9850) → AD9850 word clock input
Pin 16       → 23   → DATA (AD9850) → AD9850 serial data input
Pin 18       → 24   → FQ_UD (AD9850) → AD9850 frequency update
Pin 19       → 10   → SPI0_MOSI → MCP3008 DIN (data to ADC)
Pin 21       → 9    → SPI0_MISO → MCP3008 DOUT (data from ADC)
Pin 22       → 25   → RESET (AD9850) → AD9850 reset control
Pin 23       → 11   → SPI0_SCLK → MCP3008 CLK (SPI clock)
Pin 24       → 8    → SPI0_CE0 → MCP3008 CS (chip select)
```

---

## How to Build

### Step 1: Wiring Connections

#### AD9850 DDS Module to Raspberry Pi:
**Purpose**: Provides digital control of frequency generation
```
AD9850    →    Raspberry Pi    →    Function
VCC       →    3.3V (Pin 1)    →    Power supply for DDS chip
GND       →    GND (Pin 6)     →    Common ground reference
DATA      →    GPIO 23 (Pin 16) →   Serial data for frequency control
W_CLK     →    GPIO 18 (Pin 12) →   Clock for data shifting
FQ_UD     →    GPIO 24 (Pin 18) →   Update signal for new frequency
RESET     →    GPIO 25 (Pin 22) →   Reset control for initialization
```

#### AD8302 RF Detector to Raspberry Pi:
**Purpose**: Measures RF signal levels and converts to analog voltages
```
AD8302    →    Connection      →    Function
VPOS      →    5V (external)   →    Power supply (requires 5V, not 3.3V)
COMM      →    GND (Pin 6)     →    Ground reference
VMAG      →    MCP3008 CH0     →    Magnitude measurement to ADC
VPHS      →    MCP3008 CH1     →    Phase measurement to ADC
```

#### MCP3008 ADC to Raspberry Pi:
**Purpose**: Converts analog measurements to digital data via SPI
```
MCP3008   →    Raspberry Pi    →    Function
VDD       →    3.3V (Pin 1)    →    Digital power supply
VREF      →    3.3V (Pin 1)    →    ADC reference voltage
AGND      →    GND (Pin 6)     →    Analog ground
DGND      →    GND (Pin 6)     →    Digital ground
CLK       →    SPI0 SCLK (Pin 23) → SPI clock signal
DOUT      →    SPI0 MISO (Pin 21) → Data from ADC to Pi
DIN       →    SPI0 MOSI (Pin 19) → Data from Pi to ADC
CS        →    SPI0 CE0 (Pin 24)  → Chip select (enables ADC)

CH0       →    AD8302 VMAG     →    Receives magnitude voltage
CH1       →    AD8302 VPHS     →    Receives phase voltage
```

#### RF Signal Path:
**Purpose**: Routes test signals through the measurement system
```
Signal Flow Direction:
AD9850 OUT → Directional Coupler INPUT (Test signal injection)
Directional Coupler FWD → AD8302 INPA (Forward power sample)
Directional Coupler REF → AD8302 INPB (Reflected power sample)  
Directional Coupler OUTPUT → Antenna Under Test (Test signal to antenna)
```

### Step 2: Software Setup

#### Install Required Packages:
```bash
sudo apt update
sudo apt install python3-pip python3-numpy python3-matplotlib
pip3 install RPi.GPIO spidev
```

#### Enable SPI:
**Purpose**: Activates hardware SPI interface for ADC communication
```bash
sudo raspi-config
# Navigate to: Interfacing Options → SPI → Enable
sudo reboot
```

### Step 3: Assembly

1. **Mount components** on a breadboard or PCB
   - **Purpose**: Provides mechanical support and organized connections
   - **Considerations**: Use proper RF grounding techniques for high-frequency signals

2. **Connect all wires** according to the wiring diagram above
   - **Wire Types**: Use appropriate wire gauges and types (coax for RF signals)
   - **Grounding**: Ensure solid ground connections for accurate measurements

3. **Add BNC connectors** for antenna connection
   - **Purpose**: Provides standard 50-ohm RF interface for antenna testing
   - **Installation**: Mount on enclosure with proper grounding

4. **Install in enclosure** (optional but recommended)
   - **Benefits**: Protects circuits, provides RF shielding, enables portable use
   - **Considerations**: Include ventilation and access to controls

### Step 4: Calibration

#### Why Calibration is Critical:
Calibration compensates for system errors and ensures accurate measurements

1. **Short circuit calibration**: Connect a short to the antenna port
   - **Purpose**: Establishes reference for 100% reflection (infinite SWR)
   - **Measurement**: Records system response to perfect reflector

2. **Open circuit calibration**: Leave antenna port open
   - **Purpose**: Another reference for 100% reflection with different phase
   - **Measurement**: Records system response to open termination

3. **50Ω load calibration**: Connect a known 50Ω load
   - **Purpose**: Establishes reference for zero reflection (SWR = 1:1)
   - **Measurement**: Records system response to perfect match

### Step 5: Testing

1. **Run the Python script**
   - **Function**: Initializes all modules and starts measurement software

2. **Connect a known good antenna**
   - **Purpose**: Provides realistic test load with known characteristics

3. **Perform frequency sweep**
   - **Process**: Automatically steps through frequency range taking measurements

4. **Verify SWR readings make sense**
   - **Validation**: Compare results with expected antenna characteristics

---

## What It Can Measure

- **SWR (Standing Wave Ratio)**: Indicates antenna impedance match quality
- **Impedance** (R + jX): Complex impedance showing resistance and reactance
- **Return Loss**: Power ratio between incident and reflected signals (in dB)
- **Frequency sweeps**: Automated measurements across frequency ranges (1Hz - 40MHz)
- **Resonant frequency**: Frequency where antenna impedance is purely resistive

---

## Simple Code Example

```python
import RPi.GPIO as GPIO
import spidev
import time
import numpy as np
import matplotlib.pyplot as plt

class SimpleAntennaAnalyzer:
    def __init__(self):
        # AD9850 pins
        self.W_CLK = 18
        self.FQ_UD = 24
        self.DATA = 23
        self.RESET = 25
        
        # Setup
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.setup_gpio()
        self.reset_dds()
    
    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.W_CLK, self.FQ_UD, self.DATA, self.RESET], GPIO.OUT)
        GPIO.output([self.W_CLK, self.FQ_UD, self.DATA], GPIO.LOW)
        GPIO.output(self.RESET, GPIO.HIGH)
    
    def reset_dds(self):
        GPIO.output(self.RESET, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.RESET, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.RESET, GPIO.HIGH)
    
    def set_frequency(self, freq_hz):
        # Calculate frequency word
        freq_word = int((freq_hz * 4294967296.0) / 125000000.0)
        
        # Send frequency data
        for i in range(32):
            GPIO.output(self.DATA, (freq_word >> (31-i)) & 1)
            GPIO.output(self.W_CLK, GPIO.HIGH)
            GPIO.output(self.W_CLK, GPIO.LOW)
        
        # Send control byte
        for i in range(8):
            GPIO.output(self.DATA, GPIO.LOW)
            GPIO.output(self.W_CLK, GPIO.HIGH)
            GPIO.output(self.W_CLK, GPIO.LOW)
        
        # Update
        GPIO.output(self.FQ_UD, GPIO.HIGH)
        GPIO.output(self.FQ_UD, GPIO.LOW)
    
    def read_adc(self, channel):
        # Read MCP3008 ADC
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        voltage = (data * 3.3) / 1024.0
        return voltage
    
    def read_swr(self):
        # Read AD8302 via ADC
        mag_voltage = self.read_adc(0)  # Channel 0 = magnitude
        
        # Convert to SWR
        mag_db = (mag_voltage - 0.9) / 0.03
        reflection_coeff = 10 ** (mag_db / 20)
        
        if reflection_coeff >= 1.0:
            return 999
        else:
            return (1 + reflection_coeff) / (1 - reflection_coeff)
    
    def measure_frequency(self, freq_hz):
        self.set_frequency(freq_hz)
        time.sleep(0.01)
        return self.read_swr()
    
    def sweep(self, start_freq, stop_freq, points=50):
        frequencies = np.linspace(start_freq, stop_freq, points)
        swr_data = []
        
        for freq in frequencies:
            swr = self.measure_frequency(freq)
            swr_data.append(swr)
            print(f"{freq/1e6:.2f} MHz: SWR {swr:.2f}")
        
        return frequencies, swr_data
    
    def plot_swr(self, frequencies, swr_data):
        plt.figure(figsize=(10, 6))
        plt.plot(frequencies/1e6, swr_data)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('SWR')
        plt.title('Antenna SWR')
        plt.grid(True)
        plt.ylim(1, 10)
        plt.show()

# Usage
if __name__ == "__main__":
    analyzer = SimpleAntennaAnalyzer()
    
    # Test single frequency
    swr = analyzer.measure_frequency(14.2e6)  # 14.2 MHz
    print(f"SWR at 14.2 MHz: {swr:.2f}")
    
    # Frequency sweep
    freqs, swr_vals = analyzer.sweep(10e6, 30e6, 100)
    analyzer.plot_swr(freqs, swr_vals)
```

---

## Usage

1. **Connect the hardware components** according to the detailed wiring diagrams
2. **Run the Python script** to initialize all modules and start measurements
3. **Test individual frequencies** or perform automated frequency sweeps
4. **View SWR plots** to analyze antenna performance and identify resonant frequencies

This comprehensive setup provides professional-grade antenna analysis capabilities with detailed explanations of each component's role and connections.

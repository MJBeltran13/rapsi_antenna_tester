# Simple Antenna Analyzer

## Hardware Setup

### Components Needed:

#### **Raspberry Pi 4GB** (already owned)
- Main processing unit running the analyzer software

#### **AD9850 DDS Module** (~$15)
- Generates test signals from 1Hz to 40MHz
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4682284022-s27000512992.html)

#### **AD8302 RF Detector** (~$20)
- Measures signal phase and magnitude
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4931232200-s28732350592.html)

#### **Directional Coupler** (~$10)
- Separates forward and reflected signals
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4871092638-s28286101362.html)

battery https://www.lazada.com.ph/products/pdp-i4758996149-s27482027236.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Abattery%252Bshield%252Bf%252B18650%253Bnid%253A4758996149%253Bsrc%253ALazadaMainSrp%253Brn%253Afa7b5cf8e6fcf47df4401609a0dd8c62%253Bregion%253Aph%253Bsku%253A4758996149_PH%253Bprice%253A481%253Bclient%253Adesktop%253Bsupplier_id%253A1000253703%253Bbiz_source%253Ah5_internal%253Bslot%253A1%253Butlog_bucket_id%253A470687%253Basc_category_id%253A22654%253Bitem_id%253A4758996149%253Bsku_id%253A27482027236%253Bshop_id%253A426832%253BtemplateInfo%253A107881_A3_D_E%25231103_L%2523-1_C%2523&freeshipping=1&fs_ab=2&fuse_fs=&lang=en&location=China&price=481&priceCompare=skuId%3A27482027236%3Bsource%3Alazada-search-voucher%3Bsn%3Afa7b5cf8e6fcf47df4401609a0dd8c62%3BoriginPrice%3A48100%3BdisplayPrice%3A48100%3BsinglePromotionId%3A900000052234180%3BsingleToolCode%3ApromPrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1749886401090&ratingscore=&request_id=fa7b5cf8e6fcf47df4401609a0dd8c62&review=&sale=0&search=1&source=search&spm=a2o4l.searchlist.list.1&stock=1


screen 
https://www.lazada.com.ph/products/for-raspberry-pi-3b3b4b-display-35-inch-display-5-inch-raspberry-7-inch-hdmi-touch-screen-i299354170-s6934658106.html?


#### **MCP3008 ADC** (~$3)
- Converts analog signals to digital for Raspberry Pi

**Total cost: ~$48**

---

## Component Pinouts

### AD8302 RF Detector Pinout:
```
AD8302 Module:
Pin 1  - COMM     (Common/Ground)
Pin 2  - INPA     (RF Input A - Forward signal)
Pin 3  - OFSA     (Offset A)
Pin 4  - VPOS     (+5V Power)
Pin 5  - OFST     (Offset)
Pin 6  - INPB     (RF Input B - Reflected signal)
Pin 7  - COMM     (Common/Ground)

Pin 8  - VFLT     (Filter voltage)
Pin 9  - VPHS     (Phase output voltage)
Pin 10 - VREF     (Reference voltage)
Pin 11 - MSET     (Magnitude set)
Pin 12 - VMAG     (Magnitude output voltage)
Pin 13 - MFLT     (Magnitude filter)
Pin 14 - VCC      (+5V Power)
```

### AD9850 DDS Module Pinout:
```
AD9850 Module:
VCC    - +3.3V or +5V Power
GND    - Ground
DATA   - Serial data input
W_CLK  - Word clock
FQ_UD  - Frequency update
RESET  - Reset (active high)
OUT    - RF signal output
OUTB   - Inverted RF output (not used)
```

### MCP3008 ADC Pinout:
```
MCP3008:
Pin 1  - CH0     (Analog input 0)
Pin 2  - CH1     (Analog input 1)
Pin 3  - CH2     (Analog input 2)
Pin 4  - CH3     (Analog input 3)
Pin 5  - CH4     (Analog input 4)
Pin 6  - CH5     (Analog input 5)
Pin 7  - CH6     (Analog input 6)
Pin 8  - CH7     (Analog input 7)
Pin 9  - DGND    (Digital ground)
Pin 10 - CS      (Chip select)
Pin 11 - DIN     (Data input)
Pin 12 - DOUT    (Data output)
Pin 13 - CLK     (Clock)
Pin 14 - AGND    (Analog ground)
Pin 15 - VREF    (Reference voltage)
Pin 16 - VDD     (Power supply)
```

### Raspberry Pi GPIO Pinout (relevant pins):
```
Physical Pin → GPIO → Function
Pin 1        → 3.3V → Power
Pin 6        → GND  → Ground
Pin 12       → 18   → W_CLK (AD9850)
Pin 16       → 23   → DATA (AD9850)
Pin 18       → 24   → FQ_UD (AD9850)
Pin 19       → 10   → SPI0_MOSI
Pin 21       → 9    → SPI0_MISO
Pin 22       → 25   → RESET (AD9850)
Pin 23       → 11   → SPI0_SCLK
Pin 24       → 8    → SPI0_CE0
```

---

## How to Build

### Step 1: Wiring Connections

#### AD9850 DDS Module to Raspberry Pi:
```
AD9850    →    Raspberry Pi
VCC       →    3.3V (Pin 1)
GND       →    GND (Pin 6)
DATA      →    GPIO 23 (Pin 16)
W_CLK     →    GPIO 18 (Pin 12)
FQ_UD     →    GPIO 24 (Pin 18)
RESET     →    GPIO 25 (Pin 22)
```

#### AD8302 RF Detector to Raspberry Pi:
```
AD8302    →    Raspberry Pi
VPOS      →    5V (external power supply)
COMM      →    GND (Pin 6)
VMAG      →    MCP3008 CH0
VPHS      →    MCP3008 CH1
```

#### MCP3008 ADC to Raspberry Pi:
```
MCP3008   →    Raspberry Pi
VDD       →    3.3V (Pin 1)
VREF      →    3.3V (Pin 1)
AGND      →    GND (Pin 6)
DGND      →    GND (Pin 6)
CLK       →    SPI0 SCLK (Pin 23)
DOUT      →    SPI0 MISO (Pin 21)
DIN       →    SPI0 MOSI (Pin 19)
CS        →    SPI0 CE0 (Pin 24)

CH0       →    AD8302 VMAG
CH1       →    AD8302 VPHS
```

#### RF Signal Path:
```
AD9850 OUT → Directional Coupler INPUT
Directional Coupler FWD → AD8302 INPA
Directional Coupler REF → AD8302 INPB
Directional Coupler OUTPUT → Antenna Under Test
```

### Step 2: Software Setup

#### Install Required Packages:
```bash
sudo apt update
sudo apt install python3-pip python3-numpy python3-matplotlib
pip3 install RPi.GPIO spidev
```

#### Enable SPI:
```bash
sudo raspi-config
# Navigate to: Interfacing Options → SPI → Enable
sudo reboot
```

### Step 3: Assembly

1. **Mount components** on a breadboard or PCB
2. **Connect all wires** according to the wiring diagram above
3. **Add BNC connectors** for antenna connection
4. **Install in enclosure** (optional but recommended)

### Step 4: Calibration

1. **Short circuit calibration**: Connect a short to the antenna port
2. **Open circuit calibration**: Leave antenna port open
3. **50Ω load calibration**: Connect a known 50Ω load

### Step 5: Testing

1. Run the Python script
2. Connect a known good antenna
3. Perform frequency sweep
4. Verify SWR readings make sense

---

## What It Can Measure

- **SWR (Standing Wave Ratio)**
- **Impedance** (R + jX)
- **Return Loss**
- **Frequency sweeps** (1Hz - 40MHz)
- **Resonant frequency**

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

1. Connect the hardware components
2. Run the Python script
3. Test individual frequencies or perform sweeps
4. View SWR plots to analyze antenna performance

This simple setup provides basic antenna analysis capabilities at low cost.

# Simple Antenna Analyzer - Arduino Uno Version

## Hardware Setup

### Components Needed:

#### **Arduino Uno** (~$15)
- Main processing unit running the analyzer software
- 5V operation, 16MHz clock
- Built-in ADC for analog measurements

#### **AD9850 DDS Module** (~$15)
- Generates test signals from 1Hz to 40MHz
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4682284022-s27000512992.html)

#### **AD8302 RF Detector** (~$20)
- Measures signal phase and magnitude
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4931232200-s28732350592.html)

#### **Directional Coupler** (~$10)
- Separates forward and reflected signals
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4871092638-s28286101362.html)

#### **LCD Display (16x2)** (~$5)
- Shows SWR and frequency readings
- I2C interface for easy connection

#### **Battery Pack** (~$10)
- 18650 battery holder with USB output
- [Available on Lazada](https://www.lazada.com.ph/products/pdp-i4758996149-s27482027236.html)

**Total cost: ~$75**

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
VCC    - +5V Power
GND    - Ground
DATA   - Serial data input
W_CLK  - Word clock
FQ_UD  - Frequency update
RESET  - Reset (active high)
OUT    - RF signal output
OUTB   - Inverted RF output (not used)
```

### LCD Display (16x2 I2C):
```
LCD I2C Module:
VCC    - +5V Power
GND    - Ground
SDA    - I2C Data
SCL    - I2C Clock
```

### Arduino Uno Pinout (relevant pins):
```
Arduino Pin → Function
Pin 2       → W_CLK (AD9850)
Pin 3       → DATA (AD9850)
Pin 4       → FQ_UD (AD9850)
Pin 5       → RESET (AD9850)
Pin A0      → VMAG (AD8302)
Pin A1      → VPHS (AD8302)
Pin A4      → SDA (LCD I2C)
Pin A5      → SCL (LCD I2C)
Pin 5V      → Power supply
Pin GND     → Ground
```

---

## How to Build

### Step 1: Wiring Connections

#### AD9850 DDS Module to Arduino Uno:
```
AD9850    →    Arduino Uno
VCC       →    5V
GND       →    GND
DATA      →    Pin 3
W_CLK     →    Pin 2
FQ_UD     →    Pin 4
RESET     →    Pin 5
```

#### AD8302 RF Detector to Arduino Uno:
```
AD8302    →    Arduino Uno
VPOS      →    5V
COMM      →    GND
VMAG      →    A0 (Analog input)
VPHS      →    A1 (Analog input)
```

#### LCD Display to Arduino Uno:
```
LCD I2C   →    Arduino Uno
VCC       →    5V
GND       →    GND
SDA       →    A4 (I2C Data)
SCL       →    A5 (I2C Clock)
```

#### RF Signal Path:
```
AD9850 OUT → Directional Coupler INPUT
Directional Coupler FWD → AD8302 INPA
Directional Coupler REF → AD8302 INPB
Directional Coupler OUTPUT → Antenna Under Test
```

### Step 2: Software Setup

#### Install Required Libraries:
1. Open Arduino IDE
2. Go to Tools → Manage Libraries
3. Install these libraries:
   - **LiquidCrystal_I2C** by Frank de Brabander
   - **Wire** (built-in)

### Step 3: Assembly

1. **Mount components** on a breadboard
2. **Connect all wires** according to the wiring diagram above
3. **Add BNC connectors** for antenna connection
4. **Install in enclosure** (optional but recommended)

### Step 4: Calibration

1. **Short circuit calibration**: Connect a short to the antenna port
2. **Open circuit calibration**: Leave antenna port open
3. **50Ω load calibration**: Connect a known 50Ω load

### Step 5: Testing

1. Upload the Arduino sketch
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

## Arduino Code Example

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// AD9850 pins
#define W_CLK 2
#define FQ_UD 4
#define DATA 3
#define RESET 5

// AD8302 analog inputs
#define MAG_PIN A0
#define PHASE_PIN A1

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Calibration values
float mag_offset = 0.9;
float mag_scale = 0.03;

void setup() {
  Serial.begin(9600);
  
  // Setup AD9850 pins
  pinMode(W_CLK, OUTPUT);
  pinMode(FQ_UD, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(RESET, OUTPUT);
  
  // Initialize LCD
  Wire.begin();
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Antenna Analyzer");
  
  // Reset AD9850
  resetDDS();
  
  Serial.println("Antenna Analyzer Ready");
}

void loop() {
  // Main menu
  lcd.setCursor(0, 1);
  lcd.print("Press any key...");
  
  if (Serial.available()) {
    char cmd = Serial.read();
    
    switch(cmd) {
      case 's': // Single frequency measurement
        singleMeasurement();
        break;
      case 'w': // Frequency sweep
        frequencySweep();
        break;
      case 'c': // Calibration
        calibration();
        break;
    }
  }
}

void resetDDS() {
  digitalWrite(RESET, HIGH);
  delay(1);
  digitalWrite(RESET, LOW);
  delay(1);
  digitalWrite(RESET, HIGH);
}

void setFrequency(unsigned long freq) {
  // Calculate frequency word for AD9850
  unsigned long freqWord = (unsigned long)((double)freq * 4294967296.0 / 125000000.0);
  
  // Send frequency data (32 bits)
  for (int i = 31; i >= 0; i--) {
    digitalWrite(DATA, (freqWord >> i) & 1);
    digitalWrite(W_CLK, HIGH);
    digitalWrite(W_CLK, LOW);
  }
  
  // Send control byte (8 bits)
  for (int i = 7; i >= 0; i--) {
    digitalWrite(DATA, LOW);
    digitalWrite(W_CLK, HIGH);
    digitalWrite(W_CLK, LOW);
  }
  
  // Update frequency
  digitalWrite(FQ_UD, HIGH);
  digitalWrite(FQ_UD, LOW);
}

float readMagnitude() {
  int adcValue = analogRead(MAG_PIN);
  float voltage = (adcValue * 5.0) / 1024.0;
  return voltage;
}

float readPhase() {
  int adcValue = analogRead(PHASE_PIN);
  float voltage = (adcValue * 5.0) / 1024.0;
  return voltage;
}

float calculateSWR(float magVoltage) {
  // Convert voltage to dB
  float magDB = (magVoltage - mag_offset) / mag_scale;
  
  // Convert dB to reflection coefficient
  float reflectionCoeff = pow(10, magDB / 20.0);
  
  // Calculate SWR
  if (reflectionCoeff >= 1.0) {
    return 999.0;
  } else {
    return (1.0 + reflectionCoeff) / (1.0 - reflectionCoeff);
  }
}

void singleMeasurement() {
  Serial.println("Enter frequency in Hz:");
  while (!Serial.available()) {
    delay(10);
  }
  
  unsigned long freq = Serial.parseInt();
  setFrequency(freq);
  delay(10);
  
  float magVoltage = readMagnitude();
  float phaseVoltage = readPhase();
  float swr = calculateSWR(magVoltage);
  
  // Display on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(freq / 1000000.0, 2);
  lcd.print(" MHz");
  lcd.setCursor(0, 1);
  lcd.print("SWR: ");
  lcd.print(swr, 2);
  
  // Send to Serial
  Serial.print("Frequency: ");
  Serial.print(freq / 1000000.0, 2);
  Serial.println(" MHz");
  Serial.print("Magnitude: ");
  Serial.print(magVoltage, 3);
  Serial.println(" V");
  Serial.print("Phase: ");
  Serial.print(phaseVoltage, 3);
  Serial.println(" V");
  Serial.print("SWR: ");
  Serial.println(swr, 2);
}

void frequencySweep() {
  Serial.println("Enter start frequency (Hz):");
  while (!Serial.available()) {
    delay(10);
  }
  unsigned long startFreq = Serial.parseInt();
  
  Serial.println("Enter stop frequency (Hz):");
  while (!Serial.available()) {
    delay(10);
  }
  unsigned long stopFreq = Serial.parseInt();
  
  Serial.println("Enter number of points:");
  while (!Serial.available()) {
    delay(10);
  }
  int points = Serial.parseInt();
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sweeping...");
  
  Serial.println("Frequency(MHz),SWR");
  
  for (int i = 0; i < points; i++) {
    unsigned long freq = startFreq + ((stopFreq - startFreq) * i) / (points - 1);
    setFrequency(freq);
    delay(10);
    
    float swr = calculateSWR(readMagnitude());
    
    Serial.print(freq / 1000000.0, 2);
    Serial.print(",");
    Serial.println(swr, 2);
    
    // Update LCD progress
    lcd.setCursor(0, 1);
    lcd.print(i + 1);
    lcd.print("/");
    lcd.print(points);
  }
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sweep Complete");
}

void calibration() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Calibration Mode");
  
  Serial.println("Calibration Mode");
  Serial.println("1. Connect short circuit");
  Serial.println("2. Press 's' when ready");
  
  while (!Serial.available() || Serial.read() != 's') {
    delay(10);
  }
  
  // Short circuit calibration
  setFrequency(10000000); // 10 MHz
  delay(100);
  float shortMag = readMagnitude();
  
  Serial.println("Short circuit magnitude: ");
  Serial.println(shortMag, 3);
  
  Serial.println("3. Connect 50 ohm load");
  Serial.println("4. Press 'o' when ready");
  
  while (!Serial.available() || Serial.read() != 'o') {
    delay(10);
  }
  
  // 50 ohm load calibration
  float loadMag = readMagnitude();
  
  Serial.println("50 ohm load magnitude: ");
  Serial.println(loadMag, 3);
  
  // Calculate calibration values
  mag_offset = shortMag;
  mag_scale = (loadMag - shortMag) / 6.0; // 6dB difference for 50 ohm
  
  Serial.println("Calibration complete!");
  Serial.print("Offset: ");
  Serial.println(mag_offset, 3);
  Serial.print("Scale: ");
  Serial.println(mag_scale, 3);
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Cal Complete");
}
```

---

## Usage Instructions

### Serial Commands:
- **'s'** - Single frequency measurement
- **'w'** - Frequency sweep
- **'c'** - Calibration mode

### Example Usage:
1. **Upload the sketch** to Arduino Uno
2. **Open Serial Monitor** (9600 baud)
3. **Connect antenna** to the BNC connector
4. **Send commands** via Serial Monitor:
   - Type 's' for single measurement
   - Type 'w' for frequency sweep
   - Type 'c' for calibration

### Frequency Sweep Example:
```
Enter start frequency (Hz): 10000000
Enter stop frequency (Hz): 30000000
Enter number of points: 50
```

### Output Format:
- **LCD Display**: Shows current frequency and SWR
- **Serial Output**: CSV format for data logging
- **Real-time**: Updates as measurements are taken

---

## Advantages of Arduino Uno Version

1. **Lower Cost**: ~$75 vs ~$48 (but includes display)
2. **Simpler Setup**: No Linux configuration needed
3. **Built-in ADC**: No external ADC required
4. **Portable**: Can run on battery power
5. **Real-time Display**: LCD shows measurements immediately
6. **Easy Programming**: Arduino IDE is beginner-friendly

## Limitations

1. **Lower Processing Power**: Limited compared to Raspberry Pi
2. **Memory Constraints**: Can't store large datasets
3. **No Network**: No WiFi/Bluetooth connectivity
4. **Limited Storage**: No SD card for data logging

This Arduino version provides a more portable and simpler alternative to the Raspberry Pi version, perfect for field use and quick measurements. 
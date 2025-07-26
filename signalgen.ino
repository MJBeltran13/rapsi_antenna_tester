#define W_CLK 8
#define FQ_UD 9
#define DATA 11
#define RESET 10

// Start with 125 MHz — adjust if actual frequency doesn't match
double DDS_CLOCK = 125000000.0;

void pulse(int pin) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(pin, LOW);
  delayMicroseconds(1);
}

void sendFrequency(double frequency) {
  uint32_t freqWord = (uint32_t)((frequency * 4294967296.0) / DDS_CLOCK);

  Serial.print("Requested Frequency: ");
  Serial.print(frequency);
  Serial.print(" Hz -> Tuning Word: 0x");
  Serial.print(freqWord, HEX);
  Serial.println();

  for (int i = 0; i < 4; i++) {
    shiftOut(DATA, W_CLK, LSBFIRST, (freqWord >> (8 * i)) & 0xFF);
  }

  shiftOut(DATA, W_CLK, LSBFIRST, 0x00); // Control byte
  pulse(FQ_UD);
}

void setup() {
  pinMode(W_CLK, OUTPUT);
  pinMode(FQ_UD, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(RESET, OUTPUT);

  Serial.begin(9600);
  Serial.println("AD9850 Frequency Sweep Test Starting...");

  digitalWrite(W_CLK, LOW);
  digitalWrite(FQ_UD, LOW);
  digitalWrite(DATA, LOW);
  digitalWrite(RESET, LOW);
  delay(10);

  pulse(RESET);
  pulse(W_CLK);
  pulse(FQ_UD);
}

void loop() {
  // Frequencies to test
  double testFrequencies[] = {500, 1000, 2000, 5000, 10000};
  const int numFrequencies = sizeof(testFrequencies) / sizeof(testFrequencies[0]);

  for (int i = 0; i < numFrequencies; i++) {
    double freq = testFrequencies[i];
    sendFrequency(freq);

    Serial.println("Check frequency on multimeter now...");
    delay(5000); // Give you 5 seconds to measure each frequency
  }

  Serial.println("Sweep complete. Repeating...");
  delay(3000);
}

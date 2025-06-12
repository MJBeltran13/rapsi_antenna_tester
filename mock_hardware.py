#!/usr/bin/env python3
"""
Mock Hardware Module for Windows Development
Simulates RPi.GPIO and spidev for testing antenna analyzer GUI on Windows
"""

import time
import random
import numpy as np

class MockGPIO:
    """Mock Raspberry Pi GPIO for Windows testing"""
    
    # Constants
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0
    
    @staticmethod
    def setmode(mode):
        print(f"Mock GPIO: Set mode to {mode}")
    
    @staticmethod
    def setup(pins, direction):
        if isinstance(pins, list):
            print(f"Mock GPIO: Setup pins {pins} as {direction}")
        else:
            print(f"Mock GPIO: Setup pin {pins} as {direction}")
    
    @staticmethod
    def output(pins, state):
        if isinstance(pins, list):
            print(f"Mock GPIO: Set pins {pins} to {state}")
        else:
            print(f"Mock GPIO: Set pin {pins} to {state}")
    
    @staticmethod
    def cleanup():
        print("Mock GPIO: Cleanup completed")

class MockSpiDev:
    """Mock SPI device for Windows testing"""
    
    def __init__(self):
        self.max_speed_hz = 1000000
        self._open = False
    
    def open(self, bus, device):
        print(f"Mock SPI: Opened bus {bus}, device {device}")
        self._open = True
    
    def xfer2(self, data):
        """Simulate ADC readings with realistic values"""
        if not self._open:
            raise Exception("SPI not opened")
        
        # Simulate realistic ADC readings for antenna testing
        # Generate values that would represent decent antenna performance
        channel = (data[1] >> 4) - 8
        
        if channel == 0:  # Magnitude channel
            # Simulate magnitude reading (0.5V to 1.5V range)
            # Lower values = better SWR
            base_voltage = 0.8 + random.uniform(-0.2, 0.4)
            adc_value = int((base_voltage / 3.3) * 1024)
        elif channel == 1:  # Phase channel  
            # Simulate phase reading (0.5V to 2.5V range)
            base_voltage = 1.5 + random.uniform(-0.5, 0.5)
            adc_value = int((base_voltage / 3.3) * 1024)
        else:
            adc_value = 512  # Mid-scale for other channels
        
        # Add some noise
        adc_value += random.randint(-5, 5)
        adc_value = max(0, min(1023, adc_value))
        
        # Return simulated SPI response
        return [1, (adc_value >> 8) & 0x03, adc_value & 0xFF]
    
    def close(self):
        print("Mock SPI: Closed")
        self._open = False

# Create mock modules that can be imported
class MockRPiGPIO:
    GPIO = MockGPIO()

class MockSpiDevModule:
    SpiDev = MockSpiDev

# Make these available for import
RPi = MockRPiGPIO()
spidev = MockSpiDevModule()

if __name__ == "__main__":
    # Test the mock hardware
    print("Testing Mock Hardware...")
    
    # Test GPIO
    gpio = MockGPIO()
    gpio.setmode(gpio.BCM)
    gpio.setup([18, 23, 24, 25], gpio.OUT)
    gpio.output([18, 23, 24], gpio.LOW)
    gpio.output(25, gpio.HIGH)
    
    # Test SPI
    spi = MockSpiDev()
    spi.open(0, 0)
    
    # Test ADC reading
    for channel in range(2):
        result = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_value = ((result[1] & 3) << 8) + result[2]
        voltage = (adc_value * 3.3) / 1024.0
        print(f"Channel {channel}: ADC={adc_value}, Voltage={voltage:.3f}V")
    
    spi.close()
    gpio.cleanup()
    
    print("Mock hardware test completed!") 
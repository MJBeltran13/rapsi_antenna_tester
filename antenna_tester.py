#!/usr/bin/env python3
"""
Raspberry Pi Antenna Analyzer - One-Click Sweep & Rating System
Designed for AD9850 DDS + AD8302 RF Detector + MCP3008 ADC
"""

import RPi.GPIO as GPIO
import spidev
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class AntennaAnalyzer:
    def __init__(self):
        # Hardware configuration
        self.W_CLK = 18
        self.FQ_UD = 24
        self.DATA = 23
        self.RESET = 25
        
        # Measurement parameters
        self.ref_voltage = 3.3
        self.adc_resolution = 1024
        
        # Initialize hardware
        self.spi = None
        self.hardware_ready = False
        
        # Calibration data
        self.cal_data = {
            'short': {'mag': 0, 'phase': 0},
            'open': {'mag': 0, 'phase': 0},
            'load': {'mag': 0, 'phase': 0}
        }
        
        self.setup_hardware()
    
    def setup_hardware(self):
        """Initialize GPIO and SPI"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup([self.W_CLK, self.FQ_UD, self.DATA, self.RESET], GPIO.OUT)
            GPIO.output([self.W_CLK, self.FQ_UD, self.DATA], GPIO.LOW)
            GPIO.output(self.RESET, GPIO.HIGH)
            
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000
            
            self.reset_dds()
            self.hardware_ready = True
            print("Hardware initialized successfully")
            
        except Exception as e:
            print(f"Hardware initialization failed: {e}")
            self.hardware_ready = False
    
    def reset_dds(self):
        """Reset AD9850 DDS module"""
        GPIO.output(self.RESET, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.RESET, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.RESET, GPIO.HIGH)
    
    def set_frequency(self, freq_hz):
        """Set DDS frequency"""
        if not self.hardware_ready:
            return False
            
        # Calculate 32-bit frequency word
        freq_word = int((freq_hz * 4294967296.0) / 125000000.0)
        
        # Send frequency data (32 bits)
        for i in range(32):
            GPIO.output(self.DATA, (freq_word >> (31-i)) & 1)
            GPIO.output(self.W_CLK, GPIO.HIGH)
            GPIO.output(self.W_CLK, GPIO.LOW)
        
        # Send control byte (8 bits, all zeros for normal operation)
        for i in range(8):
            GPIO.output(self.DATA, GPIO.LOW)
            GPIO.output(self.W_CLK, GPIO.HIGH)
            GPIO.output(self.W_CLK, GPIO.LOW)
        
        # Update frequency
        GPIO.output(self.FQ_UD, GPIO.HIGH)
        GPIO.output(self.FQ_UD, GPIO.LOW)
        return True
    
    def read_adc(self, channel):
        """Read voltage from MCP3008 ADC channel"""
        if not self.hardware_ready:
            return 0
            
        try:
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            data = ((adc[1] & 3) << 8) + adc[2]
            voltage = (data * self.ref_voltage) / self.adc_resolution
            return voltage
        except:
            return 0
    
    def read_detector(self):
        """Read magnitude and phase from AD8302"""
        mag_voltage = self.read_adc(0)  # Magnitude on channel 0
        phase_voltage = self.read_adc(1)  # Phase on channel 1
        return mag_voltage, phase_voltage
    
    def calculate_swr(self, mag_voltage):
        """Calculate SWR from magnitude voltage"""
        # AD8302 outputs 30mV/dB with 900mV intercept
        # Convert voltage to dB
        mag_db = (mag_voltage - 0.9) / 0.03
        
        # Convert dB to linear reflection coefficient
        reflection_coeff = 10 ** (mag_db / 20.0)
        
        # Clamp reflection coefficient
        reflection_coeff = min(reflection_coeff, 0.99)
        
        # Calculate SWR
        if reflection_coeff >= 1.0:
            return 999  # Infinite SWR
        else:
            swr = (1 + reflection_coeff) / (1 - reflection_coeff)
            return min(swr, 50)  # Cap at reasonable value
    
    def measure_point(self, freq_hz):
        """Measure single frequency point"""
        if not self.set_frequency(freq_hz):
            return None
            
        time.sleep(0.01)  # Settling time
        mag_voltage, phase_voltage = self.read_detector()
        swr = self.calculate_swr(mag_voltage)
        
        return {
            'frequency': freq_hz,
            'swr': swr,
            'mag_voltage': mag_voltage,
            'phase_voltage': phase_voltage
        }
    
    def frequency_sweep(self, start_freq, stop_freq, points=100, progress_callback=None):
        """Perform frequency sweep"""
        frequencies = np.linspace(start_freq, stop_freq, points)
        measurements = []
        
        for i, freq in enumerate(frequencies):
            measurement = self.measure_point(freq)
            if measurement:
                measurements.append(measurement)
            
            if progress_callback:
                progress_callback(i + 1, points)
        
        return measurements
    
    def rate_antenna_performance(self, measurements):
        """Rate antenna performance based on measurements"""
        if not measurements:
            return {"rating": "F", "score": 0, "analysis": "No measurements available"}
        
        swr_values = [m['swr'] for m in measurements]
        min_swr = min(swr_values)
        avg_swr = np.mean(swr_values)
        max_swr = max(swr_values)
        
        # Count points with good SWR
        excellent_points = sum(1 for swr in swr_values if swr <= 1.5)
        good_points = sum(1 for swr in swr_values if swr <= 2.0)
        acceptable_points = sum(1 for swr in swr_values if swr <= 3.0)
        
        total_points = len(swr_values)
        excellent_ratio = excellent_points / total_points
        good_ratio = good_points / total_points
        acceptable_ratio = acceptable_points / total_points
        
        # Calculate score (0-100)
        score = 0
        if excellent_ratio >= 0.8:
            score = 90 + (excellent_ratio - 0.8) * 50
        elif good_ratio >= 0.6:
            score = 70 + (good_ratio - 0.6) * 50
        elif acceptable_ratio >= 0.4:
            score = 50 + (acceptable_ratio - 0.4) * 50
        else:
            score = acceptable_ratio * 125
        
        # Adjust for minimum SWR
        if min_swr <= 1.2:
            score += 5
        elif min_swr <= 1.5:
            score += 2
        
        # Adjust for bandwidth
        if good_ratio >= 0.7:
            score += 3
        
        score = min(100, max(0, score))
        
        # Assign letter grade
        if score >= 90:
            rating = "A+"
        elif score >= 85:
            rating = "A"
        elif score >= 80:
            rating = "A-"
        elif score >= 75:
            rating = "B+"
        elif score >= 70:
            rating = "B"
        elif score >= 65:
            rating = "B-"
        elif score >= 60:
            rating = "C+"
        elif score >= 55:
            rating = "C"
        elif score >= 50:
            rating = "C-"
        elif score >= 40:
            rating = "D"
        else:
            rating = "F"
        
        # Generate analysis
        analysis = []
        analysis.append(f"Minimum SWR: {min_swr:.2f}")
        analysis.append(f"Average SWR: {avg_swr:.2f}")
        analysis.append(f"Maximum SWR: {max_swr:.2f}")
        analysis.append(f"Points with SWR ≤ 1.5: {excellent_points}/{total_points} ({excellent_ratio:.1%})")
        analysis.append(f"Points with SWR ≤ 2.0: {good_points}/{total_points} ({good_ratio:.1%})")
        analysis.append(f"Points with SWR ≤ 3.0: {acceptable_points}/{total_points} ({acceptable_ratio:.1%})")
        
        if min_swr <= 1.5:
            analysis.append("✓ Excellent resonance achieved")
        elif min_swr <= 2.0:
            analysis.append("✓ Good resonance achieved")
        else:
            analysis.append("⚠ Poor resonance - consider adjustment")
        
        if good_ratio >= 0.7:
            analysis.append("✓ Good bandwidth coverage")
        elif good_ratio >= 0.5:
            analysis.append("⚠ Moderate bandwidth coverage")
        else:
            analysis.append("⚠ Poor bandwidth coverage")
        
        return {
            "rating": rating,
            "score": score,
            "analysis": "\n".join(analysis),
            "stats": {
                "min_swr": min_swr,
                "avg_swr": avg_swr,
                "max_swr": max_swr,
                "excellent_ratio": excellent_ratio,
                "good_ratio": good_ratio,
                "acceptable_ratio": acceptable_ratio
            }
        }
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if self.hardware_ready:
            GPIO.cleanup()


class AntennaAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Antenna Analyzer")
        self.root.geometry("1200x800")
        
        self.analyzer = AntennaAnalyzer()
        self.measurements = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Test Parameters", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Frequency settings
        ttk.Label(control_frame, text="Start Frequency (MHz):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.start_freq_var = tk.StringVar(value="1.0")
        ttk.Entry(control_frame, textvariable=self.start_freq_var, width=10).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(control_frame, text="Stop Frequency (MHz):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.stop_freq_var = tk.StringVar(value="30.0")
        ttk.Entry(control_frame, textvariable=self.stop_freq_var, width=10).grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(control_frame, text="Points:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.points_var = tk.StringVar(value="100")
        ttk.Entry(control_frame, textvariable=self.points_var, width=10).grid(row=0, column=5, padx=(0, 20))
        
        # One-click sweep button
        self.sweep_button = ttk.Button(control_frame, text="🚀 ONE-CLICK SWEEP & RATE", 
                                     command=self.one_click_sweep, style="Accent.TButton")
        self.sweep_button.grid(row=1, column=0, columnspan=6, pady=10, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=2, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to test")
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=0, columnspan=6, pady=(5, 0))
        
        # Results panel
        results_frame = ttk.LabelFrame(main_frame, text="Test Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        results_frame.rowconfigure(1, weight=1)
        
        # Rating display
        self.rating_var = tk.StringVar(value="--")
        self.score_var = tk.StringVar(value="--")
        
        rating_frame = ttk.Frame(results_frame)
        rating_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(rating_frame, text="Rating:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.rating_label = ttk.Label(rating_frame, textvariable=self.rating_var, 
                                    font=("Arial", 24, "bold"), foreground="green")
        self.rating_label.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(rating_frame, text="Score:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.score_label = ttk.Label(rating_frame, textvariable=self.score_var, 
                                   font=("Arial", 14, "bold"), foreground="blue")
        self.score_label.grid(row=0, column=3, padx=(10, 0))
        
        # Analysis text
        self.analysis_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
        analysis_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=analysis_scroll.set)
        
        self.analysis_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        analysis_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Plot panel
        plot_frame = ttk.LabelFrame(main_frame, text="SWR Plot", padding="10")
        plot_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('SWR')
        self.ax.set_title('Antenna SWR vs Frequency')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(1, 10)
        
        # Embed plot in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Additional buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Results", command=self.save_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Exit", command=self.on_closing).pack(side=tk.RIGHT)
    
    def update_progress(self, current, total):
        """Update progress bar"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.status_var.set(f"Measuring point {current}/{total}")
        self.root.update_idletasks()
    
    def one_click_sweep(self):
        """Perform complete sweep and rating with one click"""
        try:
            # Get parameters
            start_freq = float(self.start_freq_var.get()) * 1e6  # Convert MHz to Hz
            stop_freq = float(self.stop_freq_var.get()) * 1e6
            points = int(self.points_var.get())
            
            # Validate parameters
            if start_freq >= stop_freq:
                messagebox.showerror("Error", "Start frequency must be less than stop frequency")
                return
            
            if points < 10 or points > 1000:
                messagebox.showerror("Error", "Points must be between 10 and 1000")
                return
            
            # Check hardware
            if not self.analyzer.hardware_ready:
                messagebox.showerror("Error", "Hardware not ready. Check connections.")
                return
            
            # Disable button during sweep
            self.sweep_button.config(state='disabled')
            self.progress_var.set(0)
            self.status_var.set("Starting sweep...")
            
            # Perform sweep
            start_time = time.time()
            self.measurements = self.analyzer.frequency_sweep(
                start_freq, stop_freq, points, self.update_progress
            )
            sweep_time = time.time() - start_time
            
            # Rate the antenna
            self.status_var.set("Analyzing results...")
            rating_result = self.analyzer.rate_antenna_performance(self.measurements)
            
            # Update display
            self.update_results_display(rating_result, sweep_time)
            self.plot_results()
            
            self.status_var.set(f"Sweep completed in {sweep_time:.1f}s - Rating: {rating_result['rating']}")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Sweep failed: {e}")
        finally:
            self.sweep_button.config(state='normal')
            self.progress_var.set(0)
    
    def update_results_display(self, rating_result, sweep_time):
        """Update the results display"""
        # Update rating and score
        self.rating_var.set(rating_result['rating'])
        self.score_var.set(f"{rating_result['score']:.0f}/100")
        
        # Set rating color
        if rating_result['score'] >= 80:
            color = "green"
        elif rating_result['score'] >= 60:
            color = "orange"
        else:
            color = "red"
        self.rating_label.config(foreground=color)
        
        # Update analysis text
        self.analysis_text.delete(1.0, tk.END)
        
        analysis_text = f"ANTENNA PERFORMANCE ANALYSIS\n"
        analysis_text += f"={'='*50}\n\n"
        analysis_text += f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        analysis_text += f"Sweep time: {sweep_time:.1f} seconds\n"
        analysis_text += f"Frequency range: {float(self.start_freq_var.get()):.1f} - {float(self.stop_freq_var.get()):.1f} MHz\n"
        analysis_text += f"Measurement points: {len(self.measurements)}\n\n"
        
        analysis_text += f"OVERALL RATING: {rating_result['rating']} ({rating_result['score']:.0f}/100)\n\n"
        
        analysis_text += "DETAILED ANALYSIS:\n"
        analysis_text += f"{'-'*30}\n"
        analysis_text += rating_result['analysis'] + "\n\n"
        
        # Add recommendations
        score = rating_result['score']
        stats = rating_result['stats']
        
        analysis_text += "RECOMMENDATIONS:\n"
        analysis_text += f"{'-'*30}\n"
        
        if score >= 85:
            analysis_text += "✅ Excellent antenna performance! No adjustments needed.\n"
        elif score >= 70:
            analysis_text += "✅ Good antenna performance. Minor tuning could improve bandwidth.\n"
        elif score >= 50:
            analysis_text += "⚠️ Acceptable performance. Consider adjusting antenna length or matching network.\n"
        else:
            analysis_text += "❌ Poor performance. Antenna requires significant adjustment or redesign.\n"
        
        if stats['min_swr'] > 2.0:
            analysis_text += "• Check antenna resonance - may need length adjustment\n"
        
        if stats['good_ratio'] < 0.5:
            analysis_text += "• Consider adding matching network to improve bandwidth\n"
        
        if stats['avg_swr'] > 3.0:
            analysis_text += "• Check all connections and ensure proper grounding\n"
        
        self.analysis_text.insert(1.0, analysis_text)
    
    def plot_results(self):
        """Plot the measurement results"""
        if not self.measurements:
            return
        
        frequencies = [m['frequency'] / 1e6 for m in self.measurements]  # Convert to MHz
        swr_values = [m['swr'] for m in self.measurements]
        
        self.ax.clear()
        self.ax.plot(frequencies, swr_values, 'b-', linewidth=2, label='SWR')
        
        # Add SWR reference lines
        self.ax.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='SWR 1.5 (Excellent)')
        self.ax.axhline(y=2.0, color='orange', linestyle='--', alpha=0.7, label='SWR 2.0 (Good)')
        self.ax.axhline(y=3.0, color='red', linestyle='--', alpha=0.7, label='SWR 3.0 (Acceptable)')
        
        # Highlight minimum SWR point
        min_swr_idx = np.argmin(swr_values)
        self.ax.plot(frequencies[min_swr_idx], swr_values[min_swr_idx], 
                    'ro', markersize=8, label=f'Min SWR: {swr_values[min_swr_idx]:.2f}')
        
        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('SWR')
        self.ax.set_title('Antenna SWR vs Frequency')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.ax.set_ylim(1, min(max(swr_values) * 1.1, 10))
        
        self.canvas.draw()
    
    def save_results(self):
        """Save measurement results to file"""
        if not self.measurements:
            messagebox.showwarning("Warning", "No measurements to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"antenna_test_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'start_freq_mhz': float(self.start_freq_var.get()),
                'stop_freq_mhz': float(self.stop_freq_var.get()),
                'points': int(self.points_var.get())
            },
            'measurements': self.measurements,
            'rating': self.analyzer.rate_antenna_performance(self.measurements)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", f"Results saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")
    
    def clear_results(self):
        """Clear all results"""
        self.measurements = []
        self.rating_var.set("--")
        self.score_var.set("--")
        self.analysis_text.delete(1.0, tk.END)
        self.ax.clear()
        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('SWR')
        self.ax.set_title('Antenna SWR vs Frequency')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(1, 10)
        self.canvas.draw()
        self.status_var.set("Ready to test")
    
    def on_closing(self):
        """Handle application closing"""
        self.analyzer.cleanup()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AntennaAnalyzerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main() 
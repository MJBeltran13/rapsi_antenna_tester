#!/usr/bin/env python3
"""
Quick Antenna Test - Command Line Version
Simple one-click sweep for testing antennas
"""

import time
from antenna_tester import AntennaAnalyzer

def quick_sweep_and_rate():
    """Perform a quick frequency sweep and rate the antenna"""
    print("=" * 60)
    print("RASPBERRY PI ANTENNA ANALYZER - QUICK TEST")
    print("=" * 60)
    
    # Initialize analyzer
    print("Initializing hardware...")
    analyzer = AntennaAnalyzer()
    
    if not analyzer.hardware_ready:
        print("❌ Hardware not ready! Check connections:")
        print("   - AD9850 DDS module")
        print("   - AD8302 RF detector")
        print("   - MCP3008 ADC")
        print("   - Directional coupler")
        return
    
    print("✅ Hardware ready!")
    
    # Test parameters
    start_freq = 1.0e6    # 1 MHz
    stop_freq = 30.0e6    # 30 MHz
    points = 50           # 50 measurement points
    
    print(f"\nTest Parameters:")
    print(f"   Frequency range: {start_freq/1e6:.1f} - {stop_freq/1e6:.1f} MHz")
    print(f"   Measurement points: {points}")
    
    # Perform sweep
    print("\n🚀 Starting frequency sweep...")
    start_time = time.time()
    
    def progress_callback(current, total):
        percent = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rProgress: |{bar}| {percent:.1f}% ({current}/{total})', end='', flush=True)
    
    measurements = analyzer.frequency_sweep(start_freq, stop_freq, points, progress_callback)
    sweep_time = time.time() - start_time
    
    print(f"\n✅ Sweep completed in {sweep_time:.1f} seconds")
    
    # Rate the antenna
    print("\n📊 Analyzing antenna performance...")
    rating_result = analyzer.rate_antenna_performance(measurements)
    
    # Display results
    print("\n" + "=" * 60)
    print("ANTENNA PERFORMANCE RESULTS")
    print("=" * 60)
    
    # Display rating with color coding
    rating = rating_result['rating']
    score = rating_result['score']
    
    if score >= 80:
        status_icon = "🟢"
    elif score >= 60:
        status_icon = "🟡"
    else:
        status_icon = "🔴"
    
    print(f"\n{status_icon} OVERALL RATING: {rating} ({score:.0f}/100)")
    
    # Display detailed analysis
    print(f"\nDETAILED ANALYSIS:")
    print("-" * 30)
    print(rating_result['analysis'])
    
    # Display recommendations
    stats = rating_result['stats']
    print(f"\nRECOMMENDATIONS:")
    print("-" * 30)
    
    if score >= 85:
        print("✅ Excellent antenna performance! No adjustments needed.")
    elif score >= 70:
        print("✅ Good antenna performance. Minor tuning could improve bandwidth.")
    elif score >= 50:
        print("⚠️ Acceptable performance. Consider adjusting antenna length or matching network.")
    else:
        print("❌ Poor performance. Antenna requires significant adjustment or redesign.")
    
    if stats['min_swr'] > 2.0:
        print("• Check antenna resonance - may need length adjustment")
    
    if stats['good_ratio'] < 0.5:
        print("• Consider adding matching network to improve bandwidth")
    
    if stats['avg_swr'] > 3.0:
        print("• Check all connections and ensure proper grounding")
    
    # Display key frequencies
    swr_values = [m['swr'] for m in measurements]
    frequencies = [m['frequency'] for m in measurements]
    min_swr_idx = swr_values.index(min(swr_values))
    resonant_freq = frequencies[min_swr_idx]
    
    print(f"\nKEY FREQUENCIES:")
    print("-" * 30)
    print(f"   Resonant frequency: {resonant_freq/1e6:.2f} MHz")
    print(f"   Minimum SWR: {min(swr_values):.2f}")
    
    # Find usable bandwidth (SWR < 2.0)
    usable_freqs = [frequencies[i]/1e6 for i, swr in enumerate(swr_values) if swr <= 2.0]
    if usable_freqs:
        bandwidth = max(usable_freqs) - min(usable_freqs)
        print(f"   Usable bandwidth (SWR≤2.0): {bandwidth:.2f} MHz")
        print(f"   Usable range: {min(usable_freqs):.2f} - {max(usable_freqs):.2f} MHz")
    else:
        print("   Usable bandwidth: None (no frequencies with SWR≤2.0)")
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"quick_test_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("ANTENNA QUICK TEST RESULTS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Sweep Time: {sweep_time:.1f} seconds\n")
            f.write(f"Frequency Range: {start_freq/1e6:.1f} - {stop_freq/1e6:.1f} MHz\n")
            f.write(f"Points: {points}\n\n")
            f.write(f"RATING: {rating} ({score:.0f}/100)\n\n")
            f.write("ANALYSIS:\n")
            f.write(rating_result['analysis'] + "\n\n")
            f.write("MEASUREMENTS:\n")
            f.write("Frequency(MHz), SWR, Mag(V), Phase(V)\n")
            for m in measurements:
                f.write(f"{m['frequency']/1e6:.2f}, {m['swr']:.2f}, {m['mag_voltage']:.3f}, {m['phase_voltage']:.3f}\n")
        
        print(f"\n💾 Results saved to: {filename}")
        
    except Exception as e:
        print(f"\n⚠️ Could not save results: {e}")
    
    # Cleanup
    analyzer.cleanup()
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    quick_sweep_and_rate() 
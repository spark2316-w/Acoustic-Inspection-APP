import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa
import matplotlib.pyplot as plt

THRESHOLD_FREQ = 376  
MAX_ALLOWED_AMPLITUDE = 100

def analyze_fft(file_path):
    y, sr = librosa.load(file_path, sr=44100)
    ###Normalize
    y = y / np.max(np.abs(y))  
    ####

    ###FFT Kernel
    N = len(y)
    window = np.hamming(N)
    y_windowed = y * window

    Y = np.fft.fft(y_windowed)
    frequencies = np.fft.fftfreq(N, d=1/sr)

    half = N // 2
    magnitudes = np.abs(Y[:half])
    frequencies = frequencies[:half]

    peak_idx = np.argmax(magnitudes)
    peak_freq = frequencies[peak_idx]
    peak_amp = magnitudes[peak_idx]

    print(f"\n Peak Frequency: {peak_freq:.2f} Hz")
    print(f"Peak Amplitude: {peak_amp:.2f}")

    if peak_amp > MAX_ALLOWED_AMPLITUDE:
        print("⚠️ เสียงดังเกินไป ไม่สามารถวิเคราะห์ได้")
    elif not (376 <= peak_freq <= 401):
        print("🟥 วัสดุเสีย")
    else:
        print("✅ วัสดุดี")

    plt.figure(figsize=(10, 4))
    plt.plot(frequencies, magnitudes)
    plt.axvspan(376,401, color='yellow', alpha=0.3, label='วัสดุดี (8600–8800 Hz)')
    plt.title(f"FFT Spectrum (Peak = {peak_freq:.2f} Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


    # plt.figure(figsize=(12, 5))
    # plt.plot(frequencies, magnitudes, label='FFT Spectrum')
    # plt.axvline(peak_freq, color='r', linestyle='--', label=f'Peak: {peak_freq:.2f} Hz')
    # plt.title("Frequency Spectrum from FFT")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Magnitude")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(10, 3))
    # plt.plot(y_windowed, color='blue')
    # plt.title("Time-Domain Signal (with Hamming Window)")
    # plt.xlabel("Sample Index")
    # plt.ylabel("Amplitude")
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

def record_realtime_and_analyze(duration=5, output_path="realtime.wav"):
    print("กำลังอัดเสียง...")
    sr = 44100
    audio = sd.rec(int(sr * duration), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    sf.write(output_path, audio, sr)
    print("เสร็จสิ้นการอัดเสียง")
    analyze_fft(output_path)

record_realtime_and_analyze()




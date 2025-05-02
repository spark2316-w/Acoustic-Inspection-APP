import numpy as np
import sounddevice as sd
from scipy.signal import correlate
from pydub import AudioSegment
import matplotlib.pyplot as plt

def audio_to_normalized_numpy(audio_file):
    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio = audio.set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples -= np.mean(samples)
    samples /= np.std(samples) + 1e-9
    return samples

def record_audio(duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording finished.")
    return audio.flatten()

def compare_live_audio_to_reference(reference_file):
    ref_signal = audio_to_normalized_numpy(reference_file)

    # บันทึกเสียง
    live_signal = record_audio()
    live_signal -= np.mean(live_signal)
    live_signal /= np.std(live_signal) + 1e-9

    # Cross-correlation
    cross_corr = correlate(ref_signal, live_signal, mode='full', method='auto')
    max_corr = np.max(cross_corr) / len(ref_signal)

    lags = np.arange(-len(live_signal) + 1, len(ref_signal))
    
    # === Plot ทั้ง 3 ===
    plt.figure(figsize=(14, 10))

    # Plot Reference Signal
    plt.subplot(3, 1, 1)
    plt.plot(ref_signal, color='b')
    plt.title("Reference Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")

    # Plot Live Signal
    plt.subplot(3, 1, 2)
    plt.plot(live_signal, color='r')
    plt.title("Live Recorded Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")

    # Plot Cross-Correlation
    plt.subplot(3, 1, 3)
    plt.plot(lags, cross_corr, color='g')
    plt.title("Cross-Correlation between Reference and Live Signal")
    plt.xlabel("Lag")
    plt.ylabel("Correlation")

    plt.tight_layout()
    plt.grid(True)
    plt.show()

    # Print result
    if max_corr > 0.03:
        print(f"Max Corr: {max_corr:.5f} => Very Similar")
    elif max_corr > 0.02:
        print(f"Max Corr: {max_corr:.5f} => Moderately Similar")
    else:
        print(f"Max Corr: {max_corr:.5f} => Not Similar")

# ใช้งาน
reference_file = r"C:\Users\User\Desktop\Project\TestGG\Recording (109).m4a"
compare_live_audio_to_reference(reference_file)

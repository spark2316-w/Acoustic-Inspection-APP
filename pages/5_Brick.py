import streamlit as st
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
import io

THRESHOLD_FREQ = 376  
MAX_ALLOWED_AMPLITUDE = 100

def analyze_fft(y, sr):
    y = y / np.max(np.abs(y))  # Normalize

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

    st.write(f"\n🎯 **Peak Frequency:** {peak_freq:.2f} Hz")
    st.write(f"📈 **Peak Amplitude:** {peak_amp:.2f}")

    if peak_amp > MAX_ALLOWED_AMPLITUDE:
        st.error("⚠️ เสียงดังเกินไป ไม่สามารถวิเคราะห์ได้")
    elif not (376 <= peak_freq <= 401):
        st.warning("🟥 วัสดุเสีย")
    else:
        st.success("✅ วัสดุดี")

    plt.figure(figsize=(10, 4))
    plt.plot(frequencies, magnitudes)
    plt.axvspan(376, 401, color='yellow', alpha=0.3, label='วัสดุดี (8600–8800 Hz)')
    plt.title(f"FFT Spectrum (Peak = {peak_freq:.2f} Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    st.pyplot(plt)

# 👇 ส่วน UI
st.title("🎙️ วิเคราะห์วัสดุด้วยเสียง")

st.subheader("📤 วิธีเลือกเสียง:")
mode = st.radio("เลือกรูปแบบเสียงที่ต้องการวิเคราะห์", ["🎧 อัดเสียงใหม่", "📁 อัปโหลดไฟล์ (.wav, .mp3, .m4a)"])

audio_data = None
sr = 44100

if mode == "🎧 อัดเสียงใหม่":
    audio_bytes = st.audio_input("กดปุ่มเพื่ออัดเสียง")
    if audio_bytes:
        with st.spinner("อ่านไฟล์..."):
            audio_buffer = io.BytesIO(audio_bytes.getvalue())
            y, sr = sf.read(audio_buffer)
            if y.ndim > 1:
                y = y[:, 0]  # mono
            audio_data = y

elif mode == "📁 อัปโหลดไฟล์ (.wav)":
    uploaded_file = st.file_uploader("ลากไฟล์มาวาง หรือเลือกไฟล์เสียง", type=["wav"])
    if uploaded_file:
        with st.spinner("กำลังโหลดไฟล์..."):
            y, sr = librosa.load(uploaded_file, sr=44100)
            audio_data = y

# ✅ วิเคราะห์ถ้ามีข้อมูลเสียง
if audio_data is not None:
    st.success("✅ โหลดเสียงเรียบร้อย กำลังวิเคราะห์...")
    analyze_fft(audio_data, sr)

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import correlate
from io import BytesIO
import tempfile

# ==== ฟังก์ชันแปลงไฟล์ .wav เป็น normalized numpy ====
def audio_to_normalized_numpy(wav_path_or_bytes):
    sample_rate, samples = wavfile.read(wav_path_or_bytes)
    if samples.ndim > 1:
        samples = samples[:, 0]  # ถ้าเป็น stereo เอาแค่ channel แรก
    samples = samples.astype(np.float32)
    samples -= np.mean(samples)
    samples /= np.std(samples) + 1e-9
    return samples

# ==== UI ตั้งค่า ====
st.set_page_config(page_title="🎙️ Real-time Audio Comparison", layout="wide")
st.title("🎙️ เปรียบเทียบเสียง Real-Time กับ Reference WAV")

st.markdown("อัปโหลดไฟล์ **อ้างอิง (.wav)** จากนั้น **บันทึกเสียงจริงผ่านไมโครโฟน** เพื่อเปรียบเทียบความคล้ายคลึง")

# ==== Upload Reference File ====
reference_file = st.file_uploader("📌 อัปโหลด Reference .wav", type=["wav"], key="ref_upload")

# ==== Audio Input ====
recorded_audio = st.audio_input("🎤 บันทึกเสียงผ่านไมโครโฟน (Test Audio)", type="wav")

# ==== เมื่อตรวจสอบว่าพร้อม ====
if reference_file and recorded_audio:
    st.success("✅ เริ่มประมวลผล")

    # แปลงไฟล์อ้างอิง
    ref_signal = audio_to_normalized_numpy(reference_file)

    # แปลงไฟล์เสียงที่อัดผ่านไมค์ (ต้องบันทึกเป็น temp file ก่อน)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(recorded_audio.read())
        tmp_path = tmpfile.name

    test_signal = audio_to_normalized_numpy(tmp_path)

    # ==== พล็อตสัญญาณ ====
    st.subheader("🔊 สัญญาณเสียง")
    fig, axs = plt.subplots(2, 1, figsize=(12, 6))
    axs[0].plot(ref_signal, color="blue")
    axs[0].set_title("Reference Signal")
    axs[1].plot(test_signal, color="red")
    axs[1].set_title("Recorded Test Signal")
    st.pyplot(fig)

    # ==== คำนวณ Cross-Correlation ====
    cross_corr = correlate(ref_signal, test_signal, mode='full', method='auto')
    max_corr = np.max(cross_corr) / len(ref_signal)
    lags = np.arange(-(len(test_signal) - 1), len(ref_signal))

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(lags, cross_corr)
    ax2.set_title("Cross-Correlation")
    ax2.set_xlabel("Lag")
    ax2.set_ylabel("Correlation")
    ax2.grid(True)
    st.pyplot(fig2)

    # ==== วิเคราะห์ความคล้ายคลึง ====
    if max_corr > 0.3:
        similarity = "✅ Very Similar"
    elif max_corr > 0.2:
        similarity = "⚠️ Moderately Similar"
    else:
        similarity = "❌ Not Similar"

    st.markdown(f"### 🔍 ผลลัพธ์: **{similarity}** (Max Corr = `{max_corr:.5f}`)")

import streamlit as st
import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="🎤 Real-time Audio Comparison", layout="wide")
st.title("🎤 เปรียบเทียบเสียงแบบ Real-time ด้วย Cross-Correlation")

# อัปโหลดไฟล์ reference
reference_file = st.file_uploader("📌 อัปโหลด Reference .wav", type=["wav"])

# บันทึกเสียงทดสอบผ่านไมโครโฟน
audio_data = st.audio_input("🎙️ บันทึกเสียงทดสอบ (Test Audio)")

def audio_to_normalized_numpy(file):
    sr, samples = wavfile.read(file)
    if samples.ndim > 1:
        samples = samples[:, 0]
    samples = samples.astype(np.float32)
    samples -= np.mean(samples)
    samples /= np.std(samples) + 1e-9
    return samples

if reference_file and audio_data:
    ref_signal = audio_to_normalized_numpy(reference_file)
    test_signal = audio_to_normalized_numpy(audio_data)

    st.success("✅ ได้รับไฟล์ทั้งสองแล้ว เริ่มวิเคราะห์...")

    # แสดงสัญญาณ
    fig, axs = plt.subplots(2, 1, figsize=(12, 6))
    axs[0].plot(ref_signal, color='blue')
    axs[0].set_title("Reference Signal")
    axs[1].plot(test_signal, color='red')
    axs[1].set_title("Test Signal")
    st.pyplot(fig)

    # Cross-correlation
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

    # ความคล้ายคลึง
    if max_corr > 0.3:
        similarity = "✅ Very Similar"
    elif max_corr > 0.2:
        similarity = "⚠️ Moderately Similar"
    else:
        similarity = "❌ Not Similar"

    df = pd.DataFrame([{
        "Max Correlation": round(max_corr, 5),
        "Similarity": similarity
    }])
    st.subheader("📊 ผลการวิเคราะห์")
    st.dataframe(df)

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import correlate
from io import BytesIO

# ==== ฟังก์ชันแปลงไฟล์ .wav เป็น normalized numpy ====
def audio_to_normalized_numpy(wav_file):
    sample_rate, samples = wavfile.read(wav_file)
    if samples.ndim > 1:
        samples = samples[:, 0]  # เอาเฉพาะ channel แรกถ้าเป็น stereo
    samples = samples.astype(np.float32)
    samples -= np.mean(samples)
    samples /= np.std(samples) + 1e-9
    return samples

# ==== ตั้งค่า Streamlit ====
st.set_page_config(page_title="🔍 WAV Audio Comparison", layout="wide")
st.title("🔍 เปรียบเทียบเสียงไฟล์ WAV ด้วย Cross-Correlation")

st.markdown("อัปโหลดไฟล์อ้างอิง (.wav) และไฟล์เสียงทดสอบ (.wav) เพื่อวิเคราะห์ความคล้ายคลึง")

# ==== อัปโหลดไฟล์ ====
reference_file = st.file_uploader("📌 อัปโหลด Reference .wav", type=["wav"], key="ref_wav")
test_files = st.file_uploader("🎧 อัปโหลดไฟล์ทดสอบ (Test .wav)", type=["wav"], accept_multiple_files=True)

# ==== วิเคราะห์เมื่อพร้อม ====
if reference_file and test_files:
    st.success("✅ พร้อมเริ่มวิเคราะห์")

    ref_signal = audio_to_normalized_numpy(reference_file)
    results = []

    for test_file in test_files:
        test_signal = audio_to_normalized_numpy(test_file)

        # ==== พล็อตสัญญาณ ====
        st.subheader(f"🔊 {test_file.name}")
        fig, axs = plt.subplots(2, 1, figsize=(12, 6))
        axs[0].plot(ref_signal, color="blue")
        axs[0].set_title("Reference Signal")
        axs[1].plot(test_signal, color="red")
        axs[1].set_title("Test Signal")
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

        # ==== ประเมินความคล้ายคลึง ====
        if max_corr > 0.3:
            similarity = "✅ Very Similar"
        elif max_corr > 0.2:
            similarity = "⚠️ Moderately Similar"
        else:
            similarity = "❌ Not Similar"

        results.append({
            "Filename": test_file.name,
            "Max Correlation": round(max_corr, 5),
            "Similarity": similarity
        })

    # ==== แสดงผลลัพธ์ ====
    df = pd.DataFrame(results)
    st.subheader("📊 ผลการเปรียบเทียบ")
    st.dataframe(df)

    # ==== ปุ่มดาวน์โหลด Excel ====
    towrite = BytesIO()
    df.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)
    st.download_button("⬇️ ดาวน์โหลดผลลัพธ์ (.xlsx)", towrite, file_name="comparison_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

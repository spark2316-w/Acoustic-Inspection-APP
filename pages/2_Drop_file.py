import streamlit as st
import numpy as np
import librosa
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

# ==== ตั้งค่าเบื้องต้น ====
EXCEL_LOG_FILE = 'sound_inspection_log.xlsx'
SAMPLERATE = 44100
MIN_AMPLITUDE = 0.05

# ==== ฟังก์ชันช่วย ====
def normalize_audio(y):
    return y / np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else y

def align_peak_to_peak(y_ref, y_target):
    peak_ref = np.argmax(np.abs(y_ref))
    peak_target = np.argmax(np.abs(y_target))
    shift = peak_ref - peak_target
    y_target_shifted = np.roll(y_target, shift)
    min_len = min(len(y_ref), len(y_target_shifted))
    return y_ref[:min_len], y_target_shifted[:min_len]

def plot_waveform(x, y):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, label='Reference')
    ax.plot(y, label='Input (Aligned)', alpha=0.7)
    ax.set_title('Waveform Comparison (Aligned by Peak)')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

def plot_correlation_bar(corr_abs, threshold):
    fig, ax = plt.subplots(figsize=(4, 3))
    color = 'green' if corr_abs >= threshold else 'red'
    ax.bar(['Correlation'], [corr_abs], color=color)
    ax.axhline(threshold, color='blue', linestyle='--', label=f'Threshold = {threshold:.4f}')
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Value')
    ax.set_title('Correlation Value')
    ax.legend()
    st.pyplot(fig)

def load_audio(file):
    try:
        y, _ = librosa.load(file, sr=SAMPLERATE, mono=True)
        return normalize_audio(y)
    except Exception as e:
        st.error(f"❌ ไม่สามารถโหลดไฟล์เสียงได้: {str(e)}")
        return None

# ==== UI ====
st.title("🔍 ตรวจสอบเสียงด้วย Correlation")

# ==== อัปโหลดเสียงอ้างอิง ====
st.subheader("📥 อัปโหลดเสียงอ้างอิง (Reference Sound)")
ref_file = st.file_uploader("อัปโหลดไฟล์เสียงอ้างอิง (.wav เท่านั้น)", type=['wav'])

if ref_file is None:
    st.warning("⚠️ กรุณาอัปโหลดเสียงอ้างอิงก่อน")
    st.stop()

ref_y = load_audio(ref_file)
if ref_y is None:
    st.stop()
else:
    st.success("✅ โหลดเสียงอ้างอิงสำเร็จแล้ว")

# ==== อัปโหลด Threshold ====
st.subheader("📊 อัปโหลดไฟล์ Threshold (.txt)")
threshold_file = st.file_uploader("อัปโหลดไฟล์ threshold (.txt)", type=['txt'])

if threshold_file is None:
    st.warning("⚠️ กรุณาอัปโหลดไฟล์ Threshold ก่อน")
    st.stop()

try:
    threshold = float(threshold_file.read().decode().strip())
    st.success(f"✅ โหลด Threshold สำเร็จ: `{threshold:.4f}`")
except Exception as e:
    st.error(f"❌ ไม่สามารถอ่าน Threshold ได้: {str(e)}")
    st.stop()

# ==== อัปโหลดหรืออัดเสียงตรวจสอบ ====
st.subheader("🎧 อัปโหลดเสียงเพื่อตรวจสอบ")
audio_file = st.file_uploader("อัปโหลดไฟล์เสียงเพื่อตรวจสอบ (.wav เท่านั้น)", type=['wav'])

if audio_file is not None:
    y_input = load_audio(audio_file)
    if y_input is None:
        st.stop()

    peak_amp = np.max(np.abs(y_input))
    if peak_amp < MIN_AMPLITUDE:
        st.warning(f"🔇 ไม่พบเสียงการเคาะ (Peak Amplitude = {peak_amp:.4f}) → ยกเลิกการวิเคราะห์")
        st.stop()

    x_aligned, y_aligned = align_peak_to_peak(ref_y, y_input)
    corr = np.corrcoef(x_aligned, y_aligned)[0, 1]
    corr_abs = abs(corr)
    status = "✅ Good" if corr_abs >= threshold else "❌ Faulty"

    # ==== แสดงผล ====
    st.subheader("📊 ผลการวิเคราะห์")
    st.write(f"**Correlation:** `{corr_abs:.4f}` → {status}")

    st.subheader("📈 กราฟเสียง (Aligned)")
    plot_waveform(x_aligned, y_aligned)

    st.subheader("📉 ค่าความสัมพันธ์ (Correlation)")
    plot_correlation_bar(corr_abs, threshold)

    # ==== บันทึกผล ====
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {'Datetime': now, 'Correlation': corr_abs, 'Result': status}

    try:
        log_data = pd.read_excel(EXCEL_LOG_FILE)
        log_data = pd.concat([log_data, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        log_data = pd.DataFrame([new_entry])

    log_data.to_excel(EXCEL_LOG_FILE, index=False)
    st.success(f"📝 บันทึกผลลงไฟล์ `{EXCEL_LOG_FILE}` เรียบร้อยแล้ว")

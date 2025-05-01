import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import librosa
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

# ==== ตั้งค่า ==== 
REF_FILE = r'Data/TestGG/Recording_107.m4a'
THRESHOLD_FILE = 'threshold_value.txt'
EXCEL_LOG_FILE = 'sound_inspection_log.csv'  # เปลี่ยนเป็น .csv
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

# ==== โหลดเสียงอ้างอิงและ Threshold ==== 
ref_y, sr = librosa.load(REF_FILE, sr=SAMPLERATE, mono=True)
ref_y = normalize_audio(ref_y)

with open(THRESHOLD_FILE, 'r') as f:
    threshold = float(f.read().strip())

# ==== UI ==== 
st.title("🔍 ตรวจสอบเสียงด้วย Correlation")
st.write(f"🎯 **Threshold ที่ใช้:** `{threshold:.4f}`")

# ใช้ JavaScript สำหรับการบันทึกเสียงจากไมโครโฟน
record_audio_html = """
    <script>
    let audioBlob;
    const startButton = document.getElementById("start-button");
    const stopButton = document.getElementById("stop-button");
    const audioElement = document.getElementById("audio-element");

    let mediaRecorder;
    const chunks = [];

    startButton.onclick = () => {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                audioBlob = new Blob(chunks, { type: "audio/wav" });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioElement.src = audioUrl;
                window.audioBlob = audioBlob;
            };
            mediaRecorder.start();
        });
    };

    stopButton.onclick = () => {
        mediaRecorder.stop();
    };
    </script>
    <button id="start-button">Start Recording</button>
    <button id="stop-button">Stop Recording</button>
    <audio id="audio-element" controls></audio>
"""

components.html(record_audio_html, height=300)

# ให้ผู้ใช้สามารถส่งข้อมูลเสียงจาก JavaScript กลับมา
if "audioBlob" in globals():
    audio_data = globals()["audioBlob"]
    st.audio(audio_data, format="audio/wav")

    # หลังจากบันทึกเสียงเสร็จแล้ว, ทำการประมวลผลเสียง
    try:
        # โหลดเสียงจาก BytesIO
        audio_bytes = BytesIO(audio_data)
        y_input, _ = librosa.load(audio_bytes, sr=SAMPLERATE, mono=True)
        y_input = normalize_audio(y_input)
        peak_amp = np.max(np.abs(y_input))

        if peak_amp < MIN_AMPLITUDE:
            st.warning(f"🔇 ไม่พบเสียงการเคาะ (Peak Amplitude = {peak_amp:.4f}) → ยกเลิกการวิเคราะห์")
        else:
            x_aligned, y_aligned = align_peak_to_peak(ref_y, y_input)

            corr = np.corrcoef(x_aligned, y_aligned)[0, 1]
            corr_abs = abs(corr)
            status = "✅ Good" if corr_abs >= threshold else "❌ Faulty"

            st.subheader("📊 ผลการวิเคราะห์")
            st.write(f"**Correlation:** `{corr_abs:.4f}` → {status}")

            st.subheader("📈 กราฟเสียง (Aligned)")
            plot_waveform(x_aligned, y_aligned)

            st.subheader("📉 ค่าความสัมพันธ์ (Correlation)")
            plot_correlation_bar(corr_abs, threshold)

            # บันทึกผล
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = {'Datetime': now, 'Correlation': corr_abs, 'Result': status}

            try:
                log_data = pd.read_csv(EXCEL_LOG_FILE)
                log_data = log_data.append(new_entry, ignore_index=True)
            except FileNotFoundError:
                log_data = pd.DataFrame([new_entry])

            log_data.to_csv(EXCEL_LOG_FILE, index=False)  # บันทึกเป็น CSV
            st.success(f"📝 บันทึกผลลงไฟล์ `{EXCEL_LOG_FILE}` เรียบร้อยแล้ว")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการอ่านไฟล์เสียง: {str(e)}")

import streamlit as st
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="Acoustic Inspection Guide", page_icon="📘", layout="wide")

# ==== Helper ====
def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo1_b64 = image_to_base64("images/logo1.png")
logo2_b64 = image_to_base64("images/logo2.png")

# ==== Custom CSS ====
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
    padding-top: 0;
}
@keyframes float {
  0% { transform: translatey(0px); }
  50% { transform: translatey(-10px); }
  100% { transform: translatey(0px); }
}
.logo-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    margin-top: 10px;
}
.logo-bar img {
    height: 120px;
    object-fit: contain;
    animation: float 3s ease-in-out infinite;
}
h1 {
    font-size: 75px;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
}
.footer {
    margin-top: 100px;
    text-align: center;
    color: #999;
    font-size: 14px;
}
div[data-testid="stExpander"] {
    background-color: #1e293b;
    color: white;
    border-radius: 8px;
}
div[data-testid="stExpander"] span {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==== Header ====
st.markdown(f"""
<div class="logo-bar">
    <img src="data:image/png;base64,{logo1_b64}" alt="logo1">
    <img src="data:image/png;base64,{logo2_b64}" alt="logo2">
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: white; font-size: 100px; font-weight: bold;'>
        คำแนะนำการใช้งาน <span style="color: #1DA1F2;"> Apps
    </h1>
    <p style="text-align: center; font-size: 24px; color: white;">
        ตรวจสอบวัสดุด้วยเสียงได้ทั้งแบบ Real-time และ Upload
    </p>
</div>
""", unsafe_allow_html=True)

# ==== คู่มือการใช้งาน ====
with st.expander("📘 คู่มือการใช้งานแอปตรวจสอบเสียง"):
    st.markdown("""
### 🧭 วิธีใช้งานแอป Acoustic Inspection

#### 🔹 ขั้นตอนที่ 1: อัปโหลดเสียงอ้างอิง
- ไปที่หน้าเมนูหลักของแอป
- อัปโหลดไฟล์ `.wav` ที่เป็นเสียงของวัสดุที่ดี (Reference)

#### 🔹 ขั้นตอนที่ 2: อัปโหลด Threshold
- สร้างไฟล์ `.txt` ที่ภายในมีค่าตัวเลขเดียว เช่น `0.75`
- อัปโหลดในหัวข้อ Threshold เพื่อใช้เป็นเกณฑ์วัดความคล้ายเสียง

#### 🔹 ขั้นตอนที่ 3: ตรวจสอบเสียง
- อัปโหลดเสียงที่ต้องการตรวจสอบ (ไฟล์ `.wav`) หรือใช้เมนูบันทึกเสียงแบบ Real-time
- ระบบจะวิเคราะห์และแสดงผลเป็น:
  - ✅ **Good**: ถ้าเสียงมีความคล้ายกับเสียงอ้างอิง
  - ❌ **Faulty**: ถ้ามีความแตกต่างอย่างชัดเจน

#### 🔹 ขั้นตอนที่ 4: ตรวจสอบผลลัพธ์ย้อนหลัง
- ระบบจะบันทึกค่าการวิเคราะห์ลงไฟล์ `sound_inspection_log.xlsx`
- คุณสามารถเปิดไฟล์นี้เพื่อตรวจสอบผลย้อนหลังได้

---

#### 📝 หมายเหตุสำคัญ
- รองรับเฉพาะไฟล์ `.wav` เท่านั้น
- หากเสียงเบาเกิน (`Peak Amplitude < 0.05`) ระบบจะข้ามการวิเคราะห์
- หากยังไม่มี Threshold ให้เริ่มต้นที่ `0.75` เป็นค่าพื้นฐาน

---
    """)

# ==== Footer ====
st.markdown("""
<div class="footer">
    Made with ❤️ by [Theeraphat]
</div>
""", unsafe_allow_html=True)

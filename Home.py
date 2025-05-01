import streamlit as st
from PIL import Image
from io import BytesIO
import base64

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="Acoustic Inspection Apps", page_icon="🔨", layout="wide")

# --- ฟังก์ชันแปลงรูปเป็น base64 ---
def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()

# --- โหลดโลโก้ ---
logo1_b64 = image_to_base64("images/logo1.png")
logo2_b64 = image_to_base64("images/logo2.png")

# --- CSS แต่งสไตล์ ---
st.markdown("""
<style>
/* พื้นหลังเข้ม */
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
    padding-top: 0;
}

/* โลโก้ลอยนุ่ม */
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
    animation: float 6s ease-in-out infinite;
}
.logo-bar img {
    height: 120px;
    object-fit: contain;
}

/* หัวข้อใหญ่ */
h1 {
    font-size: 75px;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
}

/* ปุ่ม */
.button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    margin-top: 50px;
    flex-wrap: wrap;
}
.button-container a {
    text-decoration: none;
}
.button {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 20px 50px;
    font-size: 22px;
    font-weight: bold;
    border: none;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    transition: 0.3s;
}
.button:hover {
    background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
    transform: translateY(-5px);
}

/* การ์ดฟีเจอร์ */
.features {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 30px;
    margin-top: 80px;
    flex-wrap: wrap;
}
.feature-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px 20px;
    width: 280px;
    min-height: 220px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.feature-item h3 {
    margin-bottom: 10px;
    font-size: 26px;
}
.feature-item p {
    font-size: 16px;
    margin-top: 10px;
}

/* Footer */
.footer {
    margin-top: 100px;
    text-align: center;
    color: #999;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --- แสดงโลโก้ ---
st.markdown(f"""
<div class="logo-bar">
    <img src="data:image/png;base64,{logo1_b64}" alt="logo1">
    <img src="data:image/png;base64,{logo2_b64}" alt="logo2">
</div>
""", unsafe_allow_html=True)

# --- หัวเรื่องแอป ---
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: white; font-size: 100px; font-weight: bold;'>
        Acoustic <span style="color: #1DA1F2;">Inspection</span> Apps
    </h1>
<p style="text-align: center; font-size: 24px; color: white;">
    ตรวจสอบวัสดุด้วยเสียงได้ทั้งแบบ Real-time และ Upload
</p>
""", unsafe_allow_html=True)

# --- ปุ่มเมนู  ---
st.markdown(f"""
<div class="button-container">
    <a href="/Real_time" target="_self" class="button">🎙️ Real-time ตรวจจับทันที</a>
    <a href="/Drop_file" target="_self" class="button">📂 Upload ไฟล์เสียง</a>
</div>
<hr style="border: 1px solid white; margin: 50px 20px;">
""", unsafe_allow_html=True)


# --- การ์ดฟีเจอร์ ---
st.markdown("""
<div class="features">
    <div class="feature-item">
        <h3>🎤 ตรวจจับทันที</h3>
        <p>ฟังเสียงแบบ Real-time แล้ววิเคราะห์ได้ทันที</p>
    </div>
    <div class="feature-item">
        <h3>📂 อัปโหลดไฟล์</h3>
        <p>รองรับการวิเคราะห์ไฟล์เสียงที่บันทึกไว้</p>
    </div>
    <div class="feature-item">
        <h3>🧠 วิเคราะห์ด้วย AI</h3>
        <p>ประเมินคุณภาพวัสดุอัตโนมัติด้วย Machine Learning</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    Made with ❤️ by [Theeraphat]
</div>
""", unsafe_allow_html=True)

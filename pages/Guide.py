import streamlit as st
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="Acoustic Inspection Apps", page_icon="🔨", layout="wide")

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo1_b64 = image_to_base64("images/logo1.png")
logo2_b64 = image_to_base64("images/logo2.png")

st.markdown("""
<style>
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
}
.logo-bar img {
    height: 120px;
    object-fit: contain;
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
</style>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="footer">
    Made with ❤️ by [Theeraphat]
</div>
""", unsafe_allow_html=True)

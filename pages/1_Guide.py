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

# ==== Load Images as Base64 ====
logo1_b64 = image_to_base64("images/logo1.png")
logo2_b64 = image_to_base64("images/logo2.png")
sm57_b64 = image_to_base64("images/SM57.png")
bmg11s_b64 = image_to_base64("images/interface.png")
#ภาพที่ใช้ในคู่มือ
Home_b64 = image_to_base64("images/Home.png")
pick_b64 = image_to_base64("images/pick.png")
sum_b64 = image_to_base64("images/sum.png")

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
/* ปุ่มเฉพาะใน .feature-item */
.feature-item .button {{
    display: block;
    width: 100%;
    margin-top: 20px;
    font-size: 18px;
    padding: 15px 0;
}}

.footer {{
    margin-top: 100px;
    text-align: center;
    color: #999;
    font-size: 14px;
}}

/* ---------- รองรับหน้าจอมือถือ ---------- */
@media (max-width: 768px) {{
    h1 {{
        font-size: 40px !important;
    }}
    .logo-bar {{
        flex-direction: column;
        gap: 15px;
    }}
    .logo-bar img {{
        height: 70px;
    }}
    .button {{
        padding: 15px 30px;
        font-size: 18px;
    }}
    .button-container {{
        flex-direction: column;
        gap: 20px;
    }}
    .features {{
        flex-direction: column;
        align-items: center;
    }}
    .feature-item {{
        width: 90%;
        min-height: auto;
    }}
    .feature-item h3 {{
        font-size: 22px;
    }}
    .feature-item p {{
        font-size: 14px;
    }}
}}
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
    <h1>
        คำแนะนำการใช้งาน <span style="color: #1DA1F2;"> Apps</span>
    </h1>
    <p style="text-align: center; font-size: 24px; color: white;">
        ตรวจสอบวัสดุด้วยเสียงได้ทั้งแบบ Real-time และ Upload
    </p>
</div>
""", unsafe_allow_html=True)


# ==== คู่มืออุปกรณ์ ====
with st.expander("🎤 อุปกรณ์ที่ใช้ในการตรวจสอบเสียง"):
    st.markdown("""
### 🔧 รายการอุปกรณ์ที่ใช้ในการเก็บข้อมูลเสียง

#### 🎙️ ไมโครโฟน: Shure SM57
- ไมโครโฟนไดนามิกที่มีรูปแบบการรับเสียงแบบคาร์ดิออยด์
- ทนทาน เหมาะสำหรับการบันทึกเสียงเครื่องดนตรีและเสียงเคาะโลหะ
- ความถี่ตอบสนอง: 40Hz – 15kHz
- รองรับระดับเสียงสูงสุด (SPL) ถึง 150dB
    """)
    st.markdown(f'<img src="data:image/png;base64,{sm57_b64}" width="400">', unsafe_allow_html=True)

    st.markdown("""
#### 🔈 อินเทอร์เฟซเสียง: Bomge BMG-11S
- การ์ดเสียง USB รองรับความละเอียด 24-bit/192kHz
- มีพอร์ต XLR พร้อม Phantom Power 48V สำหรับไมโครโฟนคอนเดนเซอร์
- เหมาะสำหรับการบันทึกเสียงในสตูดิโอและการสตรีมมิง
    """)
    st.markdown(f'<img src="data:image/png;base64,{bmg11s_b64}" width="400">', unsafe_allow_html=True)

    st.markdown("""
#### 🧱 วัสดุที่ใช้ทดสอบ
- ท่อนเหล็กกลม ขนาด 6 หุน (ประมาณ 19 มม.) ยาว 10 ซม.
- ใช้เป็นชิ้นงานสำหรับตรวจสอบเสียง
- มีทั้งชิ้นงานที่สมบูรณ์ และชิ้นงานที่ผ่านการตัด เจาะ หรือขูด เพื่อจำลองกรณีชำรุด
- อิฐมวลเบา Q-con 7.5 cm x 20 cm x 40 cm 
- ใช้เป็นชิ้นงานสำหรับตรวจสอบเสียง
- เป็นชิ้นงานที่ได้ผ่านการตรวจสอบคุณภาพแล้ว โดยแบ่งออกเป็น เกรด A และเกรด B


#### 🖥️ อุปกรณ์คอมพิวเตอร์
- คอมพิวเตอร์หรือแล็ปท็อปที่รองรับ USB interface
- ระบบปฏิบัติการที่สามารถใช้งาน Streamlit ได้ เช่น Windows 10+

---

### 💡 คำแนะนำการจัดวาง
- วางไมโครโฟนห่างจากชิ้นงานประมาณ 1-2 ซม.
- ใช้การแขวนท่อเหล็กกับเชือกเพื่อให้เกิดเสียงที่ชัดเจน
- ทำการเคาะบริเวณเดียวกันทุกครั้งเพื่อความแม่นยำของข้อมูล
- สำหรับอิฐมวลเบา ใช้จุกยางวางรองอิฐเพื่อให้เกิดเสียงที่ชัดเจน
- ควรทำการทดสอบในพื้นที่ที่มีเสียงรบกวนต่ำ เช่น ห้องปิด หรือห้องเก็บเสียง
    """)

# ==== คู่มือแอป ====
with st.expander("📘 คู่มือการใช้งานแอปตรวจสอบเสียง"):
    st.markdown("""
### 🧭 วิธีใช้งานแอป Acoustic Inspection

#### 🔹 ขั้นตอนที่ 1: เลือกฟังก์ชั่นที่ต้องการใช้งาน
- ไปที่หน้าเมนูหลักของแอป
- เลือกฟังก์ชั่นที่ต้องการใช้งานเช่น Steel
""")
    st.markdown(f'<img src="data:image/png;base64,{Home_b64}" width="400">', unsafe_allow_html=True) #รูปหน้าเว็บ
    
    st.markdown("""
#### 🔹 ขั้นตอนที่ 2: อัปโหลดเสียงที่ต้องการทดสอบ
- เลือกเมนู **Upload Reference** เพื่ออัปโหลดเสียงทดสอบ
- อัปโหลดไฟล์ `.wav` ที่เป็นเสียงของวัสดุที่ดี
""")
    st.markdown(f'<img src="data:image/png;base64,{pick_b64}" width="400">', unsafe_allow_html=True) #กดbrowser
    
    st.markdown("""
#### 🔹 ขั้นตอนที่ 3: ตรวจสอบเสียง
- อัปโหลดเสียงที่ต้องการตรวจสอบ (ไฟล์ `.wav`) หรือใช้เมนูบันทึกเสียงแบบ Real-time
- ระบบจะวิเคราะห์และแสดงผลเป็น:
  - ✅ **Good**: เสียงมีความคล้ายกับเสียงอ้างอิง
  - ❌ **Faulty**: มีความแตกต่างอย่างชัดเจน
""")
    st.markdown(f'<img src="data:image/png;base64,{sum_b64}" width="400">', unsafe_allow_html=True) #กดbrowser

st.markdown("""
#### 📝 หมายเหตุสำคัญ
- รองรับเฉพาะไฟล์ `.wav` เท่านั้น
- รองรับเพียงโทรศัพท์บางรุ่นเท่านั้น
- ควรใช้ไมโครโฟนที่มีคุณภาพดีเพื่อให้ได้เสียงที่ชัดเจน
    """)

# --- Footer พร้อมลิงก์เพิ่มเติม ---

st.markdown("""
<div class="footer">
    Made with ❤️ by <strong>Theeraphat, Amika</strong><br>
    <div style="margin-top: 10px;">
        <a href="https://github.com/spark2316-w/acoustic-inspection-app" target="_blank" style="color: #ccc; margin: 0 10px; font-size: 24px;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="24" style="vertical-align: middle; margin-right: 8px;">
            GitHub
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
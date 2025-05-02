import streamlit as st
from PIL import Image

st.set_page_config(page_title="Acoustic Inspection Guide", page_icon="📘", layout="wide")

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

# ==== Header Logos ====
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/logo1.png", width=120)
    st.image("images/logo2.png", width=120)

# ==== Header Title ====
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: white; font-size: 100px; font-weight: bold;'>
        คำแนะนำการใช้งาน <span style="color: #1DA1F2;"> Apps</span>
    </h1>
    <p style="text-align: center; font-size: 24px; color: white;">
        ตรวจสอบวัสดุด้วยเสียงได้ทั้งแบบ Real-time และ Upload
    </p>
</div>
""", unsafe_allow_html=True)

# ==== อุปกรณ์ ====
with st.expander("🎤 อุปกรณ์ที่ใช้ในการตรวจสอบเสียง"):
    st.markdown("""
### 🔧 รายการอุปกรณ์ที่ใช้ในการเก็บข้อมูลเสียง

#### 🎙️ ไมโครโฟน: Shure SM57
- ไมโครโฟนไดนามิกที่มีรูปแบบการรับเสียงแบบคาร์ดิออยด์
- ทนทาน เหมาะสำหรับการบันทึกเสียงเครื่องดนตรีและเสียงเคาะโลหะ
- ความถี่ตอบสนอง: 40Hz – 15kHz
- รองรับระดับเสียงสูงสุด (SPL) ถึง 150dB
    """)
    st.image("images/SM57.png", width=400, caption="Shure SM57")

    st.markdown("""
#### 🔈 อินเทอร์เฟซเสียง: Bomge BMG-11S
- การ์ดเสียง USB รองรับความละเอียด 24-bit/192kHz
- มีพอร์ต XLR พร้อม Phantom Power 48V สำหรับไมโครโฟนคอนเดนเซอร์
- เหมาะสำหรับการบันทึกเสียงในสตูดิโอและการสตรีมมิง
    """)
    st.image("images/interface.png", width=400, caption="Bomge BMG-11S")

    st.markdown("""
#### 🧱 วัสดุที่ใช้ทดสอบ
- ท่อนเหล็กกลม ขนาด 6 หุน (ประมาณ 19 มม.) ยาว 10 ซม.
- ใช้เป็นชิ้นงานสำหรับตรวจสอบเสียง
- มีทั้งชิ้นงานที่สมบูรณ์ และชิ้นงานที่ผ่านการตัด เจาะ หรือขูด เพื่อจำลองกรณีชำรุด

#### 🖥️ อุปกรณ์คอมพิวเตอร์
- คอมพิวเตอร์หรือแล็ปท็อปที่รองรับ USB interface
- ระบบปฏิบัติการที่สามารถใช้งาน Streamlit ได้ เช่น Windows 10+

---

### 💡 คำแนะนำการจัดวาง
- วางไมโครโฟนห่างจากชิ้นงานประมาณ 1-2 ซม.
- ใช้การแขวนท่อเหล็กกับเชือกเพื่อให้เกิดเสียงที่ชัดเจน
- ทำการเคาะบริเวณเดียวกันทุกครั้งเพื่อความแม่นยำของข้อมูล
    """)

# ==== คู่มือการใช้งานแอป ====
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
    """)

# ==== Footer ====
st.markdown("""
<div class="footer">
    Made with ❤️ by <strong>Theeraphat</strong>
</div>
""", unsafe_allow_html=True)

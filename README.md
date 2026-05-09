# Handwriting ML System (Thai Digits) 🇹🇭🤖

**วิชา:** AIE322 - Supervised Machine Learning (2/2568)
**เป้าหมายของโปรเจกต์:** สร้างระบบ Web Application ที่สามารถจดจำตัวเลขไทยเขียนมือ (Handwritten Thai Digits) จำนวน 6 คลาส ได้แก่ ๖๕, ๖๖, ๖๗, ๖๘, ๖๙, และ ๗๐ โดยใช้เทคนิค Machine Learning

## 🌟 ฟีเจอร์หลักของระบบ (Features)

1. **ระบบเก็บข้อมูล (Data Collection System)** 
   - ผู้ใช้สามารถวาดตัวเลขบนหน้าเว็บและกดบันทึก ระบบจะแปลงเป็นรูปภาพและเก็บเข้าโฟลเดอร์ให้อัตโนมัติ (Extra +5 pts)
2. **ระบบทายผลตัวเลข (Prediction System)** 
   - วาดตัวเลขลงบน Canvas แล้วให้ AI ทายผล พร้อมแสดงค่าเปอร์เซ็นต์ความมั่นใจ (Confidence Score)
3. **ระบบจัดการหลังบ้าน (Admin Dashboard)**
   - ดูข้อมูลเชิงลึกของโมเดลปัจจุบัน (อัลกอริทึม, ความแม่นยำ, จำนวนฟีเจอร์)
   - อัปโหลดไฟล์โมเดล (`.joblib`) เพื่อเปลี่ยน "สมอง" ของ AI ได้ทันทีโดยไม่ต้อง Restart Server (Dynamic Model Update: Extra +5 pts)

## 📊 โมเดลและการประเมินผล (Model & Evaluation)

เพื่อให้ตรงตามเกณฑ์การให้คะแนนในส่วนของ **Model & Training (15 pts)** และ **Evaluation (25 pts)** นี่คือข้อมูลโดยละเอียดของโมเดลที่ใช้ครับ:

- **อัลกอริทึม (Algorithm):** Random Forest Classifier (100 Trees) 
  - *เปรียบเทียบง่ายๆ:* เหมือนมีนักเรียน 100 คนในห้องช่วยกันดูรูปแล้วโหวตว่ารูปนั้นคือเลขอะไร คำตอบที่คนโหวตเยอะสุดคือคำตอบสุดท้าย
- **ขนาดข้อมูล (Features):** ภาพถูกย่อเป็นขนาด 8x8 และแปลงเป็น 1D Array (64 Features) 
- **ความแม่นยำโดยรวม (Accuracy):** 92.11% (ผ่านเกณฑ์ >= 80% ของอาจารย์)
- **Metrics อื่นๆ (อ้างอิงจาก Test Set):**
  - **Precision เฉลี่ย:** ~0.92
  - **Recall เฉลี่ย:** ~0.92
  - **F1-Score เฉลี่ย:** ~0.91
- *รายละเอียดเพิ่มเติมของการเทรนและ Classification Report สามารถดูได้ในไฟล์ `EDA_Preprocessing.ipynb`*

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
- **Frontend:** HTML5 Canvas, CSS3 (Vanilla), JavaScript
- **Backend:** Python (Flask)
- **Machine Learning:** `scikit-learn` (Random Forest Classifier), `pandas`, `numpy`, `Pillow` (สำหรับการจัดการรูปภาพ)

## 📁 โครงสร้างโปรเจกต์ (Project Structure)
เพื่อความสะดวกในการอัปโหลดขึ้น GitHub และการรันระบบ ไฟล์ทั้งหมดได้ถูกนำมารวมไว้ในโฟลเดอร์เดียวกันดังนี้:

```text
Thai_Digits_ML_Project/
├── EDA_Preprocessing.ipynb  # ไฟล์ Jupyter Notebook สำหรับทำความสะอาดข้อมูลและสอน AI
├── dataset_prepared.csv     # ข้อมูลภาพ 8x8 ที่ถูกแผ่เป็น 1D Array (64 ฟีเจอร์) พร้อมนำไปเทรน
├── handwriting_model.joblib # ไฟล์โมเดล AI (Random Forest) ที่พร้อมใช้งาน
├── app.py                   # โค้ด Backend (Flask Server)
├── requirements.txt         # ไฟล์รวมรายชื่อไลบรารีที่จำเป็น (สำหรับ pip install)
├── dataset/                 # โฟลเดอร์เก็บรูปภาพตัวเลขดิบที่วาดจากหน้าเว็บ (๖๕-๗๐)
├── static/                  # โฟลเดอร์เก็บไฟล์ CSS (style.css) และ JavaScript (script.js)
└── templates/               # โฟลเดอร์เก็บไฟล์หน้าเว็บ HTML (index.html, admin.html, base.html)
```

## 🚀 วิธีการติดตั้งและรันระบบ (How to Run)

1. **ติดตั้งไลบรารีที่จำเป็น:**
   เปิด Terminal และพิมพ์คำสั่ง:
   ```bash
   pip install -r requirements.txt
   ```

2. **เปิดการทำงานของ Server:**
   เข้าไปที่โฟลเดอร์โปรเจกต์ (Thai_Digits_ML_Project) และรันไฟล์ `app.py`:
   ```bash
   python app.py
   ```

3. **เข้าใช้งานผ่าน Browser:**
   - **หน้าผู้ใช้ (วาด & ทายผล):** `http://127.0.0.1:5000/`
   - **หน้าผู้ดูแลระบบ (อัปโหลดโมเดล):** `http://127.0.0.1:5000/admin`

---
*Developed for AIE322 Assignment.*
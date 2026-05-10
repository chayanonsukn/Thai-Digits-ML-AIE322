# Handwriting ML System (Thai Digits)

**รายวิชา:** AIE322 - Supervised Machine Learning (2/2568)
**วัตถุประสงค์:** พัฒนาระบบ Web Application ที่สามารถจดจำตัวเลขไทยเขียนมือ (Handwritten Thai Digits) จำนวน 6 คลาส ได้แก่ ๖๕, ๖๖, ๖๗, ๖๘, ๖๙ และ ๗๐ โดยประยุกต์ใช้เทคนิค Machine Learning

## 🌟 ความสามารถของระบบ (Features)

1. **ระบบรวบรวมข้อมูล (Data Collection System)** 
   - รองรับการวาดตัวเลขบนหน้าเว็บและบันทึกผล ระบบจะดำเนินการแปลงเป็นรูปภาพและจัดเก็บลงในโฟลเดอร์โดยอัตโนมัติ (Extra +5 pts)
2. **ระบบพยากรณ์ตัวเลข (Prediction System)** 
   - รองรับการวาดตัวเลขลงบน Canvas เพื่อให้แบบจำลอง (Model) ทำการพยากรณ์ พร้อมแสดงค่าความเชื่อมั่น (Confidence Score)
3. **ระบบจัดการหลังบ้าน (Admin Dashboard)**
   - แสดงข้อมูลเชิงลึกของแบบจำลองที่ใช้งานอยู่ (อัลกอริทึม, ความแม่นยำ, จำนวนฟีเจอร์)
   - รองรับการอัปโหลดไฟล์แบบจำลอง (`.joblib`) เพื่อปรับเปลี่ยนการทำงานได้ทันทีโดยไม่ต้องเริ่มระบบใหม่ (Dynamic Model Update: Extra +5 pts)

## 📊 แบบจำลองและการประเมินผล (Model & Evaluation)

ข้อมูลเชิงรายละเอียดของแบบจำลองอ้างอิงตามเกณฑ์ **Model & Training (15 pts)** และ **Evaluation (25 pts)**:

- **อัลกอริทึม (Algorithm):** Random Forest Classifier (100 Trees) 
  - *หลักการทำงาน:* คล้ายการให้ผู้เชี่ยวชาญ 100 คนร่วมกันพิจารณาภาพและลงคะแนนเสียง โดยระบบจะเลือกคำตอบที่ได้รับคะแนนโหวตสูงสุด
- **ลักษณะข้อมูล (Features):** ภาพถูกปรับขนาดเป็น 8x8 และแปลงรูปแบบเป็น 1D Array (64 Features) 
- **ความแม่นยำ (Accuracy):** ~92% (ผ่านเกณฑ์ >= 80%)
- **ตัวชี้วัดอื่นๆ (Metrics จาก Test Set):**
  - **Precision เฉลี่ย:** ~0.92
  - **Recall เฉลี่ย:** ~0.92
  - **F1-Score เฉลี่ย:** ~0.91
- *รายละเอียดเพิ่มเติมขั้นตอนการฝึกสอน (Training), ข้อมูล Cross-Validation และ Error Analysis สามารถตรวจสอบได้ในไฟล์ `EDA_Preprocessing.ipynb`*

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
- **Frontend:** HTML5 Canvas, CSS3 (Vanilla), JavaScript
- **Backend:** Python (Flask)
- **Machine Learning:** `scikit-learn` (Random Forest, Decision Tree), `pandas`, `numpy`, `Pillow` (สำหรับการประมวลผลภาพ)

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
Thai_Digits_ML_Project/
├── EDA_Preprocessing.ipynb  # ไฟล์ Jupyter Notebook สำหรับเตรียมข้อมูล ฝึกสอน และประเมินผล
├── dataset_prepared.csv     # ข้อมูลภาพ 8x8 รูปแบบ 1D Array (64 ฟีเจอร์)
├── handwriting_model.joblib # ไฟล์แบบจำลองหลัก (Random Forest)
├── demo_decision_tree.joblib # ไฟล์แบบจำลองทางเลือกสำหรับการสาธิต (Decision Tree)
├── app.py                   # โค้ด Backend (Flask Server)
├── requirements.txt         # ไฟล์รวบรวมไลบรารีที่จำเป็น
├── dataset/                 # โฟลเดอร์จัดเก็บรูปภาพตัวเลข (๖๕-๗๐)
├── static/                  # โฟลเดอร์จัดเก็บไฟล์ CSS และ JavaScript
└── templates/               # โฟลเดอร์จัดเก็บหน้าเว็บ HTML
```

## 🚀 วิธีการติดตั้งและทดสอบ (How to Run)

1. **ติดตั้งไลบรารีที่จำเป็น:**
   ```bash
   pip install -r requirements.txt
   ```

2. **เริ่มต้นการทำงานของ Server:**
   เข้าไปที่โฟลเดอร์โปรเจกต์และรันไฟล์ `app.py`:
   ```bash
   cd Thai_Digits_ML_Project
   python app.py
   ```

3. **การเข้าถึงระบบผ่านบราวเซอร์:**
   - **หน้าหลัก (วาดและทดสอบ):** `http://127.0.0.1:5000/`
   - **หน้าจัดการระบบ (Admin):** `http://127.0.0.1:5000/admin`

---
*Developed for AIE322 Assignment.*
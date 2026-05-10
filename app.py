from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime
import io
import numpy as np
import joblib
import pandas as pd
from PIL import Image

app = Flask(__name__)

# กำหนดโฟลเดอร์สำหรับเก็บข้อมูล
DATASET_DIR = 'dataset'
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# โหลดโมเดล AI (ใช้เส้นทางอ้างอิงจากโฟลเดอร์ปัจจุบัน)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'handwriting_model.joblib')
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    model = None
    print(f"⚠️ Warning: Could not load model from {MODEL_PATH}. Error: {e}")

# รายชื่อตัวเลขเป้าหมาย (๖๕ - ๗๐)
TARGET_CLASSES = ['65', '66', '67', '68', '69', '70']

# สร้างโฟลเดอร์ย่อยสำหรับแต่ละ Class
for label in TARGET_CLASSES:
    class_path = os.path.join(DATASET_DIR, label)
    if not os.path.exists(class_path):
        os.makedirs(class_path)

@app.route('/')
def index():
    return render_template('index.html', classes=TARGET_CLASSES)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'status': 'error', 'message': 'โมเดลยังไม่พร้อมใช้งาน'}), 500

    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'status': 'error', 'message': 'ไม่พบข้อมูลรูปภาพ'}), 400

    try:
        # 1. แปลง Base64 เป็นรูปภาพ
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(image_bytes))

        # 2. Preprocessing (แปลงเป็นขาวดำและปรับขนาด 8x8)
        img_process = img.convert('L').resize((8, 8))
        
        # 3. แปลงเป็นตัวเลขและ Flatten เป็น 1D Array (64 ฟีเจอร์)
        img_array = np.array(img_process)
        # กลับสีภาพ (Invert) ให้เป็นพื้นดำตัวเลขขาวเหมือนตอน Train
        img_inverted = 255 - img_array
        # ปรับสเกล (Normalization) 0-1
        img_normalized = img_inverted / 255.0
        img_flat = img_normalized.flatten()
        
        # 4. แปลงเป็น DataFrame เพื่อให้ชื่อคอลัมน์ตรงกับตอน Train
        columns = [f"pixel_{i+1}" for i in range(8*8)]
        df_pred = pd.DataFrame([img_flat], columns=columns)

        # 5. ทายผลและความมั่นใจ (Confidence)
        prediction = model.predict(df_pred)[0]
        
        # ตรวจสอบว่าโมเดลรองรับการหาค่าความน่าจะเป็น (Probability) หรือไม่
        confidence = ""
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(df_pred)[0]
                max_prob = max(proba) * 100
                confidence = f"{max_prob:.2f}"
        except Exception:
            pass

        return jsonify({
            'status': 'success', 
            'prediction': str(prediction),
            'confidence': confidence,
            'message': f'AI ทำนายว่าเป็นเลข: {prediction}'
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/save-sample', methods=['POST'])
def save_sample():
    data = request.json
    image_data = data.get('image') # ข้อมูลรูปภาพแบบ Base64
    label = data.get('label')     # ตัวเลขที่เป็นคนเขียน (เช่น '65')

    if not image_data or not label:
        return jsonify({'status': 'error', 'message': 'ข้อมูลไม่ครบถ้วน'}), 400

    try:
        # ลบส่วนหัวของ Base64 ออก (data:image/png;base64,)
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        # ตั้งชื่อไฟล์ตามเวลาเพื่อไม่ให้ซ้ำกัน
        filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        filepath = os.path.join(DATASET_DIR, label, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return jsonify({'status': 'success', 'message': f'บันทึกรูป {label} เรียบร้อยแล้ว!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    if model is None:
        return jsonify({'status': 'error', 'message': 'ยังไม่มีโมเดลถูกโหลดเข้าสู่ระบบ'}), 404
    
    try:
        # ดึงข้อมูลจากตัวแปรโมเดลโดยตรง (เหมาะสำหรับใช้อธิบายตอนนำเสนอ)
        n_features = getattr(model, 'n_features_in_', 'ไม่ทราบ')
        classes = getattr(model, 'classes_', []).tolist() if hasattr(model, 'classes_') else []

        # ดึงข้อมูลที่แนบมาพิเศษ (Custom Attributes)
        model_type = getattr(model, 'algorithm_name_', 'ไม่มีข้อมูล')
        accuracy = getattr(model, 'test_accuracy_', 'ไม่มีข้อมูล')
        training_date = getattr(model, 'training_date_', 'ไม่มีข้อมูล')
        training_samples = getattr(model, 'training_samples_', 'ไม่มีข้อมูล')

        return jsonify({
            'status': 'success',
            'data': {
                'algorithm': model_type,
                'features': n_features,
                'classes': classes,
                'accuracy': accuracy,
                'training_date': training_date,
                'training_samples': training_samples
            }
        })
    except Exception as e:
         return jsonify({'status': 'error', 'message': f'เกิดข้อผิดพลาดในการดึงข้อมูล: {str(e)}'}), 500

@app.route('/api/upload-model', methods=['POST'])
def upload_model():
    global model # ประกาศใช้ตัวแปร global เพื่อให้เปลี่ยนโมเดลในหน่วยความจำได้ทันที
    
    if 'model_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'ไม่พบไฟล์ที่อัปโหลด'}), 400
        
    file = request.files['model_file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'ไม่ได้เลือกไฟล์'}), 400
        
    if not file.filename.endswith('.joblib'):
         return jsonify({'status': 'error', 'message': 'กรุณาอัปโหลดไฟล์นามสกุล .joblib เท่านั้น'}), 400
         
    try:
        # 1. บันทึกไฟล์ที่อัปโหลดเป็นชื่อใหม่ เพื่อไม่ให้ทับไฟล์ต้นฉบับของผู้ใช้
        UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'active_model.joblib')
        file.save(UPLOAD_PATH)
        
        # 2. โหลดโมเดลใหม่เข้าสู่ระบบทันที (ฟื้นคืนชีพโดยไม่ต้อง Restart)
        model = joblib.load(UPLOAD_PATH)
        # เตรียมข้อมูลโมเดลกลับไปให้ frontend ใช้อัปเดต UI ทันที
        try:
            n_features = getattr(model, 'n_features_in_', 'ไม่ทราบ')
            classes = getattr(model, 'classes_', []).tolist() if hasattr(model, 'classes_') else []
            model_type = getattr(model, 'algorithm_name_', 'ไม่มีข้อมูล')
            accuracy = getattr(model, 'test_accuracy_', 'ไม่มีข้อมูล')
            training_date = getattr(model, 'training_date_', 'ไม่มีข้อมูล')
            training_samples = getattr(model, 'training_samples_', 'ไม่มีข้อมูล')
            model_info = {
                'algorithm': model_type,
                'features': n_features,
                'classes': classes,
                'accuracy': accuracy,
                'training_date': training_date,
                'training_samples': training_samples
            }
        except Exception:
            model_info = None

        print('✅ Model reloaded from upload:', MODEL_PATH)

        return jsonify({'status': 'success', 'message': 'อัปโหลดและโหลดโมเดลใหม่สำเร็จ!', 'data': model_info})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

if __name__ == '__main__':
    # รันบนพอร์ตที่กำหนดโดยตัวแปรสภาพแวดล้อม `PORT` (ค่าเริ่มต้น 5000)
    try:
        port = int(os.environ.get('PORT', '5000'))
    except Exception:
        port = 5000
    # ปิด reloader เพื่อให้แอปทำงานเป็นกระบวนการเดียว (อัปเดตโมเดลจะมีผลทันที)
    app.run(debug=True, port=port, use_reloader=False, threaded=True)
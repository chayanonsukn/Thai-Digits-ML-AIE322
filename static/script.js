const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const messageDiv = document.getElementById('message');
let isDrawing = false;

// Tab Switch Logic
function switchMode(mode) {
    const tabs = document.querySelectorAll('.tab-btn');
    const predictBtn = document.getElementById('btn-predict-action');
    const collectBtn = document.getElementById('btn-collect-action');
    const collectOptions = document.getElementById('collect-options');
    const predictionResult = document.getElementById('prediction-result');

    tabs.forEach(tab => tab.classList.remove('active'));
    clearCanvas(); // Clear canvas when switching modes

    if (mode === 'predict') {
        tabs[0].classList.add('active');
        predictBtn.style.display = 'flex';
        collectBtn.style.display = 'none';
        collectOptions.style.display = 'none';
        document.querySelector('.subtitle').innerText = 'ทดสอบโมเดลโดยวาดตัวเลขลงในกรอบ';
    } else if (mode === 'collect') {
        tabs[1].classList.add('active');
        predictBtn.style.display = 'none';
        collectBtn.style.display = 'flex';
        collectOptions.style.display = 'block';
        predictionResult.style.display = 'none';
        document.querySelector('.subtitle').innerText = 'เลือกตัวเลขที่ต้องการและวาดลงในกรอบ';
    }
}

// ตั้งค่าลายเส้นให้ดูนุ่มนวล
ctx.lineWidth = 15;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';
ctx.strokeStyle = '#2C2C2C'; // สีน้ำตาลเข้มเกือบดำเพื่อให้เข้ากับธีม

// ฟังก์ชันระบุตำแหน่งที่ถูกต้อง (รองรับ Touch Screen)
function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
        x: clientX - rect.left,
        y: clientY - rect.top
    };
}

// เริ่มวาด
function startDrawing(e) {
    isDrawing = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    // เพิ่มเอฟเฟกต์การกดปุ่มบันทึก (Feedback)
    canvas.style.borderColor = '#D4AF37';
}

// กำลังวาด
function draw(e) {
    if (!isDrawing) return;
    e.preventDefault(); // ป้องกันการ Scroll บนมือถือ
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

// หยุดวาด
function stopDrawing() {
    isDrawing = false;
    canvas.style.borderColor = '#F3F0E6';
}

// Event Listeners สำหรับเมาส์
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseleave', stopDrawing);

// Event Listeners สำหรับมือถือ (Touch)
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', stopDrawing);

// ล้างหน้าจอพร้อม Animation
function clearCanvas() {
    // ใส่ Fade out effect เล็กน้อยด้วย CSS Transition ถ้าทำได้ แต่ในนี้ใช้เคลียร์ตรงๆ
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    hideMessage();
}

function showMessage(text, type) {
    messageDiv.innerText = text;
    messageDiv.className = type + ' show';
}

function hideMessage() {
    messageDiv.className = '';
    messageDiv.innerText = '';
}

// ส่งข้อมูลไปเก็บที่ Server
async function saveSample() {
    const label = document.getElementById('digit-label').value;
    const imageData = canvas.toDataURL('image/png');

    // ตรวจสอบเบื้องต้นว่ามีการวาดหรือไม่ (เช็คความว่างเปล่าของ Canvas)
    const blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;
    if (canvas.toDataURL() === blank.toDataURL()) {
        showMessage('กรุณาวาดตัวเลขก่อนบันทึก', 'error');
        return;
    }
    
    try {
        const response = await fetch('/save-sample', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData,
                label: label
            }),
        });

        const result = await response.json();
        if (result.status === 'success') {
            showMessage('✨ บันทึกข้อมูลสำเร็จ!', 'success');
            // Feedback: กระพริบสีทองที่ Canvas
            canvas.style.animation = 'pulseGold 0.5s ease-out';
            setTimeout(() => {
                canvas.style.animation = '';
                clearCanvas();
            }, 1000);
        } else {
            showMessage('❌ เกิดข้อผิดพลาด: ' + result.message, 'error');
        }
    } catch (error) {
        showMessage('🔌 ไม่สามารถเชื่อมต่อกับ Server ได้', 'error');
    }
}

// ส่งข้อมูลไปให้ AI ทายผล (Predict)
async function predictDigit() {
    const imageData = canvas.toDataURL('image/png');

    // ตรวจสอบเบื้องต้นว่ามีการวาดหรือไม่
    const blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;
    if (canvas.toDataURL() === blank.toDataURL()) {
        showMessage('กรุณาวาดตัวเลขก่อนทายผล', 'error');
        return;
    }
    
    showMessage('กำลังคิด...', 'info');
    document.getElementById('prediction-result').style.display = 'none';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData
            }),
        });

        const result = await response.json();
        hideMessage();
        
        if (result.status === 'success') {
            document.getElementById('prediction-result').style.display = 'block';
            document.getElementById('pred-number').innerText = result.prediction;
            
            // แสดงค่าความมั่นใจ (ถ้ามี)
            const confElement = document.getElementById('pred-confidence');
            if (result.confidence) {
                confElement.innerHTML = `<i class="fas fa-chart-pie" style="color: var(--primary-gold);"></i> ความมั่นใจ: <strong>${result.confidence}%</strong>`;
                confElement.style.display = 'block';
            } else {
                confElement.style.display = 'none';
            }
            
            // Feedback: กระพริบสีทองที่ Canvas เพื่อให้ดูเท่ๆ
            canvas.style.animation = 'pulseGold 0.5s ease-out';
            setTimeout(() => {
                canvas.style.animation = '';
            }, 1000);
        } else {
            showMessage('❌ เกิดข้อผิดพลาด: ' + result.message, 'error');
        }
    } catch (error) {
        hideMessage();
        showMessage('🔌 ไม่สามารถเชื่อมต่อกับ Server ได้', 'error');
    }
}

from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import pytesseract
 
from datetime import timedelta
 
#設置允許的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 設置靜態文件緩存過期時間
app.send_file_max_age_default = timedelta(seconds=1)
 
 
@app.route('/upload', methods=['POST', 'GET'])  
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "只可以上傳:png、PNG、jpg、JPG、bmp"})
 
        
 
        basepath = os.path.dirname(__file__)  # 當前文件所在路徑
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename)) 
        f.save(upload_path)
 
        # OCR
        img = cv2.imread(upload_path)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\yuhao.lin\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
        user_input = pytesseract.image_to_string(img,lang = "eng")
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('upload_ok.html',userinput=user_input,val1=time.time())
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='127.0.0.1', port=8000, debug=True)
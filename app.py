# app.py
from flask import Flask, render_template, request
import os
from uploader import upload_video
from config import UPLOAD_FOLDER

app = Flask(__name__)

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # 获取上传的文件
    if 'video' not in request.files:
        return "没有选择文件", 400

    video_file = request.files['video']
    if video_file.filename == '':
        return "没有选择文件", 400

    # 获取上传文件的绝对路径
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)

    # 调用上传视频的函数
    upload_result = upload_video(video_path)

    # 判断上传结果
    if isinstance(upload_result, dict) and upload_result.get('status') == 'success':
        return render_template('upload_success.html', result=upload_result)
    else:
        return f"上传失败: {upload_result}"

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from video_creator import VideoCreator
import json
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Lưu trạng thái các job
jobs = {}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Lấy danh sách giọng nói
    creator = VideoCreator()
    return render_template('index.html', voices=creator.gemini_voices)

@app.route('/create_video', methods=['POST'])
def create_video():
    try:
        # Lấy dữ liệu từ form
        text = request.form.get('text', '').strip()
        voice_name = request.form.get('voice', 'Puck')
        if not text:
            return jsonify({'error': 'Text không được để trống'}), 400
        
        # Xử lý file upload
        uploaded_files = request.files.getlist('images')
        image_paths = []
        
        for file in uploaded_files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Thêm UUID để tránh trùng tên file
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                image_paths.append(file_path)
        
        # Tạo job ID
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Đang xử lý...',
            'result': None,
            'error': None
        }
        
        # Tạo video trong thread riêng
        def process_video():
            try:
                creator = VideoCreator()
                output_filename = f"video_{job_id}.mp4"
                
                # Update progress
                jobs[job_id]['progress'] = 25
                jobs[job_id]['message'] = 'Đang tạo âm thanh...'
                
                success, result = creator.create_video(text, image_paths, output_filename, voice_name)
                
                if success:
                    jobs[job_id]['status'] = 'completed'
                    jobs[job_id]['progress'] = 100
                    jobs[job_id]['message'] = 'Hoàn thành!'
                    jobs[job_id]['result'] = output_filename
                else:
                    jobs[job_id]['status'] = 'error'
                    jobs[job_id]['error'] = result
                    jobs[job_id]['message'] = f'Lỗi: {result}'
                
                # Dọn dẹp file upload
                for img_path in image_paths:
                    try:
                        os.remove(img_path)
                    except:
                        pass
                        
            except Exception as e:
                jobs[job_id]['status'] = 'error'
                jobs[job_id]['error'] = str(e)
                jobs[job_id]['message'] = f'Lỗi: {str(e)}'
                
                # Dọn dẹp file upload
                for img_path in image_paths:
                    try:
                        os.remove(img_path)
                    except:
                        pass
        
        # Bắt đầu xử lý
        thread = threading.Thread(target=process_video)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'message': 'Đang bắt đầu tạo video...'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/job_status/<job_id>')
def job_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job không tồn tại'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/download/<filename>')
def download_video(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File không tồn tại'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup/<job_id>')
def cleanup_job(job_id):
    """Xóa job và file output sau khi download"""
    try:
        if job_id in jobs:
            job = jobs[job_id]
            if job['result']:
                file_path = os.path.join(app.config['OUTPUT_FOLDER'], job['result'])
                try:
                    os.remove(file_path)
                except:
                    pass
            del jobs[job_id]
        
        return jsonify({'message': 'Đã xóa'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Tạo thư mục nếu chưa có
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=4000)

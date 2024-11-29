#! /usr/bin/python
# apk add flask
# get: time curl http://localhost:8100/converter?file=/path/to/file.docx
# post: time curl -X POST -F "file=@/path/to/file.docx" http://localhost:8100/converter -o test.pdf
import os
import subprocess
import time
from flask import Flask, request, jsonify, send_from_directory, after_this_request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置文件上传的最大大小和允许的文件类型
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx','doc'}

# 检查文件扩展名是否有效
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 封装文件转换功能
def convert_to_pdf(input_file_path, output_directory):
    """将输入文件转换为 PDF 格式"""
    # 获取文件的基础名称（去除扩展名）
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    
    # 生成 PDF 输出文件路径
    output_pdf_path = os.path.join(output_directory, base_name + '.pdf')

    # 执行 soffice 命令进行转换
    command = ['soffice', '--headless', '--convert-to', 'pdf', input_file_path, '--outdir', output_directory]
    try:
        subprocess.run(command, check=True)
        return output_pdf_path
    except subprocess.CalledProcessError as e:
        return None

# GET 方法：将文件路径作为参数，进行文件转换
@app.route('/converter', methods=['GET'])
def convert_file():
    file_path = request.args.get('file')

    if not file_path or not os.path.isfile(file_path):
        return jsonify({'error': 'Invalid file path'}), 400

    # 调用封装好的文件转换函数
    output_pdf_path = convert_to_pdf(file_path, os.path.dirname(file_path))

    if output_pdf_path:
        return jsonify({'pdf_file': output_pdf_path}), 200
    else:
        return jsonify({'error': 'Failed to convert the file'}), 500

# POST 方法：接收上传的 Word 文件并转换为 PDF
@app.route('/converter', methods=['POST'])
def upload_and_convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # 为文件生成唯一的 ID（系统时间戳）
        timestamp = str(int(time.time() * 1000))  # 毫秒级时间戳
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # 保存上传的文件
        file.save(file_path)

        # 调用封装好的文件转换函数
        output_pdf_path = convert_to_pdf(file_path, os.path.dirname(file_path))

        if output_pdf_path:
            # 删除原始的 DOCX 文件
            os.remove(file_path)

            # 处理响应，确保在下载后删除 PDF 文件
            @after_this_request
            def delete_pdf(response):
                try:
                    os.remove(output_pdf_path)  # 删除 PDF 文件
                except Exception as e:
                    app.logger.error(f"Error deleting PDF file: {e}")
                return response

            # 返回给用户的 PDF 文件名使用原始文件名
            original_filename = os.path.basename(file.filename)
            return send_from_directory(os.path.dirname(file_path), original_filename.replace('.docx', '.pdf'), as_attachment=True)
        else:
            # 转换失败，删除上传的文件
            os.remove(file_path)
            return jsonify({'error': 'Failed to convert the file'}), 500

    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

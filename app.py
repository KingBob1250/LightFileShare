from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import uuid
from datetime import datetime, timedelta
from functools import wraps

from config import Config
from models import db, File, ShareLink
from utils import allowed_file, safe_filename, send_file_with_range, cleanup_expired_shares

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """首页重定向到登录"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='密码错误')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """管理面板"""
    # 清理过期的分享链接
    cleanup_expired_shares()
    
    # 获取所有文件
    files = File.query.order_by(File.upload_time.desc()).all()
    
    message = request.args.get('message')
    error = request.args.get('error')
    
    return render_template('dashboard.html', 
                         files=files, 
                         message=message, 
                         error=error,
                         share_host=app.config['SHARE_HOST'])

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """文件上传"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    if file and allowed_file(file.filename, enable_check=app.config['ENABLE_FILE_TYPE_CHECK']):
        # 生成安全的文件名
        original_filename = file.filename
        filename = safe_filename(file.filename)
        
        # 如果文件名已存在，添加随机后缀
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 保存文件信息到数据库
        file_record = File(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path)
        )
        
        db.session.add(file_record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '文件上传成功'})
    
    # 不支持的文件类型
    if file.filename and '.' in file.filename:
        file_extension = file.filename.rsplit('.', 1)[1].lower()
    else:
        file_extension = '未知'
    return jsonify({'success': False, 'error': f'不支持的文件类型: .{file_extension}'})

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    """删除文件"""
    file_record = File.query.get_or_404(file_id)
    
    try:
        # 删除物理文件
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 删除数据库记录
        db.session.delete(file_record)
        db.session.commit()
        
        return redirect(url_for('dashboard', message='文件删除成功'))
    except Exception as e:
        return redirect(url_for('dashboard', error=f'删除文件失败: {str(e)}'))

@app.route('/share', methods=['POST'])
@login_required
def share_file():
    """创建分享链接"""
    data = request.get_json()
    file_id = data.get('file_id')
    days = data.get('days', 7)
    
    file_record = File.query.get_or_404(file_id)
    
    try:
        # 创建分享链接
        share_link = ShareLink.create_share_link(file_id, days)
        
        return jsonify({
            'success': True,
            'token': share_link.token,
            'share_url': f"{app.config['SHARE_HOST']}/download/{share_link.token}",
            'filename': file_record.original_filename,
            'message': '分享链接创建成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建分享链接失败: {str(e)}'
        })

@app.route('/download/<token>')
def download_file(token):
    """下载分享的文件"""
    # 查找分享链接
    share_link = ShareLink.query.filter_by(token=token).first()
    
    if not share_link:
        return "分享链接不存在或已过期", 404
    
    if share_link.is_expired:
        return "分享链接已过期", 410
    
    # 获取文件信息
    file_record = share_link.file
    
    if not file_record or not os.path.exists(file_record.file_path):
        return "文件不存在", 404
    
    # 增加下载次数
    share_link.download_count += 1
    db.session.commit()
    
    # 返回文件（支持断点续传）
    return send_file_with_range(file_record.file_path, file_record.original_filename)

@app.route('/api/files')
@login_required
def api_files():
    """API: 获取文件列表"""
    files = File.query.order_by(File.upload_time.desc()).all()
    return jsonify([{
        'id': f.id,
        'filename': f.original_filename,
        'size': f.file_size,
        'size_human': f.file_size_human,
        'upload_time': f.upload_time.isoformat(),
        'shares': [{
            'token': s.token,
            'expire_time': s.expire_time.isoformat(),
            'is_expired': s.is_expired,
            'days_remaining': s.days_remaining
        } for s in f.shares if not s.is_expired]
    } for f in files])

@app.route('/api/shares')
@login_required
def api_shares():
    """API: 获取分享链接列表"""
    shares = ShareLink.query.filter(ShareLink.expire_time > datetime.utcnow()).all()
    return jsonify([{
        'id': s.id,
        'token': s.token,
        'filename': s.file.original_filename,
        'created_time': s.created_time.isoformat(),
        'expire_time': s.expire_time.isoformat(),
        'days_remaining': s.days_remaining,
        'download_count': s.download_count
    } for s in shares])

@app.route('/api/delete_share/<int:share_id>', methods=['DELETE'])
@login_required
def api_delete_share(share_id):
    """API: 删除分享链接"""
    share = ShareLink.query.get_or_404(share_id)
    db.session.delete(share)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/download_file/<int:file_id>')
@login_required
def download_file_admin(file_id):
    """管理员下载文件（需要登录验证）"""
    file_record = File.query.get_or_404(file_id)
    
    if not os.path.exists(file_record.file_path):
        return "文件不存在", 404
    
    # 返回文件（支持断点续传）
    return send_file_with_range(file_record.file_path, file_record.original_filename)

@app.errorhandler(404)
def not_found(error):
    return "页面不存在", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "服务器内部错误", 500

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=False
    ) 
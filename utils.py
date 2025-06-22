import os
import hashlib
from werkzeug.utils import secure_filename
from flask import request, send_file, Response
import mimetypes
import re
from models import db

def allowed_file(filename, allowed_extensions=None, enable_check=True):
    """检查文件类型是否允许"""
    # 如果禁用文件类型检测，直接返回 True
    if not enable_check:
        return True
        
    if allowed_extensions is None:
        allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
                             'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', 'mp3', 
                             'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'torrent', 'apk'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def safe_filename(filename):
    """生成安全的文件名"""
    return secure_filename(filename)

def get_file_size(file_path):
    """获取文件大小"""
    return os.path.getsize(file_path)

def send_file_with_range(file_path, filename):
    """支持断点续传的文件发送"""
    file_size = os.path.getsize(file_path)
    
    # 获取Range头
    range_header = request.headers.get('Range', None)
    
    if range_header:
        # 解析Range头
        byte1, byte2 = 0, None
        m = re.search(r'(\d+)-(\d*)', range_header)
        if not m:
            return send_file(file_path, as_attachment=True, download_name=filename)
        groups = m.groups()
        
        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
        
        if byte2 is None:
            byte2 = file_size - 1
        
        length = byte2 - byte1 + 1
        
        # 设置响应头
        resp = send_file(file_path, as_attachment=True, download_name=filename)
        resp.status_code = 206
        resp.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{file_size}')
        resp.headers.add('Accept-Ranges', 'bytes')
        resp.headers.add('Content-Length', str(length))
        resp.headers['Content-Type'] = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        return resp
    else:
        # 完整文件下载
        resp = send_file(file_path, as_attachment=True, download_name=filename)
        resp.headers.add('Accept-Ranges', 'bytes')
        return resp

def cleanup_expired_shares():
    """清理过期的分享链接"""
    from models import ShareLink
    from datetime import datetime
    
    expired_shares = ShareLink.query.filter(ShareLink.expire_time < datetime.utcnow()).all()
    for share in expired_shares:
        db.session.delete(share)
    db.session.commit()

def format_file_size(size_bytes):
    """格式化文件大小显示"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}" 
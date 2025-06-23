import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 时区配置
    TIMEZONE = os.environ.get('TIMEZONE', 'Asia/Shanghai')  # 默认使用中国时区
    
    # 数据库配置 - 固定路径
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    
    # 文件存储配置 - 固定路径
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 1024 * 1024 * 100))  # 100MB
    
    # 文件类型检测配置
    ENABLE_FILE_TYPE_CHECK = os.environ.get('ENABLE_FILE_TYPE_CHECK', 'false').lower() == 'true'
    
    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # 分享链接配置
    DEFAULT_SHARE_DAYS = int(os.environ.get('DEFAULT_SHARE_DAYS', 7))
    SHARE_HOST = os.environ.get('SHARE_HOST', 'http://localhost:5000')  # 分享链接的host
    
    # 管理员密码
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # 可预览文件类型
    PREVIEWABLE_EXTENSIONS = {
        'image': ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'],
        'text': ['txt', 'md', 'py', 'js', 'css', 'html', 'json', 'xml', 'sh', 'ini'],
        'pdf': ['pdf'],
        'video': ['mp4', 'webm', 'mov'],
        'audio': ['mp3', 'ogg', 'wav'],
    } 
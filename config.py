import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件存储配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
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
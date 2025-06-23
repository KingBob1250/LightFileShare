from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
import uuid
import pytz

db = SQLAlchemy()

def ensure_timezone_aware(dt):
    """确保datetime对象是timezone-aware的"""
    if dt is None:
        return dt
    if dt.tzinfo is None:
        # 假设naive datetime是UTC时间
        return dt.replace(tzinfo=timezone.utc)
    return dt

class File(db.Model):
    """文件信息表"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    upload_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # 关联的分享链接
    shares = db.relationship('ShareLink', backref='file', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<File {self.original_filename}>'
    
    @property
    def file_size_human(self):
        """返回人类可读的文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def get_local_time(self, timezone_str='Asia/Shanghai'):
        """返回指定时区的本地时间"""
        try:
            tz = pytz.timezone(timezone_str)
            utc_time = pytz.utc.localize(self.upload_time) if self.upload_time.tzinfo is None else self.upload_time
            return utc_time.astimezone(tz)
        except:
            return self.upload_time

class ShareLink(db.Model):
    """分享链接表"""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    created_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expire_time = db.Column(db.DateTime, nullable=False)
    download_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<ShareLink {self.token}>'
    
    @property
    def is_expired(self):
        """检查链接是否过期"""
        expire_time_utc = ensure_timezone_aware(self.expire_time)
        return datetime.now(timezone.utc) > expire_time_utc
    
    @property
    def days_remaining(self):
        """返回剩余天数"""
        if self.is_expired:
            return 0
        expire_time_utc = ensure_timezone_aware(self.expire_time)
        delta = expire_time_utc - datetime.now(timezone.utc)
        return delta.days
    
    def get_local_created_time(self, timezone_str='Asia/Shanghai'):
        """返回指定时区的本地创建时间"""
        try:
            tz = pytz.timezone(timezone_str)
            utc_time = pytz.utc.localize(self.created_time) if self.created_time.tzinfo is None else self.created_time
            return utc_time.astimezone(tz)
        except:
            return self.created_time
    
    def get_local_expire_time(self, timezone_str='Asia/Shanghai'):
        """返回指定时区的本地过期时间"""
        try:
            tz = pytz.timezone(timezone_str)
            utc_time = pytz.utc.localize(self.expire_time) if self.expire_time.tzinfo is None else self.expire_time
            return utc_time.astimezone(tz)
        except:
            return self.expire_time
    
    @classmethod
    def create_share_link(cls, file_id, days):
        """创建新的分享链接，如果已有有效分享则更新有效期"""
        # 检查是否已有有效的分享链接
        # 确保比较时两个datetime都是timezone-aware的
        current_utc = datetime.now(timezone.utc)
        existing_share = cls.query.filter_by(file_id=file_id).filter(
            cls.expire_time > current_utc
        ).first()
        
        if existing_share:
            # 如果已有有效分享，更新有效期
            existing_share.expire_time = current_utc + timedelta(days=days)
            db.session.commit()
            return existing_share
        else:
            # 创建新的分享链接
            token = str(uuid.uuid4()).replace('-', '')
            expire_time = current_utc + timedelta(days=days)
            
            share_link = cls(
                token=token,
                file_id=file_id,
                expire_time=expire_time
            )
            
            db.session.add(share_link)
            db.session.commit()
            return share_link 
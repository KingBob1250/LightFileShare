#!/usr/bin/env python3
"""
LightFileShare - 轻量化文件分享平台
使用uvicorn启动文件服务器
"""

import os
import sys
import uvicorn
from app import app, db
from asgiref.wsgi import WsgiToAsgi

def init_database():
    """初始化数据库"""
    try:
        with app.app_context():
            # 创建数据库表
            db.create_all()
            print("✅ 数据库初始化完成")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)

def create_upload_dir():
    """创建上传目录"""
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        print(f"✅ 创建上传目录: {upload_dir}")
    else:
        print(f"✅ 上传目录已存在: {upload_dir}")

def main():
    """主函数"""
    print("🚀 LightFileShare - 轻量化文件分享平台启动中...")
    
    # 初始化
    init_database()
    create_upload_dir()
    
    # 显示配置信息
    print(f"📋 配置信息:")
    print(f"   - 端口: {app.config['PORT']}")
    print(f"   - 主机: {app.config['HOST']}")
    print(f"   - 上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"   - 最大文件大小: {app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024):.2f} MB")
    print(f"   - 默认分享天数: {app.config['DEFAULT_SHARE_DAYS']} 天")
    print(f"   - 分享链接Host: {app.config['SHARE_HOST']}")
    
    print(f"\n🌐 服务地址: http://{app.config['HOST']}:{app.config['PORT']}")
    print("🔐 管理员密码: " + app.config['ADMIN_PASSWORD'])
    print("\n按 Ctrl+C 停止服务")
    
    # 启动uvicorn
    # 将Flask应用转换为ASGI应用
    asgi_app = WsgiToAsgi(app)
    uvicorn.run(
        asgi_app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        log_level="info",
        lifespan="off"  # 禁用lifespan协议以避免警告
    )

if __name__ == '__main__':
    main() 
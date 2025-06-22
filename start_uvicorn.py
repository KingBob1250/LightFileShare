#!/usr/bin/env python3
"""
使用uvicorn启动文件服务器
"""

import os
import sys
from app import app, db

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("✅ 数据库初始化完成")

def create_upload_dir():
    """创建上传目录"""
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print(f"✅ 创建上传目录: {upload_dir}")
    else:
        print(f"✅ 上传目录已存在: {upload_dir}")

def main():
    """主函数"""
    print("🚀 使用uvicorn启动文件服务器...")
    
    # 初始化
    init_database()
    create_upload_dir()
    
    # 显示配置信息
    print(f"📋 配置信息:")
    print(f"   - 端口: {app.config['PORT']}")
    print(f"   - 主机: {app.config['HOST']}")
    print(f"   - 上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"   - 最大文件大小: {app.config['MAX_CONTENT_LENGTH']} 字节")
    print(f"   - 默认分享天数: {app.config['DEFAULT_SHARE_DAYS']} 天")
    print(f"   - 分享链接Host: {app.config['SHARE_HOST']}")
    
    print(f"\n🌐 服务地址: http://{app.config['HOST']}:{app.config['PORT']}")
    print("🔐 管理员密码: " + app.config['ADMIN_PASSWORD'])
    print("\n按 Ctrl+C 停止服务")
    
    # 启动uvicorn
    try:
        import uvicorn
        from asgiref.wsgi import WsgiToAsgi
        
        # 将Flask应用转换为ASGI应用
        asgi_app = WsgiToAsgi(app)
        
        uvicorn.run(
            asgi_app,
            host=app.config['HOST'],
            port=app.config['PORT'],
            log_level="info"
        )
    except ImportError:
        print("❌ 错误: 未安装uvicorn或asgiref")
        print("请运行: pip install uvicorn asgiref")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

if __name__ == '__main__':
    main() 
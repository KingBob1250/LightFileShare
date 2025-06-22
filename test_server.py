#!/usr/bin/env python3
"""
文件服务器测试脚本
"""

import requests
import os
import tempfile
import time

def test_server():
    """测试服务器功能"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 开始测试文件服务器...")
    
    # 测试1: 检查服务器是否运行
    try:
        response = session.get(base_url, timeout=5)
        print("✅ 服务器运行正常")
    except requests.exceptions.RequestException as e:
        print(f"❌ 服务器连接失败: {e}")
        return False
    
    # 测试2: 登录
    login_data = {'password': 'admin123'}
    try:
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        if response.status_code == 302:  # 登录成功会重定向
            print("✅ 登录成功")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 登录请求失败: {e}")
        return False
    
    # 测试3: 创建测试文件
    test_content = "这是一个测试文件\n" * 100
    test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    test_file.write(test_content)
    test_file.close()
    
    print(f"📝 创建测试文件: {test_file.name}")
    
    try:
        # 测试4: 上传文件
        with open(test_file.name, 'rb') as f:
            files = {'file': f}
            response = session.post(f"{base_url}/upload", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            if upload_result.get('success'):
                print("✅ 文件上传成功")
            else:
                print(f"❌ 文件上传失败: {upload_result.get('error')}")
                return False
        else:
            print(f"❌ 文件上传请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
        
        # 测试5: 获取文件列表
        response = session.get(f"{base_url}/api/files")
        if response.status_code == 200:
            try:
                files_data = response.json()
                if files_data:
                    print(f"✅ 获取文件列表成功，共 {len(files_data)} 个文件")
                    test_file_info = files_data[0]  # 假设刚上传的文件在第一位
                else:
                    print("❌ 文件列表为空")
                    return False
            except requests.exceptions.JSONDecodeError as e:
                print(f"❌ 解析文件列表JSON失败: {e}")
                print(f"响应内容: {response.text}")
                return False
        else:
            print(f"❌ 获取文件列表失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
        
        # 测试6: 创建分享链接
        share_data = {
            'file_id': test_file_info['id'],
            'days': 1
        }
        response = session.post(f"{base_url}/share", json=share_data)
        
        if response.status_code == 200:
            try:
                share_result = response.json()
                if share_result.get('success'):
                    share_token = share_result.get('token')
                    share_url = share_result.get('share_url')
                    print(f"✅ 创建分享链接成功")
                    print(f"   Token: {share_token}")
                    print(f"   URL: {share_url}")
                    
                    # 测试7: 下载文件
                    download_url = f"{base_url}/download/{share_token}"
                    response = requests.get(download_url)
                    
                    if response.status_code == 200:
                        print("✅ 文件下载成功")
                    else:
                        print(f"❌ 文件下载失败: {response.status_code}")
                else:
                    print(f"❌ 创建分享链接失败: {share_result.get('error')}")
            except requests.exceptions.JSONDecodeError as e:
                print(f"❌ 解析分享链接JSON失败: {e}")
                print(f"响应内容: {response.text}")
        else:
            print(f"❌ 创建分享链接请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
        
    finally:
        # 清理测试文件
        os.unlink(test_file.name)
        print("🧹 清理测试文件")
    
    print("🎉 测试完成！")
    return True

if __name__ == '__main__':
    print("请确保文件服务器正在运行 (python start.py 或 python start_uvicorn.py)")
    print("然后运行此测试脚本")
    
    input("按回车键开始测试...")
    test_server() 
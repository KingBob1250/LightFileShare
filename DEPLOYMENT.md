# 文件服务器部署指南

## 启动方式对比

### 1. Flask开发服务器 (start.py)
```bash
python start.py
```
- **性能**: 单线程，适合开发测试
- **并发**: 不支持并发请求
- **生产环境**: ❌ 不推荐

### 2. Uvicorn ASGI服务器 (start_uvicorn.py)
```bash
python start_uvicorn.py
```
- **性能**: 异步，高并发
- **并发**: 支持大量并发请求
- **生产环境**: ✅ 推荐

### 3. 终端直接运行uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```
- **性能**: 与Python脚本中运行完全相同
- **并发**: 支持大量并发请求
- **生产环境**: ✅ 推荐

## 性能差异

| 启动方式 | 并发能力 | 性能 | 生产适用性 |
|---------|---------|------|-----------|
| Flask开发服务器 | 单线程 | 低 | ❌ |
| Uvicorn (脚本) | 异步 | 高 | ✅ |
| Uvicorn (终端) | 异步 | 高 | ✅ |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境变量配置

```bash
# 基础配置
export SECRET_KEY="your-secret-key"
export ADMIN_PASSWORD="your-password"

# 服务器配置
export HOST="0.0.0.0"
export PORT="5000"

# 文件上传配置
export MAX_CONTENT_LENGTH="104857600"
export ENABLE_FILE_TYPE_CHECK="false"  # 设置为true启用文件类型限制

# 分享链接配置
export SHARE_HOST="https://your-domain.com"
```

## 生产环境部署建议

1. **使用uvicorn启动**:
   ```bash
   python start_uvicorn.py
   ```

2. **配置反向代理** (Nginx):
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:5000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

3. **使用进程管理器** (systemd):
   ```ini
   [Unit]
   Description=File Server
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/file_server
   Environment=PATH=/path/to/venv/bin
   ExecStart=/path/to/venv/bin/python start_uvicorn.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 性能优化建议

1. **使用uvicorn而不是Flask开发服务器**
2. **配置适当的worker数量** (如果使用gunicorn+uvicorn)
3. **使用CDN加速静态文件**
4. **配置数据库连接池**
5. **启用文件压缩** 
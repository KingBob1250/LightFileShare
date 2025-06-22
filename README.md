# 文件服务器

一个轻量级的Python文件服务器，支持文件上传、分享和下载功能。

## 功能特性

- 🔐 **密码保护**：管理员密码登录
- 📁 **文件管理**：上传、删除、查看文件列表
- 🔗 **文件分享**：生成临时下载链接，支持设置有效期
- ⬇️ **断点续传**：支持大文件断点续传下载
- 🐳 **Docker部署**：一键部署，配置灵活
- 📱 **响应式界面**：支持移动端访问

## 快速开始

### 使用Docker部署（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd file_server
```

2. **配置环境变量**
```bash
cp env.example .env
# 编辑 .env 文件，修改管理员密码等配置
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问管理界面**
打开浏览器访问 `http://localhost:5000`，使用配置的密码登录。

### 本地开发

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置环境变量**
```bash
export ADMIN_PASSWORD=your_password
export PORT=5000
```

3. **启动服务**
```bash
python app.py
```

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 5000 | 服务端口 |
| `HOST` | 0.0.0.0 | 监听地址 |
| `ADMIN_PASSWORD` | admin123 | 管理员密码 |
| `UPLOAD_FOLDER` | uploads | 文件存储目录 |
| `MAX_CONTENT_LENGTH` | 104857600 | 最大文件大小（字节） |
| `DEFAULT_SHARE_DAYS` | 7 | 默认分享天数 |
| `SECRET_KEY` | dev-secret-key | 会话密钥 |

### 支持的文件类型

- 文档：txt, pdf, doc, docx, xls, xlsx, ppt, pptx
- 图片：png, jpg, jpeg, gif
- 压缩包：zip, rar, 7z
- 视频：mp4, avi, mkv, mov, wmv, flv, webm
- 音频：mp3

## 使用说明

### 管理员功能

1. **登录管理界面**
   - 访问 `http://localhost:5000`
   - 输入管理员密码登录

2. **上传文件**
   - 拖拽文件到上传区域或点击选择文件
   - 支持多文件同时上传
   - 显示上传进度

3. **管理文件**
   - 查看文件列表（文件名、大小、上传时间）
   - 搜索文件
   - 删除文件（需二次确认）

4. **分享文件**
   - 点击文件列表中的"分享"按钮
   - 选择分享天数（1-30天）
   - 生成临时下载链接
   - 复制链接分享给他人

### 下载功能

- 访问分享链接直接下载文件
- 支持断点续传
- 无需登录即可下载

## API接口

### 文件管理API

- `GET /api/files` - 获取文件列表
- `POST /upload` - 上传文件
- `DELETE /delete/<file_id>` - 删除文件

### 分享管理API

- `POST /share` - 创建分享链接
- `GET /api/shares` - 获取分享链接列表
- `DELETE /api/delete_share/<share_id>` - 删除分享链接

### 下载API

- `GET /download/<token>` - 下载分享的文件

## 部署说明

### Docker部署

```bash
# 构建镜像
docker build -t file-server .

# 运行容器
docker run -d \
  --name file-server \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/database.db:/app/database.db \
  -e ADMIN_PASSWORD=your_password \
  file-server
```

### 生产环境建议

1. **修改默认密码**：设置强密码
2. **配置HTTPS**：使用反向代理（如Nginx）
3. **数据备份**：定期备份数据库和文件
4. **监控日志**：配置日志收集和监控

## 项目结构

```
file_server/
├── app.py                 # 主应用文件
├── config.py              # 配置管理
├── models.py              # 数据模型
├── utils.py               # 工具函数
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像配置
├── docker-compose.yml    # Docker Compose配置
├── env.example           # 环境变量示例
├── templates/            # HTML模板
│   ├── base.html
│   ├── login.html
│   └── dashboard.html
├── uploads/              # 文件存储目录
└── README.md
```

## 技术栈

- **后端**：Flask + SQLAlchemy
- **数据库**：SQLite
- **前端**：原生HTML + CSS + JavaScript
- **部署**：Docker + Docker Compose

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
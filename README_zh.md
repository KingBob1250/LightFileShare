[English README](README.md)

# 🪶 LightFileShare

> **轻量化文件分享平台** | **Lightweight File Sharing Platform**

一个轻量级的Python文件服务器，支持文件上传、分享和下载功能。

## ✨ 功能特性

- 🔐 **密码保护**：管理员密码登录
- 📁 **文件管理**：上传、删除、查看文件列表
- 🔗 **文件分享**：生成临时下载链接，支持设置有效期
- 🛑 **停止分享**：单个或批量停止分享链接
- ⬇️ **断点续传**：支持大文件断点续传下载
- 📊 **访问统计**：统计分享链接的访问次数
- 👁️ **文件预览**：支持多种文件类型的在线预览
- 🐳 **Docker部署**：一键部署，配置灵活
- 📱 **响应式界面**：支持移动端访问
- 🔍 **文件搜索**：支持文件名搜索
- 📊 **批量操作**：支持批量删除、分享、下载
- 🌍 **多语言支持**：支持21种语言

## 🚀 快速开始

### 方法一：使用Docker（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/KingBob1250/LightFileShare.git
cd LightFileShare

# 2. 配置环境变量
cp env.example .env
# 编辑 .env 文件，修改管理员密码等配置

# 3. 启动服务（会自动构建镜像）
docker compose up -d

# 4. 访问管理界面
# 打开浏览器访问: http://localhost:5000
# 默认密码: admin123
```

**注意**：`docker compose up -d` 会自动构建镜像（如果不存在）。如果需要重新构建镜像，可以使用：
```bash
docker compose up -d --build
```

### 方法二：本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp env.example .env
# 编辑 .env 文件修改配置

# 3. 启动服务
python start_server.py

# 4. 访问管理界面
# 打开浏览器访问: http://localhost:5000
# 默认密码: admin123
```

## 📝 基本使用

1. **登录管理界面**
   - 访问 `http://localhost:5000`
   - 输入密码：`admin123`

2. **上传文件**
   - 拖拽文件到上传区域
   - 或点击"选择文件"按钮
   - 支持多文件同时上传

3. **管理文件**
   - 查看文件列表（文件名、大小、上传时间）
   - 搜索文件
   - 删除文件（需二次确认）
   - 批量操作（删除、分享、下载）

4. **预览文件**
   - 点击文件列表中的"预览"按钮
   - 支持多种文件类型预览：
     - **图片**：png, jpg, jpeg, gif, webp, svg
     - **文本**：txt, md, py, js, css, html, json, xml, sh, ini
     - **PDF**：pdf文件
     - **视频**：mp4, webm, mov
     - **音频**：mp3, ogg, wav
   - 文本文件支持语法高亮显示
   - 图片、视频、音频支持在线播放

5. **分享文件**
   - 点击文件列表中的"分享"按钮
   - 选择分享天数（1-30天）
   - 生成临时下载链接
   - 复制链接分享给他人

6. **管理分享**
   - 点击"分享管理"标签页查看所有分享链接
   - 查看分享状态、剩余时间、访问次数
   - 单个停止分享或批量停止分享
   - 复制分享链接

7. **下载文件**
   - 直接访问分享链接即可下载
   - 支持断点续传
   - 无需登录即可下载

## ⚙️ 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 5000 | 服务端口 |
| `HOST` | 0.0.0.0 | 监听地址 |
| `ADMIN_PASSWORD` | admin123 | 管理员密码 |
| `MAX_CONTENT_LENGTH` | 104857600 | 最大文件大小（字节） |
| `DEFAULT_SHARE_DAYS` | 7 | 默认分享天数 |
| `SECRET_KEY` | dev-secret-key | 会话密钥 |
| `ENABLE_FILE_TYPE_CHECK` | false | 是否启用文件类型检测 |
| `TIMEZONE` | Asia/Shanghai | 时区设置，支持标准时区名称 |

### 时区配置

系统支持多时区显示，确保不同时区的用户都能看到符合当地时区的时间。

#### 配置说明

**服务器端时区配置**（用于默认显示）：
- 在 `.env` 文件中设置 `TIMEZONE=Asia/Shanghai`
- 仅影响服务器端模板渲染的时间显示
- 不影响API接口返回的时间格式

**用户端时区检测**：
- 自动检测，无需配置
- 如果检测失败，使用服务器配置的默认时区
- 在页面顶部显示当前使用的时区信息

### 目录结构

```
LightFileShare/
├── app.py              # 主应用文件
├── config.py           # 配置文件
├── models.py           # 数据模型
├── utils.py            # 工具函数
├── start_server.py     # 启动脚本
├── requirements.txt    # Python依赖
├── docker-compose.yml  # Docker配置
├── Dockerfile          # Docker镜像配置
├── .env                # 环境变量（需要创建）
├── uploads/            # 文件上传目录（固定路径）
├── instance/           # 数据库目录（固定路径）
│   └── database.db     # SQLite数据库文件
├── translations/       # 国际化文件
│   ├── en/            # 英文翻译
│   └── zh/            # 中文翻译
└── templates/          # HTML模板
```

### 路径配置说明

**固定路径配置**：
- **数据库路径**：`./instance/database.db`（本地开发）或 `/app/instance/database.db`（Docker环境）
- **上传文件夹**：`./uploads`（本地开发）或 `/app/uploads`（Docker环境）

**Docker 路径映射**：
- 本地的 `./uploads` 目录 → 容器内的 `/app/uploads`
- 本地的 `./instance` 目录 → 容器内的 `/app/instance`

这些路径是固定的，无需通过环境变量配置。

### 文件类型检测

默认情况下，文件类型检测功能是**禁用**的（`ENABLE_FILE_TYPE_CHECK=false`），这意味着您可以上传任何类型的文件。

如果您想启用文件类型限制，可以设置 `ENABLE_FILE_TYPE_CHECK=true`，系统将只允许上传以下类型的文件：

- 文档：txt, pdf, doc, docx, xls, xlsx, ppt, pptx
- 图片：png, jpg, jpeg, gif
- 压缩包：zip, rar, 7z
- 音视频：mp3, mp4, avi, mkv, mov, wmv, flv, webm
- 其他：torrent, apk

### 文件预览功能

系统支持多种文件类型的在线预览功能，无需下载即可查看文件内容：

#### 支持预览的文件类型

- **图片文件**：png, jpg, jpeg, gif, webp, svg
- **文本文件**：txt, md, py, js, css, html, json, xml, sh, ini
- **PDF文件**：pdf
- **视频文件**：mp4, webm, mov
- **音频文件**：mp3, ogg, wav

#### 预览功能特点

- **文本文件**：支持语法高亮显示，使用Prism.js提供代码着色
- **图片文件**：支持缩放和自适应显示
- **视频/音频**：支持在线播放，带播放控制
- **PDF文件**：使用浏览器内置PDF查看器
- **模态框预览**：所有预览都在模态框中显示，不影响主界面

## 🌍 多语言支持

系统支持21种语言：

- 英语 (en)
- 简体中文 (zh)
- 繁体中文 (zh_TW)
- 西班牙语 (es)
- 阿拉伯语 (ar)
- 法语 (fr)
- 葡萄牙语 (pt)
- 俄语 (ru)
- 印地语 (hi)
- 日语 (ja)
- 韩语 (ko)
- 德语 (de)
- 土耳其语 (tr)
- 越南语 (vi)
- 泰语 (th)
- 乌克兰语 (uk)
- 印尼语 (id)
- 波兰语 (pl)
- 意大利语 (it)
- 波斯语 (fa)
- 马来语 (ms)

### 语言切换

- 系统自动检测浏览器语言设置
- 用户可以通过右上角的语言选择器手动切换语言
- 语言偏好保存在会话中
- 如果浏览器语言不支持，默认使用英语

## 🚀 部署指南

### 启动方式对比

| 启动方式 | 并发能力 | 性能 | 生产适用性 | 命令 |
|---------|---------|------|-----------|------|
| Flask开发服务器 | 单线程 | 低 | ❌ | `python app.py` |
| Uvicorn (脚本) | 异步 | 高 | ✅ | `python start_server.py` |
| Uvicorn (终端) | 异步 | 高 | ✅ | `uvicorn app:app --host 0.0.0.0 --port 5000` |

### Docker部署

#### 使用 Docker Compose（推荐）

```bash
# 1. 配置环境变量
cp env.example .env
# 编辑 .env 文件

# 2. 启动服务（自动构建镜像）
docker compose up -d

# 3. 查看日志
docker compose logs -f

# 4. 停止服务
docker compose down
```

#### 重要说明：.dockerignore 文件

项目包含 `.dockerignore` 文件，用于排除不需要复制到容器内部的文件和目录：

- **环境变量文件**：`.env`、`.env.local` 等
- **数据目录**：`uploads/`、`instance/`（通过 volumes 映射）
- **开发文件**：`.git/`、`__pycache__/`、IDE 配置文件等

**⚠️ 重要提醒**：如果您修改了 `docker-compose.yml` 中的 volumes 映射配置，请同时更新 `.dockerignore` 文件中的相应排除规则，确保数据目录不被复制到容器内部，避免数据冲突和镜像过大。

例如，如果您将 volumes 映射从 `./uploads:/app/uploads` 改为 `./data:/app/uploads`，那么需要在 `.dockerignore` 中将 `uploads/` 改为 `data/`。

## 🛑 停止服务

```bash
# Docker方式
docker compose down

# 本地运行
# 按 Ctrl+C 停止
```

## API接口

### 文件管理API

- `GET /api/files` - 获取文件列表
- `POST /upload` - 上传文件
- `DELETE /delete/<file_id>` - 删除文件
- `POST /api/batch_delete` - 批量删除文件
- `GET /api/search_files` - 搜索文件
- `GET /preview/<file_id>` - 预览文件

### 分享管理API

- `POST /share` - 创建分享链接
- `GET /api/shares` - 获取分享链接列表
- `DELETE /api/delete_share/<share_id>` - 删除分享链接
- `POST /api/batch_share` - 批量分享文件

### 下载API

- `GET /download/<token>` - 下载分享的文件
- `GET /download_file/<int:file_id>` - 管理员下载文件
- `GET /api/batch_download` - 批量下载文件

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

## 📞 支持

如果遇到问题或有疑问，请在GitHub上提交issue。

---

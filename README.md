[中文版 README](README_zh.md) 

# 🪶 LightFileShare

> **轻量化文件分享平台** | **Lightweight File Sharing Platform**

A lightweight Python file server with file upload, sharing, and download capabilities.

## ✨ Features

- 🔐 **Password Protection**: Administrator password login
- 📁 **File Management**: Upload, delete, view file list
- 🔗 **File Sharing**: Generate temporary download links with customizable expiration
- 🛑 **Stop Sharing**: Stop individual or batch share links
- ⬇️ **Resume Download**: Support for large file resume download
- 📊 **Access Statistics**: Track share link access counts
- 👁️ **File Preview**: Online preview for multiple file types
- 🐳 **Docker Deployment**: One-click deployment with flexible configuration
- 📱 **Responsive Interface**: Mobile-friendly access
- 🔍 **File Search**: File name search functionality
- 📊 **Batch Operations**: Support for batch delete, share, download
- 🌍 **Multi-language Support**: Support for 21 languages

![image](https://github.com/user-attachments/assets/b930dd68-2975-43f8-ab6a-f59556a0036d)
![image](https://github.com/user-attachments/assets/187d5c9f-c2f4-4f32-97e1-cffc06b4b0b7)

## 🚀 Quick Start

### Method 1: Using Docker (Recommended)

```bash
# 1. Clone the project
git clone https://github.com/KingBob1250/LightFileShare.git
cd LightFileShare

# 2. Configure environment variables
cp env.example .env
# Edit .env file to modify administrator password and other configurations

# 3. Start the service (will automatically build the image)
docker compose up -d

# 4. Access the management interface
# Open browser and visit: http://localhost:5000
# Default password: admin123
```

**Note**: `docker compose up -d` will automatically build the image (if it doesn't exist). If you need to rebuild the image, use:
```bash
docker compose up -d --build
```

### Method 2: Local Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment variables
cp env.example .env
# Edit .env file to modify configurations

# 3. Start the service
python start_server.py

# 4. Access the management interface
# Open browser and visit: http://localhost:5000
# Default password: admin123
```

## 📝 Basic Usage

1. **Login to Management Interface**
   - Visit `http://localhost:5000`
   - Enter password: `admin123`

2. **Upload Files**
   - Drag files to the upload area
   - Or click "Select Files" button
   - Support multiple file uploads

3. **Manage Files**
   - View file list (filename, size, upload time)
   - Search files
   - Delete files (requires confirmation)
   - Batch operations (delete, share, download)

4. **Preview Files**
   - Click "Preview" button in file list
   - Supports multiple file type previews:
     - **Images**: png, jpg, jpeg, gif, webp, svg
     - **Text**: txt, md, py, js, css, html, json, xml, sh, ini
     - **PDF**: pdf files
     - **Video**: mp4, webm, mov
     - **Audio**: mp3, ogg, wav
   - Text files support syntax highlighting
   - Images, videos, audio support online playback

5. **Share Files**
   - Click "Share" button in file list
   - Select share duration (1-30 days)
   - Generate temporary download links
   - Copy links to share with others

6. **Manage Shares**
   - Click "Share Management" tab to view all share links
   - View share status, remaining time, access count
   - Stop individual shares or batch stop shares
   - Copy share links

7. **Download Files**
   - Directly visit share links to download
   - Support resume download
   - No login required for downloads

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Service port |
| `HOST` | 0.0.0.0 | Listen address |
| `ADMIN_PASSWORD` | admin123 | Administrator password |
| `MAX_CONTENT_LENGTH` | 104857600 | Maximum file size (bytes) |
| `DEFAULT_SHARE_DAYS` | 7 | Default share days |
| `SECRET_KEY` | dev-secret-key | Session key |
| `ENABLE_FILE_TYPE_CHECK` | false | Enable file type detection |
| `TIMEZONE` | Asia/Shanghai | Timezone setting, supports standard timezone names |

### Timezone Configuration

The system supports multi-timezone display, ensuring users from different timezones can see times that match their local timezone.

#### Configuration Details

**Server-side Timezone Configuration** (for default display):
- Set `TIMEZONE=Asia/Shanghai` in `.env` file
- Only affects server-side template rendering time display
- Does not affect API interface returned time format

**Client-side Timezone Detection**:
- Automatic detection, no configuration needed
- If detection fails, uses server-configured default timezone
- Displays current timezone information at the top of the page

### Directory Structure

```
LightFileShare/
├── app.py              # Main application file
├── config.py           # Configuration file
├── models.py           # Data models
├── utils.py            # Utility functions
├── start_server.py     # Startup script
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker configuration
├── Dockerfile          # Docker image configuration
├── .env                # Environment variables (needs to be created)
├── uploads/            # File upload directory (fixed path)
├── instance/           # Database directory (fixed path)
│   └── database.db     # SQLite database file
├── translations/       # Internationalization files
│   ├── en/            # English translations
│   └── zh/            # Chinese translations
└── templates/          # HTML templates
```

### Path Configuration

**Fixed Path Configuration**:
- **Database Path**: `./instance/database.db` (local development) or `/app/instance/database.db` (Docker environment)
- **Upload Folder**: `./uploads` (local development) or `/app/uploads` (Docker environment)

**Docker Path Mapping**:
- Local `./uploads` directory → Container `/app/uploads`
- Local `./instance` directory → Container `/app/instance`

These paths are fixed and do not need to be configured through environment variables.

### File Type Detection

By default, file type detection is **disabled** (`ENABLE_FILE_TYPE_CHECK=false`), meaning you can upload any type of file.

If you want to enable file type restrictions, set `ENABLE_FILE_TYPE_CHECK=true`, and the system will only allow uploading the following file types:

- Documents: txt, pdf, doc, docx, xls, xlsx, ppt, pptx
- Images: png, jpg, jpeg, gif
- Archives: zip, rar, 7z
- Audio/Video: mp3, mp4, avi, mkv, mov, wmv, flv, webm
- Others: torrent, apk

### File Preview Feature

The system supports online preview for multiple file types without downloading:

#### Supported Preview File Types

- **Image Files**: png, jpg, jpeg, gif, webp, svg
- **Text Files**: txt, md, py, js, css, html, json, xml, sh, ini
- **PDF Files**: pdf
- **Video Files**: mp4, webm, mov
- **Audio Files**: mp3, ogg, wav

#### Preview Features

- **Text Files**: Support syntax highlighting using Prism.js for code coloring
- **Image Files**: Support zoom and adaptive display
- **Video/Audio**: Support online playback with playback controls
- **PDF Files**: Use browser built-in PDF viewer
- **Modal Preview**: All previews displayed in modal boxes without affecting main interface

## 🌍 Multi-language Support

The system supports 21 languages:

- English (en)
- Simplified Chinese (zh)
- Traditional Chinese (zh_TW)
- Spanish (es)
- Arabic (ar)
- French (fr)
- Portuguese (pt)
- Russian (ru)
- Hindi (hi)
- Japanese (ja)
- Korean (ko)
- German (de)
- Turkish (tr)
- Vietnamese (vi)
- Thai (th)
- Ukrainian (uk)
- Indonesian (id)
- Polish (pl)
- Italian (it)
- Persian (fa)
- Malay (ms)

### Language Switching

- The system automatically detects browser language settings
- Users can manually switch languages using the language selector in the top-right corner
- Language preferences are saved in session
- If the browser language is not supported, English is used as default

## 🚀 Deployment Guide

### Startup Method Comparison

| Startup Method | Concurrency | Performance | Production Ready | Command |
|---------------|-------------|-------------|------------------|---------|
| Flask Dev Server | Single-threaded | Low | ❌ | `python app.py` |
| Uvicorn (Script) | Async | High | ✅ | `python start_server.py` |
| Uvicorn (Terminal) | Async | High | ✅ | `uvicorn app:app --host 0.0.0.0 --port 5000` |

### Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# 1. Configure environment variables
cp env.example .env
# Edit .env file

# 2. Start service (auto-build image)
docker compose up -d

# 3. View logs
docker compose logs -f

# 4. Stop service
docker compose down
```

#### Important Note: .dockerignore File

The project includes a `.dockerignore` file to exclude unnecessary files and directories from being copied into the container:

- **Environment files**: `.env`, `.env.local`, etc.
- **Data directories**: `uploads/`, `instance/` (mapped via volumes)
- **Development files**: `.git/`, `__pycache__/`, IDE config files, etc.

**⚠️ Important Reminder**: If you modify the volumes mapping configuration in `docker-compose.yml`, please also update the corresponding exclusion rules in the `.dockerignore` file to ensure data directories are not copied into the container, avoiding data conflicts and large image sizes.

For example, if you change the volumes mapping from `./uploads:/app/uploads` to `./data:/app/uploads`, you need to change `uploads/` to `data/` in `.dockerignore`.

## 🛑 Stop Service

```bash
# Docker method
docker compose down

# Local run
# Press Ctrl+C to stop
```

## API Interfaces

### File Management APIs

- `GET /api/files` - Get file list
- `POST /upload` - Upload file
- `DELETE /delete/<file_id>` - Delete file
- `POST /api/batch_delete` - Batch delete files
- `GET /api/search_files` - Search files
- `GET /preview/<file_id>` - Preview file

### Share Management APIs

- `POST /share` - Create share link
- `GET /api/shares` - Get share link list
- `DELETE /api/delete_share/<share_id>` - Delete share link
- `POST /api/batch_share` - Batch share files

### Download APIs

- `GET /download/<token>` - Download shared file
- `GET /download_file/<int:file_id>` - Admin download file
- `GET /api/batch_download` - Batch download files

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---


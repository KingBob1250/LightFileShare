# 快速启动指南

## 🚀 立即开始

### 方法一：使用Docker（推荐）

```bash
# 1. 启动服务
docker-compose up -d

# 2. 访问管理界面
# 打开浏览器访问: http://localhost:5000
# 默认密码: admin123
```

### 方法二：本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python start.py

# 3. 访问管理界面
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

3. **分享文件**
   - 点击文件列表中的"分享"按钮
   - 选择分享天数
   - 复制生成的下载链接

4. **下载文件**
   - 直接访问分享链接即可下载
   - 支持断点续传

## ⚙️ 自定义配置

复制环境变量文件并修改：

```bash
cp env.example .env
# 编辑 .env 文件修改配置
```

主要配置项：
- `ADMIN_PASSWORD`: 管理员密码
- `PORT`: 服务端口
- `MAX_CONTENT_LENGTH`: 最大文件大小

## 🧪 测试功能

```bash
# 运行测试脚本
python test_server.py
```

## 🛑 停止服务

```bash
# Docker方式
docker-compose down

# 本地运行
# 按 Ctrl+C 停止
```

## 📁 文件存储

- 上传的文件保存在 `uploads/` 目录
- 数据库文件：`database.db`
- 日志：查看控制台输出

## 🔧 故障排除

1. **端口被占用**
   - 修改 `PORT` 环境变量
   - 或停止占用端口的其他服务

2. **权限问题**
   - 确保对 `uploads/` 目录有写权限
   - Docker用户确保卷挂载正确

3. **数据库问题**
   - 删除 `database.db` 文件重新初始化
   - 检查磁盘空间是否充足

## 📞 获取帮助

- 查看完整文档：`README.md`
- 检查日志输出
- 运行测试脚本验证功能 
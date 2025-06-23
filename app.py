from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_babel import Babel, gettext as _, ngettext, get_locale
import os
import uuid
from datetime import datetime, timezone
from functools import wraps
import json
import mimetypes
from dotenv import load_dotenv
import pytz
import subprocess
from pathlib import Path

# 加载 .env 文件中的环境变量
load_dotenv()

from config import Config
from models import db, File, ShareLink
from utils import allowed_file, safe_filename, send_file_with_range, cleanup_expired_shares

def compile_translations_if_needed():
    """如果需要，编译翻译文件"""
    translations_dir = Path("translations")
    
    if not translations_dir.exists():
        return
    
    # 检查是否需要编译
    po_files = list(translations_dir.rglob("*.po"))
    mo_files = list(translations_dir.rglob("*.mo"))
    
    # 如果没有 .mo 文件，或者 .po 文件比 .mo 文件新，则需要编译
    if not mo_files or any(
        po_file.stat().st_mtime > mo_file.stat().st_mtime 
        for po_file in po_files 
        for mo_file in mo_files
    ):
        print("检测到翻译文件需要编译...")
        try:
            # 编译所有语言
            for po_file in po_files:
                lang = po_file.parent.parent.name
                subprocess.run([
                    "pybabel", "compile", 
                    "-d", "translations", 
                    "-l", lang
                ], check=True, capture_output=True)
            print("翻译文件编译完成")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"翻译文件编译失败: {e}")
            # 编译失败不影响应用启动

app = Flask(__name__)
app.config.from_object(Config)

# 在应用启动时编译翻译文件
compile_translations_if_needed()

# 初始化Babel
babel = Babel(app)

# 初始化数据库
db.init_app(app)

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh': '简体中文',
    'zh_TW': '繁體中文',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'ja': '日本語',
    'ko': '한국어',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'th': 'ไทย',
    'vi': 'Tiếng Việt',
    'tr': 'Türkçe',
    'uk': 'Українська',
    'id': 'Bahasa Indonesia',
    'ms': 'Bahasa Melayu',
    'fa': 'فارسی',
    'pl': 'Polski'
}

def get_locale():
    """获取用户语言设置"""
    # 首先检查session中的语言设置
    if 'language' in session:
        lang = session['language']
        if lang in SUPPORTED_LANGUAGES:
            return lang
    
    # 然后检查请求参数中的语言设置
    lang = request.args.get('lang')
    if lang and lang in SUPPORTED_LANGUAGES:
        session['language'] = lang
        return lang
    
    # 最后使用浏览器语言设置，如果都不支持则使用英文
    browser_lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys(), default='en')
    # 将检测到的语言保存到session中
    session['language'] = browser_lang
    return browser_lang

# 设置 Babel 的语言选择器
babel.init_app(app, locale_selector=get_locale)

def get_local_timezone():
    """获取本地时区"""
    return app.config.get('TIMEZONE', 'Asia/Shanghai')

def convert_to_local_time(utc_time, timezone_str=None):
    """将UTC时间转换为本地时间"""
    if not utc_time:
        return utc_time
    
    if timezone_str is None:
        timezone_str = get_local_timezone()
    
    try:
        tz = pytz.timezone(timezone_str)
        if utc_time.tzinfo is None:
            utc_time = pytz.utc.localize(utc_time)
        return utc_time.astimezone(tz)
    except:
        return utc_time

def format_local_time(utc_time, timezone_str=None, format_str='%Y-%m-%d %H:%M:%S'):
    """格式化本地时间显示"""
    local_time = convert_to_local_time(utc_time, timezone_str)
    return local_time.strftime(format_str)

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """首页重定向到登录"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=_('Wrong password'), supported_languages=SUPPORTED_LANGUAGES)
    
    return render_template('login.html', supported_languages=SUPPORTED_LANGUAGES)

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/set_language/<language>')
def set_language(language):
    """设置语言"""
    if language in SUPPORTED_LANGUAGES:
        session['language'] = language
    return redirect(request.referrer or url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """管理面板"""
    # 清理过期的分享链接
    cleanup_expired_shares()
    
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)  # 每页显示20个文件
    
    # 获取所有文件（分页）
    pagination = File.query.order_by(File.upload_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    files = pagination.items
    
    message = request.args.get('message')
    error = request.args.get('error')
    
    return render_template('dashboard.html', 
                         files=files, 
                         pagination=pagination,
                         message=message, 
                         error=error,
                         share_host=app.config['SHARE_HOST'],
                         timezone=get_local_timezone(),
                         supported_languages=SUPPORTED_LANGUAGES)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """文件上传"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    if file and allowed_file(file.filename, enable_check=app.config['ENABLE_FILE_TYPE_CHECK']):
        # 生成安全的文件名
        original_filename = file.filename
        filename = safe_filename(file.filename)
        
        # 如果文件名已存在，添加随机后缀
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 保存文件信息到数据库
        file_record = File(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path)
        )
        
        db.session.add(file_record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '文件上传成功'})
    
    # 不支持的文件类型
    if file.filename and '.' in file.filename:
        file_extension = file.filename.rsplit('.', 1)[1].lower()
    else:
        file_extension = '未知'
    return jsonify({'success': False, 'error': f'不支持的文件类型: .{file_extension}'})

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    """删除文件"""
    file_record = File.query.get_or_404(file_id)
    
    try:
        # 删除物理文件
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 删除数据库记录
        db.session.delete(file_record)
        db.session.commit()
        
        return redirect(url_for('dashboard', message='文件删除成功'))
    except Exception as e:
        return redirect(url_for('dashboard', error=f'删除文件失败: {str(e)}'))

@app.route('/share', methods=['POST'])
@login_required
def share_file():
    """创建分享链接"""
    data = request.get_json()
    file_id = data.get('file_id')
    days = data.get('days', 7)
    
    file_record = File.query.get_or_404(file_id)
    
    try:
        # 创建分享链接
        share_link = ShareLink.create_share_link(file_id, days)
        
        return jsonify({
            'success': True,
            'token': share_link.token,
            'share_url': f"{app.config['SHARE_HOST']}/download/{share_link.token}",
            'filename': file_record.original_filename,
            'message': '分享链接创建成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建分享链接失败: {str(e)}'
        })

@app.route('/download/<token>')
def download_file(token):
    """下载分享的文件"""
    # 查找分享链接
    share_link = ShareLink.query.filter_by(token=token).first()
    
    if not share_link:
        return "分享链接不存在或已过期", 404
    
    if share_link.is_expired:
        return "分享链接已过期", 410
    
    # 获取文件信息
    file_record = share_link.file
    
    if not file_record or not os.path.exists(file_record.file_path):
        return "文件不存在", 404
    
    # 增加下载次数（在发送文件前）
    share_link.download_count += 1
    db.session.commit()
    
    # 返回文件（支持断点续传）
    return send_file_with_range(file_record.file_path, file_record.original_filename)

@app.route('/api/files')
@login_required
def api_files():
    """API: 获取文件列表"""
    files = File.query.order_by(File.upload_time.desc()).all()
    return jsonify([{
        'id': f.id,
        'filename': f.original_filename,
        'size': f.file_size,
        'size_human': f.file_size_human,
        'upload_time_utc': f.upload_time.isoformat() + 'Z',  # UTC时间戳
        'shares': [{
            'token': s.token,
            'expire_time_utc': s.expire_time.isoformat() + 'Z',  # UTC时间戳
            'is_expired': s.is_expired,
            'days_remaining': s.days_remaining
        } for s in f.shares if not s.is_expired]
    } for f in files])

@app.route('/api/shares')
@login_required
def api_shares():
    """API: 获取分享链接列表"""
    current_utc = datetime.now(timezone.utc)
    shares = ShareLink.query.filter(ShareLink.expire_time > current_utc).all()
    return jsonify([{
        'id': s.id,
        'token': s.token,
        'filename': s.file.original_filename,
        'created_time_utc': s.created_time.isoformat() + 'Z',  # UTC时间戳
        'expire_time_utc': s.expire_time.isoformat() + 'Z',  # UTC时间戳
        'days_remaining': s.days_remaining,
        'download_count': s.download_count
    } for s in shares])

@app.route('/api/delete_share/<int:share_id>', methods=['DELETE'])
@login_required
def api_delete_share(share_id):
    """API: 删除分享链接"""
    share = ShareLink.query.get_or_404(share_id)
    db.session.delete(share)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/download_file/<int:file_id>')
@login_required
def download_file_admin(file_id):
    """管理员下载文件（需要登录验证）"""
    file_record = File.query.get_or_404(file_id)
    
    if not os.path.exists(file_record.file_path):
        return "文件不存在", 404
    
    # 返回文件（支持断点续传）
    return send_file_with_range(file_record.file_path, file_record.original_filename)

@app.route('/api/search_files')
@login_required
def search_files():
    """API: 搜索文件（支持分页和排序）"""
    # 获取搜索参数
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'upload_time')
    sort_order = request.args.get('sort_order', 'desc')

    # 基础查询
    files_query = File.query

    # 应用搜索过滤器
    if query:
        search_filter = File.original_filename.ilike(f'%{query}%')
        files_query = files_query.filter(search_filter)
    
    # 应用排序
    if sort_by == 'share_status':
        # 按分享状态排序：计算每个文件有效的分享链接数
        current_utc = datetime.now(timezone.utc)
        active_shares_subquery = db.session.query(
            ShareLink.file_id,
            db.func.count(ShareLink.id).label('active_shares_count')
        ).filter(ShareLink.expire_time > current_utc).group_by(ShareLink.file_id).subquery()

        files_query = files_query.outerjoin(
            active_shares_subquery, File.id == active_shares_subquery.c.file_id
        )
        order_expression = db.func.coalesce(active_shares_subquery.c.active_shares_count, 0)
        
        if sort_order == 'desc':
            files_query = files_query.order_by(order_expression.desc())
        else:
            files_query = files_query.order_by(order_expression.asc())
            
    elif sort_by in ['original_filename', 'file_size', 'upload_time']:
        sort_column = getattr(File, sort_by)
        if sort_order == 'desc':
            files_query = files_query.order_by(sort_column.desc())
        else:
            files_query = files_query.order_by(sort_column.asc())
    
    # 添加第二排序，确保顺序稳定
    if sort_by != 'upload_time':
        files_query = files_query.order_by(File.upload_time.desc())
    else: # 如果按上传时间排序，则按ID进行第二排序
        files_query = files_query.order_by(File.id.desc())

    # 分页
    pagination = files_query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 构建响应数据
    files_data = []
    for file in pagination.items:
        file_data = {
            'id': file.id,
            'filename': file.original_filename,
            'size': file.file_size,
            'size_human': file.file_size_human,
            'upload_time_utc': file.upload_time.isoformat() + 'Z',  # UTC时间戳
            'shares': []
        }
        
        # 添加有效的分享链接
        for share in file.shares:
            if not share.is_expired:
                file_data['shares'].append({
                    'token': share.token,
                    'expire_time_utc': share.expire_time.isoformat() + 'Z',  # UTC时间戳
                    'is_expired': share.is_expired,
                    'days_remaining': share.days_remaining
                })
        
        files_data.append(file_data)
    
    return jsonify({
        'files': files_data,
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num
        }
    })

@app.route('/api/batch_delete', methods=['POST'])
@login_required
def batch_delete():
    """API: 批量删除文件"""
    data = request.get_json()
    file_ids = data.get('file_ids', [])
    
    if not file_ids:
        return jsonify({'success': False, 'error': '请选择要删除的文件'})
    
    deleted_count = 0
    failed_files = []
    
    for file_id in file_ids:
        try:
            file_record = File.query.get(file_id)
            if file_record:
                # 删除物理文件
                if os.path.exists(file_record.file_path):
                    os.remove(file_record.file_path)
                
                # 删除数据库记录
                db.session.delete(file_record)
                deleted_count += 1
            else:
                failed_files.append(f"文件ID {file_id} 不存在")
        except Exception as e:
            failed_files.append(f"文件ID {file_id}: {str(e)}")
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'failed_files': failed_files,
            'message': f'成功删除 {deleted_count} 个文件'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'批量删除失败: {str(e)}'})

@app.route('/api/batch_share', methods=['POST'])
@login_required
def batch_share():
    """API: 批量分享文件"""
    data = request.get_json()
    file_ids = data.get('file_ids', [])
    days = data.get('days', 7)
    
    if not file_ids:
        return jsonify({'success': False, 'error': '请选择要分享的文件'})
    
    shared_count = 0
    failed_files = []
    share_links = []
    
    for file_id in file_ids:
        try:
            file_record = File.query.get(file_id)
            if file_record:
                # 创建分享链接
                share_link = ShareLink.create_share_link(file_id, days)
                shared_count += 1
                
                share_links.append({
                    'file_id': file_id,
                    'filename': file_record.original_filename,
                    'share_url': f"{app.config['SHARE_HOST']}/download/{share_link.token}",
                    'token': share_link.token
                })
            else:
                failed_files.append(f"文件ID {file_id} 不存在")
        except Exception as e:
            failed_files.append(f"文件ID {file_id}: {str(e)}")
    
    return jsonify({
        'success': True,
        'shared_count': shared_count,
        'failed_files': failed_files,
        'share_links': share_links,
        'message': f'成功分享 {shared_count} 个文件'
    })

@app.route('/api/batch_download')
@login_required
def batch_download():
    """API: 批量下载文件（创建ZIP包）"""
    file_ids_str = request.args.get('file_ids', '')
    
    if not file_ids_str:
        return jsonify({'success': False, 'error': '请选择要下载的文件'})
    
    try:
        file_ids = json.loads(file_ids_str)
    except:
        return jsonify({'success': False, 'error': '文件ID格式错误'})
    
    if not file_ids:
        return jsonify({'success': False, 'error': '请选择要下载的文件'})
    
    import zipfile
    from io import BytesIO
    
    # 创建临时ZIP文件
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        added_count = 0
        for file_id in file_ids:
            try:
                file_record = File.query.get(file_id)
                if file_record and os.path.exists(file_record.file_path):
                    # 添加到ZIP文件
                    zip_file.write(file_record.file_path, file_record.original_filename)
                    added_count += 1
            except Exception as e:
                continue
        
        if added_count == 0:
            return jsonify({'success': False, 'error': '没有找到可下载的文件'})
    
    zip_buffer.seek(0)
    
    # 生成ZIP文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'files_{timestamp}.zip'
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_filename
    )

@app.route('/preview/<int:file_id>')
@login_required
def preview_file(file_id):
    """文件预览"""
    file_record = File.query.get_or_404(file_id)

    if not os.path.exists(file_record.file_path):
        return "文件不存在", 404

    ext = file_record.original_filename.rsplit('.', 1)[-1].lower()
    
    # 文本类型预览
    if ext in app.config['PREVIEWABLE_EXTENSIONS']['text']:
        try:
            with open(file_record.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template('preview_text.html', content=content, lang=ext)
        except Exception as e:
            return f"无法预览文件: {e}", 500
    
    # 其他类型直接发送文件
    mimetype = mimetypes.guess_type(file_record.original_filename)[0] or 'application/octet-stream'
    
    return send_file(file_record.file_path, mimetype=mimetype)

@app.errorhandler(404)
def not_found(error):
    return "页面不存在", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "服务器内部错误", 500

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=False
    ) 
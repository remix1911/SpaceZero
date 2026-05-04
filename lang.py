# 多语言配置文件
# 支持中文和英文自动切换

# 中文翻译
zh_CN = {
    "title": "SpaceZero",
    "scan_path": "扫描路径:",
    "browse": "浏览",
    "temp_files": "临时文件",
    "log_files": "日志文件",
    "cache_files": "缓存文件",
    "start_scan": "开始扫描",
    "stop_scan": "停止扫描",
    "select_all": "全选",
    "deselect_all": "取消全选",
    "clean_selected": "清理选中文件",
    "about": "关于软件",
    "found_files": "发现文件:",
    "total_size": "总大小:",
    "scan_complete": "扫描完成",
    "warning_select": "请选择文件",
    "confirm_delete": "确定将 {} 个文件移到回收站？",
    "clean_complete": "清理完成",
    "success_delete": "成功删除 {} 个文件",
    "failed_delete": "以下 {} 个文件未能删除:",
    "file_not_found": "文件不存在",
    "permission_denied": "权限不足",
    "file_in_use": "正在被其他程序占用",
    "delete_failed": "删除失败: {}",
    "disclaimer_title": "用户协议与免责声明",
    "disclaimer_content": "本工具为个人独立开发的免费系统优化辅助软件，所有操作均在本地设备完成，不会收集、上传、泄露用户个人隐私信息，请放心使用。\n\n免责声明\n本软件为个人独立开发的免费系统辅助工具，仅供个人学习与日常维护使用。所有清理、优化操作均由用户手动确认后执行，操作决策权归用户所有。因用户误操作、自行强制删除文件所造成的文件丢失、系统故障等后果，本开发者不承担相关责任。本软件仅在本地执行操作，不收集、不上传、不泄露用户隐私数据。",
    "agree": "同意",
    "disagree": "不同意",
    "about_title": "关于软件",
    "about_content": "SpaceZero v1.0.0\n\n本工具为个人独立开发的免费系统优化辅助软件，所有操作均在本地设备完成，不会收集、上传、泄露用户隐私信息，请放心使用。\n\n免责声明\n本软件为个人独立开发的免费系统辅助工具，仅供个人学习与日常维护使用。所有清理、优化操作均由用户手动确认后执行，操作决策权归用户所有。因用户误操作、自行强制删除文件所造成的文件丢失、系统故障等后果，本开发者不承担相关责任。本软件仅在本地执行操作，不收集、不上传、不泄露用户隐私数据。",
    "close": "关闭"
}

# 英文翻译
en_US = {
    "title": "SpaceZero",
    "scan_path": "Scan Path:",
    "browse": "Browse",
    "temp_files": "Temp Files",
    "log_files": "Log Files",
    "cache_files": "Cache Files",
    "start_scan": "Start Scan",
    "stop_scan": "Stop Scan",
    "select_all": "Select All",
    "deselect_all": "Deselect All",
    "clean_selected": "Clean Selected",
    "about": "About",
    "found_files": "Found Files:",
    "total_size": "Total Size:",
    "scan_complete": "Scan Complete",
    "warning_select": "Please select files",
    "confirm_delete": "Move {} files to Recycle Bin?",
    "clean_complete": "Clean Complete",
    "success_delete": "Successfully deleted {} files",
    "failed_delete": "Failed to delete {} files:",
    "file_not_found": "File not found",
    "permission_denied": "Permission denied",
    "file_in_use": "File in use by another process",
    "delete_failed": "Delete failed: {}",
    "disclaimer_title": "User Agreement & Disclaimer",
    "disclaimer_content": "This tool is a free system optimization software developed by an individual. All operations are performed locally and will not collect, upload, or disclose user personal privacy information. Please feel free to use it.\n\nDisclaimer\nThis software is a free system utility tool developed by an individual, for personal learning and daily maintenance use only. All cleaning and optimization operations are executed after manual confirmation by the user, and the decision-making power belongs to the user. The developer is not responsible for any consequences such as file loss or system failure caused by user's misoperation or forced file deletion. This software only performs operations locally and does not collect, upload, or disclose user privacy data.",
    "agree": "Agree",
    "disagree": "Disagree",
    "about_title": "About",
    "about_content": "SpaceZero v1.0.0\n\nThis tool is a free system optimization software developed by an individual. All operations are performed locally and will not collect, upload, or disclose user personal privacy information. Please feel free to use it.\n\nDisclaimer\nThis software is a free system utility tool developed by an individual, for personal learning and daily maintenance use only. All cleaning and optimization operations are executed after manual confirmation by the user, and the decision-making power belongs to the user. The developer is not responsible for any consequences such as file loss or system failure caused by user's misoperation or forced file deletion. This software only performs operations locally and does not collect, upload, or disclose user privacy data.",
    "close": "Close"
}

def get_language():
    """根据系统语言返回对应的语言字典"""
    import locale
    try:
        lang_code, _ = locale.getdefaultlocale()
        if lang_code and lang_code.startswith('zh'):
            return zh_CN
        else:
            return en_US
    except:
        return en_US

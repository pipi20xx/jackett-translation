import os
import shutil
import sys
import importlib.util
from loguru import logger

def setup_work_dir():
    """准备 2.trans.py 所需的目录结构"""
    root = os.getcwd()
    src_content = os.path.join(root, "Content")
    src_defs = os.path.join(root, "Definitions")
    
    # 检查本地资源
    if not os.path.exists(src_content):
        logger.error("错误: 根目录下缺少 'Content' 文件夹")
        return False
    if not os.path.exists(src_defs):
        logger.error("错误: 根目录下缺少 'Definitions' 文件夹")
        return False

    from settings import BASE_FOLDER
    # 构造 2.trans.py 期待的结构: BASE_FOLDER/Jackett-src/src/Jackett.Common/
    base_path = os.path.join(BASE_FOLDER, "Jackett-src")
    common_path = os.path.join(base_path, "src", "Jackett.Common")
    
    if os.path.exists(BASE_FOLDER):
        logger.info(f"清理旧的工作目录: {BASE_FOLDER}")
        shutil.rmtree(BASE_FOLDER)
    
    os.makedirs(common_path, exist_ok=True)
    
    # 复制资源
    logger.info(f"正在准备 Content...")
    shutil.copytree(src_content, os.path.join(common_path, "Content"))
    
    logger.info(f"正在准备 Definitions...")
    # 确保复制的是文件夹里的内容
    shutil.copytree(src_defs, os.path.join(common_path, "Definitions"))
    
    # 检查一下是否真的进去了
    defs_count = len(os.listdir(os.path.join(common_path, "Definitions")))
    logger.info(f"工作目录准备就绪，包含 {defs_count} 个定义文件。")
    return True

def run_project_script(script_name):
    """动态加载并运行项目中的脚本"""
    logger.info(f"开始执行项目核心脚本: {script_name}")
    spec = importlib.util.spec_from_file_location("module.name", script_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)

def main():
    print("=== Jackett 汉化本地一键处理入口 ===")
    
    # 1. 自动准备环境
    if not setup_work_dir():
        return

    # 2. 调用项目原有的翻译脚本 (2.trans.py)
    try:
        run_project_script("2.trans.py")
        
        from settings import PATCH_FOLDER
        print(f"\n[成功] 汉化已完成！")
        print(f"请在以下目录查看生成的补丁文件: {PATCH_FOLDER}")
        
    except Exception as e:
        logger.exception(f"运行过程中出现错误: {e}")
    
    print("\n" + "="*40)
    input("处理完成。请检查上方的日志信息。\n按回车键退出程序...")

if __name__ == "__main__":
    main()

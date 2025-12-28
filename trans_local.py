import os
import re
import shutil
from pathlib import Path
from loguru import logger

# 尝试导入项目依赖
try:
    from translations import translation_dict
except ImportError:
    print("错误: 请确保 translations.py 在当前目录下。")
    exit(1)

# 编译正则表达式用于匹配 [[...]] 格式
pat = re.compile('[[.*]]', flags=re.DOTALL + re.MULTILINE)

def translate(m):
    trans = translation_dict.get(m.group(1), m.group(1))
    return trans if trans else m.group(1)

def make_parent_folder(output_path):
    parent_folder = Path(output_path).parent.absolute()
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

def replace_in_file(file_path, translation, output_path):
    if not os.path.exists(file_path):
        logger.warning(f"跳过: 文件未找到 {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for ori_mark in translation:
        ori_content = ori_mark.replace('[[', '').replace(']]', '')
        trans = pat.sub(translate, ori_mark)
        content = content.replace(ori_content, trans)

    make_parent_folder(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"已处理: {output_path}")

def mass_trans_yml(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        res = re.findall('^type: (.*)', content, re.MULTILINE)
        for x in res:
            try:
                content = re.sub('^type: ' + x, 'type: ' + translation_dict[x], content, flags=re.MULTILINE | re.DOTALL)
            except:
                pass
        return content

def load_js(js_file_path, indent):
    if not os.path.exists(js_file_path):
        return ""
    with open(js_file_path, 'r', encoding='utf-8') as f:
        res = '\n'
        for line in f:
            res += ' ' * indent + line
        return res

def main():
    root = os.getcwd()
    src_content = os.path.join(root, "Content")
    src_defs = os.path.join(root, "Definitions")
    output_root = os.path.join(root, "Jackett-CN-Patch")

    if not os.path.exists(src_content) or not os.path.exists(src_defs):
        print("错误: 请确保根目录下存在 'Content' 和 'Definitions' 文件夹。")
        return

    if os.path.exists(output_root):
        shutil.rmtree(output_root)
    os.makedirs(output_root)

    # 1. 处理 Content 目录下的关键文件
    content_tasks = {
        "custom.js": [
            '>[[Show all]]<', '>[[Click here to open an issue on GitHub for this indexer.]]<',
            '>[[NO UPLOAD]]<', '>[[ Show dead torrents]]<',
            '[[Search query consists of several keywords.\nKeyword starting with \
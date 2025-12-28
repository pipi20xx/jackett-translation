# 警告! 文件夹的内容可能会被删除, 请确保路径没有重要文件
# WARNING! folders may get deleted during the execution
# make sure the folders not containing anything important!

# 路径结尾的斜杠不能省略
# ending slash in folders can NOT be omitted

import os
import platform

# DEBUG = False
DEBUG = False

if 'GITHUB_ACTIONS' in os.environ:

    # Github Action 环境
    # Github Action Environment
    BASE_FOLDER = f'{os.getcwd()}/Jackett-trans/'
    PATCH_FOLDER = f'{os.getcwd()}/Jackett-trans-patch/'
    TRANS_RELEASE_FOLDER = f'{os.getcwd()}/Jackett-trans-release/'
    USE_PROXY = False
    PROXIES = {}

else:

    # 自动获取当前目录作为根目录
    current_dir = os.getcwd()

    if platform.system() == 'Linux' and os.path.exists('/home/nate/soft/Jackett/'):
        # 原作者的 Linux 路径
        BASE_FOLDER = '/home/nate/soft/Jackett/Jackett-trans/'
        PATCH_FOLDER = '/home/nate/soft/Jackett/Jackett-trans-patch/'
        TRANS_RELEASE_FOLDER = '/home/nate/soft/Jackett/Jackett-trans-release/'
    elif platform.system() == 'Darwin' and os.path.exists('/Users/nate/soft/Jackett/'):
        # 原作者的 MacOS 路径
        BASE_FOLDER = '/Users/nate/soft/Jackett/Jackett-trans/'
        PATCH_FOLDER = '/Users/nate/soft/Jackett/Jackett-trans-patch/'
        TRANS_RELEASE_FOLDER = '/Users/nate/soft/Jackett/Jackett-trans-release/'
    else:
        # 默认使用当前文件夹下的相对路径，方便其他人使用
        BASE_FOLDER = os.path.join(current_dir, 'work_dir/')
        PATCH_FOLDER = os.path.join(current_dir, 'Jackett-CN-Patch/')
        TRANS_RELEASE_FOLDER = os.path.join(current_dir, 'Jackett-Release/')

    # 确保目录结尾有斜杠（保持原有逻辑一致性）
    if not BASE_FOLDER.endswith(os.sep): BASE_FOLDER += os.sep
    if not PATCH_FOLDER.endswith(os.sep): PATCH_FOLDER += os.sep
    if not TRANS_RELEASE_FOLDER.endswith(os.sep): TRANS_RELEASE_FOLDER += os.sep

    # 连不到GitHub需要设置代理 USE_PROXY=False 不会用代理
    # Change following proxy setting if you need proxy to connect to GitHub. set USE_PROXY=False can ignore it.
    # USE_PROXY = True
    USE_PROXY = False
    PROXIES = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809"
    }

# release文件名后缀
# release file name suffix
LANG = 'cn'

# 翻译者信息, 会在关于页面显示
# translator info, will be in about page
TRANSLATOR = 'Nriver'
TRANSLATOR_URL = 'https://github.com/Nriver/Jackett-translation'

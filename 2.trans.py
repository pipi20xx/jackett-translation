import os
import platform
import re
import shutil
from pathlib import Path
from loguru import logger

from settings import BASE_FOLDER, PATCH_FOLDER, TRANSLATOR, TRANSLATOR_URL, LANG
from translations import translation_dict

script_path = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = os.path.join(BASE_FOLDER, 'Jackett-src/')
# os.chdir(BASE_PATH)

TRANSLATOR_LABEL = translation_dict['translator']

# 用 [[]] 来标记要翻译的内容
# use [[]] to mark the content you want to translate
# 使用原始字符串和双重转义确保方括号被正确识别
pat = re.compile(r'\[\[(.*?)\]\]', flags=re.DOTALL | re.MULTILINE)

missing_files = []

def translate(m):
    try:
        # 确保捕获组存在
        content_to_trans = m.group(1)
        trans = translation_dict.get(content_to_trans, content_to_trans)
        return trans if trans else content_to_trans
    except IndexError:
        # 如果正则匹配没有捕获组，原样返回匹配到的字符串
        return m.group(0)

def make_parent_folder(output_path):
    # 对文件生成父级目录，防止不存在报错
    parent_folder = Path(output_path).parent.absolute()
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder, exist_ok=True)

def replace_in_file(file_path, translation, base_path=BASE_PATH, output_path=None):
    file_full_path = os.path.join(base_path, file_path)
    if not os.path.exists(file_full_path):
        missing_files.append(file_full_path)
        return

    # 强制 utf-8 读取
    with open(file_full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for ori_mark in translation:
        ori_content = ori_mark.replace('[[', '').replace(']]', '')
        trans = pat.sub(translate, ori_mark)
        content = content.replace(ori_content, trans)

    # 模糊匹配补丁：处理 index.html 中的安全警告
    if file_path.endswith('index.html'):
        for key in [
            'WARNING: The proxy option potentially leaks requests. Recommendation is to use a VPN.',
            'Jackett is running with root privileges. You should run Jackett as an unprivileged user.',
            'This site may use Cloudflare DDoS Protection, therefore Jackett requires FlareSolverr to access it.',
            'Security Risk: Your instance has external access enabled without using an admin password.'
        ]:
            if key in translation_dict:
                p_str = re.escape(key).replace(r'\ ', r'\s+')
                content = re.sub(p_str, translation_dict[key], content)

    if not output_path:
        output_path = file_full_path

    print(f'写入文件 {output_path}')
    make_parent_folder(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 创建补丁文件
if os.path.exists(PATCH_FOLDER):
    try: shutil.rmtree(PATCH_FOLDER)
    except: pass
os.makedirs(PATCH_FOLDER, exist_ok=True)

# --- 关键增强：全量复制原始文件 ---
logger.info("正在全量同步原始文件到补丁目录...")
shutil.copytree(os.path.join(BASE_PATH, 'src/Jackett.Common/Content'), os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Content'), dirs_exist_ok=True)
shutil.copytree(os.path.join(BASE_PATH, 'src/Jackett.Common/Definitions'), os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Definitions'), dirs_exist_ok=True)

# TODO: 关于页面添加翻译者信息
# add translator info in about page :)
logger.info(f"{ 'add translator info in about page.'}")
translator_info = f'{TRANSLATOR} {TRANSLATOR_URL} {LANG}'

# 下面是原始项目的翻译任务列表，一个不少
file_path = 'src/Jackett.Common/Content/custom.js'
translation = [
    '>[[Show all]]<', '>[[Click here to open an issue on GitHub for this indexer.]]<', '>[[NO UPLOAD]]<', '>[[ Show dead torrents]]<',
    '[[Search query consists of several keywords.\nKeyword starting with \"-\" is considered a negative match.]]',
    'doNotify("[[Error loading Jackett settings, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Error loading indexers, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Adding selected Indexers, please wait...]]",',
    'doNotify("[[Error: You must select more than one indexer]]",',
    'doNotify("[[Selected indexers successfully added.]]",',
    'doNotify("[[Configuration failed]]",',
    'doNotify("[[An error occurred while configuring this indexer, is Jackett server running ?]]",',
    'doNotify("[[Copied to clipboard!]]",',
    'doNotify("[[Error deleting indexer, request to Jackett server error]]",',
    'doNotify("[[An error occurred while testing indexers, please take a look at indexers with failed test for more informations.]]",',
    'doNotify("[[Request to Jackett server failed]]",',
    'doNotify("[[An error occurred while updating this indexer, request to Jackett server failed, is server running ?]]",',
    'doNotify("[[Downloaded sent to the blackhole successfully.]]",',
    'doNotify("[[Redirecting you to complete configuration update..]]",',
    'doNotify("[[Updater triggered see log for details..]]",',
    'doNotify("[[Admin password has been set.]]",',
    ', "[[All]]"]', "nonSelectedText: '[[All]]'",
    '"[[public]]"', '"[[private]]"', '"[[semi-private]]"',
]
replace_in_file(file_path, translation, output_path=PATCH_FOLDER + file_path)

file_path = 'src/Jackett.Common/Content/index.html'
translation = [
    '>[[API Key: ]]<', '>[[Standalone version of Jackett is now available - Mono not required]]<',
    '[[To upgrade to the standalone version of Jackett, <a href="https://github.com/Jackett/Jackett#install-on-linux-amdx64" target="_blank" class="alert-link">click here</a> for install instructions.\n            Upgrading is straight forward, simply install the standalone version and your indexers/configuration will carry over.\n            Benefits include: increased performance, improved stability and no dependency on Mono.]]',
    '>[[Configured Indexers]]<', '>[[Adding a Jackett indexer in Sonarr or Radarr]]<', '>[[Go to ]]<',
    '>[[Settings > Indexers > Add > Torznab > Custom]]<',
    '>[[Click on the indexers corresponding <button type="button" class="disabled btn btn-xs btn-info">Copy Torznab Feed</button> button and paste it into the Sonarr/Radarr <b>URL</b> field.]]<',
    '[[Click on an URL to copy it to the Site Link field.]]', '>[[For the <b>API key</b> use <b class="api-key-text"></b>.]]<',
    '>[[Configure the correct category IDs via the <b>(Anime) Categories</b> options. See the Jackett indexer configuration for a list of supported categories.]]<',
    '>[[Adding a Jackett indexer in CouchPotato]]<', '>[[Settings > Searchers]]<', '>[[Enable ]]<',
    '>[[Click on the indexers corresponding <button type="button" class="disabled btn btn-xs btn-info">Copy Potato Feed</button> button and paste it into the CouchPotato <b>host</b> field.]]<',
    '>[[Click on the indexers corresponding <button type="button" class="disabled btn btn-xs btn-info">Copy RSS Feed</button> button and paste it into the URL field of the RSS client.]]<',
    '>[[For the <b>Passkey</b> use <b class="api-key-text"></b>. Leave the <b>username</b> field blank.]]<',
    '>[[Adding a Jackett indexer to RSS clients (RSS feed)]]<',
    '[[You can adjust the <b>q</b> (search string) and <b>cat</b> (categories) arguments accordingly.\n                    E.g. <b>...&cat=2030,2040&q=big+buck+bunny</b> will search for "big buck bunny" in the Movies/SD (2030) and Movies/HD (2040) categories (See the indexer configuration for available categories).]]',
    '>[[Jackett Configuration]]<', '>[[   Apply server settings ]]<', '>[[ View logs ]]<', '>[[   Check for updates ]]<',
    '>[[Admin password: ]]<', '>[[  Set Password ]]<', '>[[Base path override: ]]<', '>[[Base URL override: ]]<',
    '>[[Server port: ]]<', '>[[Blackhole directory: ]]<', '>[[Proxy type: ]]<', '>[[Disabled]]<', '>[[Proxy URL: ]]<',
    '>[[Proxy port: ]]<', '>[[Proxy username: ]]<', '>[[Proxy password: ]]<', '>[[External access: ]]<',
    '>[[Local bind address: ]]<', '>[[Allow CORS: ]]<', '>[[Disable auto update: ]]<', '>[[Update to pre-release: ]]<',
    '>[[Enhanced logging: ]]<', '>[[Cache enabled (recommended): ]]<', '>[[Cache TTL (seconds): ]]<',
    '>[[Cache max results per indexer: ]]<', '>[[FlareSolverr API URL: ]]<', '>[[FlareSolverr Max Timeout (ms): ]]<',
    '>[[OMDB API key: ]]<', '>[[OMDB API Url: ]]<', '>[[ Version ]]<', '>[[Indexer]]<', '>[[Actions]]<', '>[[Categories]]<',
    '>[[Type]]<', '>[[Type string]]<', '>[[Language]]<', '>[[Cached Releases]]<',
    '>[[This screen shows releases which have been recently returned from Jackett. Only the last 300 releases for each tracker are returned.]]<',
    '>[[Published]]<', '>[[First Seen]]<', '>[[Tracker]]<', '>[[Name]]<', '>[[Size]]<', '[[title="Files">F</th>]]', '>[[Category]]<',
    '[[title="Grabs">G</th>]]', '[[title="Seeders">S</th>]]', '[[title="Leechers">L</th>]]', '>[[DLF]]<', '>[[ULF]]<',
    '>[[DL]]<', '>[[Close]]<', '>[[Manual search]]<', '>[[You can search all configured indexers from this screen.]]<',
    '>[[Query]]<', '>[[Filter]]<', '>[[Tracker]]<', '>[[all]]<', '>[[Error]]<', '>[[Select an indexer to setup]]<',
    '>[[Add Selected]]<', '>[[Server Logs]]<', '>[[Date]]<', '>[[Level]]<', '>[[Message]]<', '>[[Okay]]<', '>[[Capabilities]]<',
    '>[[Description]]<', '>[[Filter ]]<', '>[[All]]<', 'title="[[Copy API Key to clipboard]]"',
    'title="[[Jackett on GitHub]]"', 'title="[[Search]]"', 'title="[[Configure]]"', 'title="[[Delete]]"', 'title="[[Add]]"',
    'title="[[Download locally]]"', 'title="[[Download locally (magnet)]]"', 'title="[[Save to server blackhole directory]]"',
    'placeholder="[[Blank to disable]]"', '[[Your search was done using]]:',
    '[[WARNING: The proxy option potentially leaks requests. Recommendation is to use a VPN.]]',
    '> [[Add indexer]]', '> [[Manual Search]]', '>  [[View cached releases]]', '> [[Test All]]',
    '>[[Copy RSS Feed]]<', '>[[Copy Torznab Feed]]<', '>[[Copy Potato Feed]]<', '        [[Test]]', '"[[Blank for default]]"',
]
replace_in_file(file_path, translation, output_path=PATCH_FOLDER + file_path)

file_path = 'src/Jackett.Common/Content/libs/bootstrap-notify.js'
translation = ['>[[{1}]]<', '>[[{2}]]<']
replace_in_file(file_path, translation, output_path=PATCH_FOLDER + file_path)

file_path = 'src/Jackett.Common/Content/login.html'
translation = ['>[[Jackett]]<', '>[[Login]]<', '>[[Admin password]]<']
replace_in_file(file_path, translation, output_path=PATCH_FOLDER + file_path)

file_path = 'src/Jackett.Common/Content/libs/jquery.dataTables.min.js'
translation = [
    'sFirst:"[[First]]",', 'sLast:"[[Last]]"', 'sNext:"[[Next]]",', 'sPrevious:"[[Previous]]"', '"[[No data available in table]]"',
    'sInfo:"[[Showing _START_ to _END_ of _TOTAL_ entries]]"', 'sInfoEmpty:"[[Showing 0 to 0 of 0 entries]]",',
    'sInfoFiltered:"[[(filtered from _MAX_ total entries)]]"', 'sLengthMenu:"[[Show _MENU_ entries]]",',
    'sLoadingRecords:"[[Loading...]]",', 'sProcessing:"[[Processing...]]"', 'sSearch:"[[Search:]]",',
    'sZeroRecords:"[[No matching records found]]"',
]
replace_in_file(file_path, translation, output_path=PATCH_FOLDER + file_path)

def mass_trans_yml(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        res = re.findall('^type: (.*)', content, re.MULTILINE)
        for x in res:
            try: content = re.sub('^type: ' + x, 'type: ' + translation_dict[x.strip()], content, flags=re.MULTILINE)
            except: pass
        # 站点描述自动汉化
        desc_map = {'is a ': '是一个', 'CHINESE': '中国', 'TAIWANESE': '台湾', 'Public': '公开', 'Private': '私有',
                    'magnet tracker': '磁力站', 'Torrent Tracker': '种子站', 'torrent tracker': '种子站',
                    'for MOVIES': '针对 电影', 'for TV': '针对 电视', 'for GENERAL': '针对 综合', 'for ANIME': '针对 动漫',
                    'MOVIES / TV / GENERAL': '电影 / 电视 / 综合', 'MOVIES / TV': '电影 / 电视',
                    'MOVIES': '电影', 'TV': '电视', 'GENERAL': '综合', 'ANIME': '动漫'}
        for en, zh in desc_map.items(): content = content.replace(en, zh)
        return content


# Definitions 批量替换
def_folder = os.path.join(BASE_PATH, 'src/Jackett.Common/Definitions/')
if os.path.exists(def_folder):
    for x in os.listdir(def_folder):
        if x.endswith('.yml'):
            content = mass_trans_yml(os.path.join(def_folder, x))
            out_f = os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Definitions', x)
            make_parent_folder(out_f)
            with open(out_f, 'w', encoding='utf-8') as f: f.write(content)

def load_js(js_file_path, indent):
    with open(js_file_path, 'r', encoding='utf-8') as f:
        res = '\n'
        for line in f: res += ' ' * indent + line
        return res

# 最终手术：处理 custom.js
custom_js_final_path = os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Content/custom.js')
if os.path.exists(custom_js_final_path):
    with open(custom_js_final_path, 'r', encoding='utf-8') as f: content = f.read()
    key_code = 'if (item.type == "公开") {'
    if key_code in content:
        code = load_js('js_codes/item_type_fix.txt', 12)
        content = content.replace(key_code, code + '\n' + ' ' * 12 + key_code)
    if 'item.mains_cats = $.unique(main_cats_list).join(", ");' in content:
        code = load_js('js_codes/item_category_fix.txt', 12)
        content = content.replace('item.mains_cats = $.unique(main_cats_list).join(", ");', code)
    if 'function translation(results) {' not in content:
        content += load_js('js_codes/result_category_fix.txt', 0)
        content = content.replace('function updateSearchResultTable(element, results) {', 'function updateSearchResultTable(element, results) {\n    if ("Results" in results) { results.Results = translation(results.Results); }')
        content = content.replace('api.getServerCache(function (data) {', 'api.getServerCache(function (data) {\n            data = translation(data);')
    # 筛选标签替换
    content = content.replace('id: "test:passed"', 'id: "测试:通过"').replace('id: "test:failed"', 'id: "测试:失败"')
    content = content.replace('id: "type:public"', 'id: "类型:公开"').replace('id: "type:private"', 'id: "类型:私密"')
    # 注入动态翻译补丁
    dynamic_patch = r"""
(function() {
    const transDict = {
        "Jackett is running with root privileges. You should run Jackett as an unprivileged user.": "Jackett 正在以 root 权限运行。建议您以非特权用户身份运行 Jackett。",
        "WARNING: The proxy option potentially leaks requests. Recommendation is to use a VPN.": "警告：代理选项可能会泄漏请求。建议使用 VPN。",
        "A <b>FlareSolverr</b> error means your IP was not accepted.": "<b>FlareSolverr</b> 错误意味着您的 IP 不被接受。",
        "FlareSolverr is required to access this site.": "访问此站点需要 FlareSolverr。"
    };
    const flareRegex = /This site may use Cloudflare DDoS Protection,?\s+therefore Jackett requires FlareSolverr to access it.?/i;
    const flareZh = "此站点可能使用了 Cloudflare DDoS 保护，因此 Jackett 需要 FlareSolverr 才能访问它。";
    function trNode(node) {
        if (!node) return;
        if (node.nodeType === 3) {
            let t = node.nodeValue; if (!t) return;
            for (let [en, zh] of Object.entries(transDict)) { if (t.includes(en)) t = t.replace(en, zh); }
            if (flareRegex.test(t)) t = t.replace(flareRegex, flareZh);
            t = t.replace(/Test started for (.*)/i, "正在开始测试索引器: $1").replace(/Test successful for (.*)/i, "索引器测试成功: $1");
            if (t.includes("is a ") || t.toLowerCase().includes("tracker")) {
                const dict = {"is a ": "是一个", "CHINESE": "中国", "TAIWANESE": "台湾", "Public": "公开", "Private": "私有", "MOVIES": "电影", "TV": "电视", "GENERAL": "综合", "ANIME": "动漫"};
                const ks = Object.keys(dict).sort((a, b) => b.length - a.length);
                for (let en of ks) t = t.replace(new RegExp(en, 'gi'), dict[en]);
            }
            node.nodeValue = t;
        } else if (node.nodeType === 1) {
            ['placeholder', 'title'].forEach(a => { 
                let v = node.getAttribute(a); if (v) {
                    if (flareRegex.test(v)) v = v.replace(flareRegex, flareZh);
                    for (let [en, zh] of Object.entries(transDict)) { if (v.includes(en)) v = v.replace(en, zh); }
                    v = v.replace(/Test started for (.*)/i, "正在开始测试索引器: $1").replace(/Test successful for (.*)/i, "索引器测试成功: $1");
                    node.setAttribute(a, v);
                }
            });
            if (node.innerHTML && flareRegex.test(node.innerHTML)) node.innerHTML = node.innerHTML.replace(flareRegex, flareZh);
            node.childNodes.forEach(trNode);
        }
    }
    const obs = new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach(trNode)));
    trNode(document.body);
    obs.observe(document.body, { childList: true, subtree: true });
})();
"""
    with open(custom_js_final_path, 'w', encoding='utf-8') as f: f.write(content + "\n// 动态翻译补丁\n" + dynamic_patch)

# 整理文件：把文件夹移出来
shutil.move(os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Content'), os.path.join(PATCH_FOLDER, 'Content_tmp'))
shutil.move(os.path.join(PATCH_FOLDER, 'src/Jackett.Common/Definitions'), os.path.join(PATCH_FOLDER, 'Definitions_tmp'))
shutil.rmtree(os.path.join(PATCH_FOLDER, 'src'))
shutil.move(os.path.join(PATCH_FOLDER, 'Content_tmp'), os.path.join(PATCH_FOLDER, 'Content'))
shutil.move(os.path.join(PATCH_FOLDER, 'Definitions_tmp'), os.path.join(PATCH_FOLDER, 'Definitions'))

if missing_files:
    logger.info(f"{ 'missing_files!'}")
    for x in missing_files: logger.info(f'{x}')
logger.info(f"{ 'finished!'}")
if platform.system() == 'Linux' and 'GITHUB_ACTIONS' not in os.environ: os.system(f'xdg-open {PATCH_FOLDER}')

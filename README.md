# Jackett 汉化工具 (增强版)

本项目 Fork 自 [Nriver/jackett-translation](https://github.com/Nriver/jackett-translation)，并针对本地化运行、自动化处理和深度汉化进行了显著增强。

### 🚀 增强功能
- **一键入口**：提供 `start_translation.py` 脚本，无需繁琐步骤，一键生成本地补丁。
- **全量汉化**：不仅处理静态页面，还自动扫描并翻译所有 500+ 个索引器定义文件（Definitions）。
- **动态劫持**：通过 JavaScript 注入技术，完美解决了原版无法触及的 Root 权限警告、FlareSolverr 提示、动态测试通知以及站点实时描述信息。
- **跨平台修复**：彻底解决了在 Windows 环境下常见的 GBK 编码报错、路径斜杠冲突以及文件占用无法删除等兼容性问题。

### 🐳 Docker 用户使用指南 (以 linuxserver/jackett 为例)

对于使用 Docker 的用户，推荐通过卷映射（Volumes）的方式实现汉化，这样即使容器更新，汉化依然有效。

#### 1. 提取原始文件
在容器运行时，执行以下命令将原始静态文件复制到主机的映射目录（假设您的映射目录是 `./data`）：
```bash
docker exec -it jackett-9117 cp -r /app/Jackett/Content /config/Content
docker exec -it jackett-9117 cp -r /app/Jackett/Definitions /config/Definitions
```

#### 2. 汉化处理
将提取出来的 `Content` 和 `Definitions` 文件夹放到本项目根目录，运行：
```bash
python start_translation.py
```

#### 3. 映射回容器
将生成的 `Jackett-CN-Patch/` 文件夹内的 `Content` 和 `Definitions` 复制到您的 Docker 数据目录下，并在 `docker-compose.yml` 中添加以下映射：

```yaml
services:
  jackett:
    image: linuxserver/jackett:latest
    container_name: jackett-9117
    volumes:
      - ./data:/config
      - ./data/Content:/app/Jackett/Content
      - ./data/Definitions:/app/Jackett/Definitions
    # ... 其他配置
```
最后重启容器即可完成汉化。

### 🛠️ 使用方法 (本地处理)
1. **准备原始文件**：从 Jackett 原版安装目录提取 `Content` 和 `Definitions` 文件夹，并放置到本项目根目录下。
2. **安装依赖**：
   ```bash
   pip install loguru
   ```
3. **运行汉化**：
   ```bash
   python start_translation.py
   ```
4. **覆盖安装**：运行完成后，将生成的 `Jackett-CN-Patch` 文件夹内的内容直接覆盖回 Jackett 安装目录即可。

---

# jackett-cn

jackett 汉化

如果你喜欢，请给个star :)

# 截图

主界面
![](docs/screenshot_1.png)

索引器搜索
![](docs/screenshot_2.png)

# 食用方法

1. 下载[原版](https://github.com/Jackett/Jackett/releases)
2. 下载[汉化包 jackett-cn-patch.zip](https://github.com/Nriver/jackett-translation/releases), 解压覆盖原版对应的目录

# 翻译打包流程

1. init.py
2. trans.py
3. make_release.py

# 翻译

## 静态文件

在源码这个目录下 /Jackett/src/Jackett.Common/Content/ 的Release包Content目录的页面代码

## 源码

一些文字是写死在c#代码里的, 由于没有方便的编译环境, 没有进行处理, 有想法的欢迎提pr.

## 通过 Scoop 安装

添加我的scoop源

```
scoop bucket add Scoop-Nriver https://github.com/nriver/Scoop-Nriver
```

安装 Jackett

```
scoop install jackett-cn
```

更新

```
scoop update jackett-cn
```
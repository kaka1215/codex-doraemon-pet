# 哆啦A梦 · Codex Pet

[English](README.en.md)

一个日式二维动画风格的哆啦A梦桌面伙伴，支持 Codex 桌面端的 **9 组状态、57 帧动画**。包含待机眨眼、左右跑动、挥手、跳跃、等待、思考和检查成果。

<p align="center"><img src="preview.gif" width="720" alt="哆啦A梦的九组宠物动画"></p>

> 非官方同人项目，与 OpenAI 或哆啦A梦权利方无隶属、合作或认可关系。代码和文档采用 MIT；角色图像不在该许可范围内，见 [素材权利说明](ASSET_RIGHTS.md)。

## 安装

下载本仓库（**Code → Download ZIP** 并解压），或：

```sh
git clone https://github.com/kaka1215/codex-doraemon-pet.git
cd codex-doraemon-pet
python3 install.py
```

Windows 可使用 `py install.py`。安装器只需要 Python 3 标准库，无需安装 Pillow。

安装器会验证文件校验和，把 `pet.json` 和 `spritesheet.webp` 放到 `$CODEX_HOME/pets/doraemon-theatrical/`；没有设置 `CODEX_HOME` 时，使用 `~/.codex/pets/doraemon-theatrical/`。更新时会先备份旧文件到 `pets/.backups/`，重复安装同一版本不会重复写入。

```sh
# 只检查，不写入
python3 install.py --dry-run

# 指定 Codex 数据目录
python3 install.py --codex-home "/path/to/codex-data"
```

也可以手动创建上述目录，并将本仓库的 `pet.json`、`spritesheet.webp` 一起复制进去。

安装后：

1. 打开桌面应用的 **设置 → Pets／宠物**（部分版本为 Mini & Pets）。
2. 点击 **Refresh／刷新**，选择 **「哆啦A梦 · 剧场版」**。
3. 输入 **`/pet`**，或在命令菜单选择 **Show pet**。
4. 在 **Customize → Pet size** 调整大小。

参见 [OpenAI 官方 Pets 说明](https://learn.chatgpt.com/docs/pets)。本包面向桌面端的本地自定义宠物格式；不自动同步到网页端。

## 跑动预览

<p align="center"><img src="run-preview.gif" width="720" alt="左右跑动与待机比例对照"></p>

跑步采用前伸、蹬地、收腿和腾空的循环；左右两组由同一套姿势制作。预览保留桌面端的播放间隔：前七帧各 120 ms、末帧 220 ms，较长停留放在接地姿势。

这是简化的二维卡通跑步，部分半周期摆臂重复。请以预览效果判断是否符合自己的偏好。

## 文件与动画规格

| 文件 | 用途 |
| --- | --- |
| `pet.json` | 宠物名称、ID 与精灵图路径 |
| `spritesheet.webp` | 最终透明动画精灵图 |
| `reference.png` | 角色比例参考图 |
| `preview.gif` / `run-preview.gif` | 全动作和跑动预览 |
| `install.py` | 校验、安装、更新前备份 |
| `validate.py` | 校验精灵图，也可导出单帧供修改 |
| `DESIGN.md` | 制作方法与可复用提示词 |
| `SHA256SUMS` | 安装所用两份文件的 SHA-256 |

格式为 **Codex sprite v1**：1536 × 1872，8 列 × 9 行，每格 192 × 208；未用格完全透明。

| 行（从 0 开始） | 状态 | 帧数 |
| --- | --- | ---: |
| 0 | `idle` 待机 | 6 |
| 1 | `running-right` 向右移动 | 8 |
| 2 | `running-left` 向左移动 | 8 |
| 3 | `waving` 挥手 | 4 |
| 4 | `jumping` 跳跃 | 5 |
| 5 | `failed` 遇到问题 | 8 |
| 6 | `waiting` 等待回应 | 6 |
| 7 | `running` 思考／处理任务 | 6 |
| 8 | `review` 检查成果 | 6 |

`running` 表示处理任务；实际跑动使用两个方向状态。

## 校验与修改

需要 Python 3 和 Pillow：

```sh
python3 -m pip install -r requirements.txt
python3 validate.py
python3 -m unittest -v test_install.py
python3 validate.py --extract frames
```

校验包含尺寸、透明通道、57 个有效帧、15 个空白格、边界裁切及透明像素残留。导出会生成 `frames/<state>/<index>.png`；已有帧文件不会被覆盖。测试只使用临时目录，不写入真实 Codex 目录。

修改精灵图后，请重新生成 `SHA256SUMS`，再运行校验。制作过程使用内置 ImageGen 与官方 [hatch-pet 技能](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet)。本仓库提供最终可安装素材和独立安装／校验代码，不包含该技能的上游实现。

## 许可

本仓库原创代码和文档使用 [MIT](LICENSE)。哆啦A梦及相关名称、形象的权利归相应权利人所有；图片、动图和精灵图不包含在 MIT 授权范围内。本仓库不授予这些角色的商业使用或再许可权。详见 [ASSET_RIGHTS.md](ASSET_RIGHTS.md)。

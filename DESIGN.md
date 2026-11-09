# 制作与二次修改

形象目标是日式二维动画风格：较高且小的椭圆眼睛、窄躯干、细黑轮廓、蓝白红黄纯色。`reference.png` 用于保持角色比例；`spritesheet.webp` 是最终帧数据的来源。

制作使用内置 ImageGen，逐行生成状态动画，再通过官方 hatch-pet 的确定性提取、组装和校验流程处理。透明边缘采用色键去色；每一行使用统一缩放与位置配准，避免逐帧缩放引起大小跳变。左向跑步从右向逐帧镜像，保留时间顺序。没有加入阴影、速度线或漂浮装饰。

最终跑步包含接地、支撑、蹬地、腾空阶段。将整段循环的起点平移，使桌面端较长的末帧停留落在接地姿势，而不是空中。其他七种状态保持稳定。

## 可复用的跑步提示词

下面是整理后的设计提示词，不是确定性构建脚本。以 `reference.png` 和从精灵图导出的目标帧作为图像参考；模型输出仍需逐帧检查。

> Create exactly eight separate full-body poses in one horizontal rightward run-cycle strip. Use the supplied Doraemon reference as the character model. Preserve the modest round head, small high oval eyes, narrow torso, white pocket, red collar and nose, yellow bell, and compact white oval feet.
>
> Show a clear forward reach, push-off, recovery and short flight phase. Keep the chest-to-hip length and head size stable. Increase stride through leg rotation rather than larger feet. Use a right-facing three-quarter view with the belly and both eyes readable. Arm movement should oppose the legs. Avoid tiny shuffling, body collapse, oversized head, enlarged feet or long human legs.
>
> Keep one construction scale and common ground baseline across all eight poses. Use generous spacing and complete unclipped figures. Flat Japanese 2D anime, continuous fine black outlines, solid blue/white/red/yellow fills. Uniform #FF00FF chroma background; no labels, grids, shadows, floor, effects, texture or motion blur.

## 修改流程

1. 运行 `python3 validate.py --extract frames`，导出全部 57 帧。
2. 编辑所需状态，并按 README 中的行号和帧数放回精灵图。
3. 保持 192 × 208 单格、1536 × 1872 总尺寸；未使用格必须完全透明。
4. 对 `pet.json` 和 `spritesheet.webp` 重新计算 SHA-256，更新 `SHA256SUMS`。
5. 运行校验与安装测试，并检查浅色、深色背景和实际播放节奏。

自动校验只能发现格式问题，不能代替动作和角色一致性的目视检查。本项目的跑步是简化卡通循环，部分摆臂相位重复。

参考工具：[OpenAI hatch-pet](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet)；使用说明：[Pets](https://learn.chatgpt.com/docs/pets)。

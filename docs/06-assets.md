# LYCO · 资产清单

> 全部资产位于 `design/` 与 `platform/`。
> **`design/` 是设计基准，只读，不要改。**

---

## design/ 设计基准

### three-view/ —— 三视图（★ 最高权威）

| 文件 | 说明 |
|---|---|
| `lyco_three_view.png` | **三视图** 正 / 侧 / 背。任何尺寸争议以这张为准 |
| `lyco_three_view_face_zoom.png` | 脸部放大校验图 |

### palette/ —— 配色

| 文件 | 说明 |
|---|---|
| `lyco_palette_card.png` | **配色卡**，19 个色值 + 用途 + 设计铁律 |

### illustration/ —— 立绘

| 文件 | 说明 | 用途 |
|---|---|---|
| `lyco_fullbody_stand.png` | 全身立绘 · 正面站姿 | 壁纸 / 装扮 / 亚克力立牌 |
| `lyco_action_redflash.png` | 战斗立绘 · 红色闪光 | 壁纸 / 转场 / 色纸 |
| `lyco_chibi_sheet_9pose.png` | Q 版精灵表 · 9 姿势 | **桌宠** / 表情包 / 挂件 |

Q 版 9 姿势：正面站 / 侧面站 / 走 / 跑 / 腾空 / 蹲 / 挥击 / 持杆 / 倒地

### expression/ —— 表情

| 文件 | 说明 |
|---|---|
| `lyco_expression_sheet.png` | 表情差分 ×4（默认 / 微讶 / 闭眼 / 侧目） |

### action/ —— 动作关键帧

| 文件 | 说明 |
|---|---|
| `lyco_act_idle_dodge.png` | 待机 与 侧身闪避 |
| `lyco_act_counter_redflash.png` | 反击充能 与 红色闪光 |

### weapon/ —— 武器

| 文件 | 说明 |
|---|---|
| `lyco_weapon_stowed.png` | 收束形态（便携短杆） |
| `lyco_weapon_rifle.png` | 步枪形态 |
| `lyco_weapon_scythe.png` | 镰刀形态（巨大弯刃） |
| `lyco_weapon_atlas_band.png` | 游戏内图集带（786×121 像素对齐版） |

### layers/ —— 分层拆件

| 文件 | 说明 |
|---|---|
| `lyco_layer_split.png` | 前发 / 后发 / 光头 / 军装 / 左右臂 / 两片裙 / 红内衬 / 裤袜 / 双腿 / 双靴 |

**这张是 Live2D 绑定的输入格式**，可直接用于 Inochi2D / Cubism。

---

## platform/ 各平台落地

### minecraft/

| 文件 | 说明 |
|---|---|
| `lyco_slim.png` | **推荐** —— 64×64，纤细手臂（Alex 模型） |
| `lyco_classic.png` | 64×64，标准手臂（Steve 模型） |
| `preview.png` | 头部特写 + 正/侧/背预览 |
| `_archive/` | 备选与失败版本（不推荐使用） |

**用法**：上传到 minecraft.net 或皮肤站即可。

### live2d/ —— *预留*

计划：用 Inochi2D（开源一条龙）绑定 `design/layers/lyco_layer_split.png`。
产出 `lyco.inochi2d` + 直播配置。

### streaming/ —— *预留*

计划：待机动画 / 进场特效 / 粉丝牌 / 弹幕样式 / 转场。
规格见 [挂件规范 B1](04-accessories.md#b1-直播挂件)。

---

## tools/ 生成脚本

所有资产**可复现**。脚本需要 Python + numpy / Pillow / scipy。

| 脚本 | 用途 |
|---|---|
| `make_palette_card.py` | 生成配色卡 |
| `build_mc_skin_v2.py` | 生成 Minecraft 皮肤 |
| `fix_chatgpt_skin2.py` | 把高分皮肤图降采样为 64×64（**效果一般，仅备查**） |

---

## 版本历史

| 版本 | 变更 |
|---|---|
| `v1.0` | 首次整理。设计基准 = 三视图 v3。含 8 类设计资产 + Minecraft 皮肤 |

# Minecraft 皮肤 · 设计规范与工具生态

> 调研来源：[minotar/skin-spec](https://github.com/minotar/skin-spec)（权威技术规范）、
> [Minecraft Wiki](https://minecraft.wiki/w/Skin)、[Mojang 帮助中心](https://help.minecraft.net/)、
> 以及**本项目实测**（2026-09/10，见文末「踩过的坑」）

---

# 一、格式规范

## 1.1 硬性要求

| 项目 | 要求 |
|---|---|
| **尺寸** | **64×64**（1.8+）或 **64×32**（1.8 之前）—— 其他尺寸一律非法 |
| **格式** | PNG |
| **色彩空间** | 无强制；但建议显式转成 NRGBA 以避免色偏 |
| **位深** | 8 bit/通道（标准 PNG） |

> ⚠️ **512×512 不是合法皮肤。** 这是最常见的新手错误 ——
> 很多生图模型输出 512×512，直接上传会报格式错误。必须先用 **NEAREST** 降采样到 64×64。

## 1.2 完整 UV 表（已修正 skin-spec 的印刷错误）

坐标系：`(x1, y1, x2, y2)`，左上角为原点。

### 第一层（身体本体）——**绝对不能不透明**

| 部位 | 面 | 坐标 | 尺寸 |
|---|---|---|---|
| **头** | Top | `(8, 0, 16, 8)` | 8×8 |
| | Bottom | `(16, 0, 24, 8)` | 8×8 |
| | Right | `(0, 8, 8, 16)` | 8×8 |
| | Front | `(8, 8, 16, 16)` | 8×8 |
| | Left | `(16, 8, 24, 16)` | 8×8 |
| | Back | `(24, 8, 32, 16)` | 8×8 |
| **躯干** | Top | `(20, 16, 28, 20)` | 8×4 |
| | Bottom | `(28, 16, 36, 20)` | 8×4 |
| | Right | `(16, 20, 20, 32)` | 4×12 |
| | Front | `(20, 20, 28, 32)` | 8×12 |
| | Left | `(28, 20, 32, 32)` | 4×12 |
| | Back | `(32, 20, 40, 32)` | 8×12 |
| **右臂** | Top | `(44, 16, 48, 20)` | 4×4 |
| | Bottom | `(48, 16, 52, 20)` | 4×4 |
| | Right | `(40, 20, 44, 32)` | 4×12 |
| | Front | `(44, 20, 48, 32)` | 4×12 |
| | Left | `(48, 20, 52, 32)` | 4×12 |
| | Back | `(52, 20, 56, 32)` | 4×12 |
| **右腿** | Top | `(4, 16, 8, 20)` | 4×4 |
| | Bottom | `(8, 16, 12, 20)` | 4×4 |
| | Right | `(0, 20, 4, 32)` | 4×12 |
| | Front | `(4, 20, 8, 32)` | 4×12 |
| | Left | `(8, 20, 12, 32)` | 4×12 |
| | Back | `(12, 20, 16, 32)` | 4×12 |
| **左腿** | Top | `(20, 48, 24, 52)` | 4×4 |
| | Bottom | `(24, 48, 28, 52)` | 4×4 |
| | Right | `(16, 52, 20, 64)` | 4×12 |
| | Front | `(20, 52, 24, 64)` | 4×12 |
| | Left | `(24, 52, 28, 64)` | 4×12 |
| | Back | `(28, 52, 32, 64)` | 4×12 |
| **左臂** | Top | `(36, 48, 40, 52)` | 4×4 |
| | Bottom | `(40, 48, 44, 52)` | 4×4 |
| | Right | `(32, 52, 36, 64)` | 4×12 |
| | Front | `(36, 52, 40, 64)` | 4×12 |
| | Left | `(40, 52, 44, 64)` | 4×12 |
| | Back | `(44, 52, 48, 64)` | 4×12 |

### 第二层（帽层 / 外套层）——**可以透明**

| 部位 | 包围盒 | 六个面 |
|---|---|---|
| 帽层 | `(32,0)-(64,16)` | Top `(40,0,48,8)` · Bottom `(48,0,56,8)` · Right `(32,8,40,16)` · Front `(40,8,48,16)` · Left `(48,8,56,16)` · Back `(56,8,64,16)` |
| 躯干外套 | `(16,32)-(40,48)` | Top `(20,32,28,36)` · Bottom `(28,32,36,36)` · Right `(16,36,20,48)` · Front `(20,36,28,48)` · Left `(28,36,32,48)` · Back `(32,36,40,48)` |
| 右臂外套 | `(40,32)-(56,48)` | Top `(44,32,48,36)` · Bottom `(48,32,52,36)` · Right `(40,36,44,48)` · Front `(44,36,48,48)` · Left `(48,36,52,48)` · Back `(52,36,56,48)` |
| 右腿外套 | `(0,32)-(16,48)` | Top `(4,32,8,36)` · Bottom `(8,32,12,36)` · Right `(0,36,4,48)` · Front `(4,36,8,48)` · Left `(8,36,12,48)` · Back `(12,36,16,48)` |
| **左腿外套** | `(0,48)-(16,64)` | Top `(4,48,8,52)` · Bottom `(8,48,12,52)` · Right `(0,52,4,64)` · Front `(4,52,8,64)` · Left `(8,52,12,64)` · Back `(12,52,16,64)` |
| **左臂外套** | `(48,48)-(64,64)` | Top `(52,48,56,52)` · Bottom `(56,48,60,52)` · Right `(48,52,52,64)` · Front `(52,52,56,64)` · Left `(56,52,60,64)` · Back `(60,52,64,64)` |

> **⚠️ 已修正 skin-spec 的 4 处印刷错误**（原文把右侧外套的 Top/Bottom 写成了 y=48，导致 `y2 < y1` 的非法值）：
> - 躯干外套 Top `(20,48,28,36)` → **`(20,32,28,36)`**
> - 右臂外套 Top `(44,48,48,36)` → **`(44,32,48,36)`**
> - 右腿外套 Top `(4,48,8,36)` → **`(4,32,8,36)`**
> - 右臂外套 Back `(52,36,64,48)` → **`(52,36,56,48)`**
>
> 另外原文把「左腿外套」和「右腿外套」的 Top 写成同一坐标，也是这个错误导致的。

### 模型类型：classic vs slim

| | classic（Steve） | slim（Alex） |
|---|---|---|
| 手臂宽 | 4 px | **3 px** |
| 右臂 Top | `(44,16,48,20)` | `(44,16,47,20)` |
| 右臂 Bottom | `(48,16,52,20)` | `(47,16,50,20)` |
| 右臂 Left | `(48,20,52,32)` | `(47,20,51,32)` |
| 右臂 Back | `(52,20,56,32)` | `(51,20,54,32)` |
| 左臂 Top | `(36,48,40,52)` | `(36,48,39,52)` |
| 左臂 Bottom | `(40,48,44,52)` | `(39,48,42,52)` |
| 左臂 Left | `(40,52,44,64)` | `(39,52,43,64)` |
| 左臂 Back | `(44,52,48,64)` | `(43,52,46,64)` |

> **坑**：slim 皮肤的左臂包围盒 `(32,48)-(48,64)` 里，**第 46–48 列是不使用的**。
> 用包围盒做「第一层是否全不透明」的校验会**误报**。必须逐面检查。

---

# 二、透明度规则（最容易翻车的一节）

## 2.1 两条并列机制

skin-spec 原文：

> *"Transparency must be based off of the upper left-hand pixel of the image.
> Though many skins use standard the standard alpha-channel, others use a solid matte."*

也就是说，皮肤有两种表达透明的方式：

| 机制 | 做法 | 判断方式 |
|---|---|---|
| **标准 alpha 通道** | 透明像素 alpha = 0 | 看 alpha |
| **哑光色（matte）** | 左上角 `(0,0)` 像素的颜色 = **透明色**；全图等于该色的像素都视为透明 | 看 `(0,0)` 的颜色 |

**实测我们自己的文件**（`tools/check_matte_rule.py`）：

```
手绘 v2 slim        左上角 #000000 a=0     → 标准 alpha 通道
BLOCK seed0        左上角 #FDFDFD a=255   → 同色像素仅 67 个，非哑光皮肤
Kaggle v6 seed42   左上角 #FDFEFD a=255   → 同色像素仅 11 个，非哑光皮肤
```

→ **我们产出的是标准 alpha 皮肤**，不涉及哑光机制。
但**处理别人的皮肤时必须判断**，否则会：
- 把哑光皮肤当标准皮肤 → 该透明的地方变成实心色块
- 把标准皮肤当哑光皮肤 → **误删真实内容**

## 2.2 ★ 第一层 / 第二层的透明度约束

**这条最实用**，直接决定皮肤能不能用：

| 层 | 是否可透明 | 后果 |
|---|---|---|
| **第一层**（身体本体） | **✗ 必须完全不透明** | 有透明像素 → **角色身上出现破洞** |
| **第二层**（帽层 / 外套层） | **✓ 可以透明** | 全不透明 → **整个角色被这层盖住** |

### 实例：BLOCKv0.6 输出为什么在游戏里变成白块

| 文件 | 第二层不透明占比 | 结果 |
|---|---|---|
| 手绘 v2 slim | hat 51% · jacket 75% · 其余 0% | ✅ 正常 |
| **BLOCK 未修** | **hat 100% · jacket 100% · 四肢 100%** | ❌ **角色成一坨白块** |
| BLOCK 已修 | hat 12% · jacket 16% · 其余 0% | ✅ 正常 |
| Kaggle v6 | hat 14% · 其余 0% | ✅ 正常 |

根因：**模型输出 RGB 没有 alpha 通道**，它把「应该透明」的区域填成了白色；
而第二层是**盖在第一层上面渲染**的 → 全白 = 白块。

**修法**：把第二层里的近白像素判为背景、置为透明（`tools/fix_block_skin.py`）。

---

# 三、设计规范（怎么做好看，不只是合法）

## 3.1 先认清分辨率的物理现实

| 部位 | 可用像素 |
|---|---|
| 头（整块） | 8×8×8 |
| **脸（正面）** | **8×8 —— 这就是全部** |
| 躯干正面 | 8×12 |
| 手臂正面 | 4×12（classic）/ 3×12（slim） |
| 腿正面 | 4×12 |

**结论**：**脸只有 8×8 像素**。这是硬上限，任何「精修五官」的想法都要先接受这一点。
能做到的是：**一双眼睛 + 一条嘴线**，仅此而已。

## 3.2 8×8 脸的可行方案

```
row0-2  ← 刘海（约占 3 行，形成"重刘海"）
row3    ← 额头
row4    ← 上眼睑（深色）
row5    ← 瞳色 + 1 个白色高光点
row6    ← 鼻下 / 阴影
row7    ← 下巴（两侧可放发梢）
```

**要点**：
- **眼睛给 2 行**（上睑 + 瞳），比 1 行更"有神"
- **高光点朝内**（显得温和），朝外会显得凶
- **不要画眉毛** —— 8px 宽度下画了会糊
- **嘴只给 1–2px**，深色

## 3.3 第二层怎么用（决定"厚度感"）

好皮肤和差皮肤的主要差别就在第二层。

| 用法 | 效果 |
|---|---|
| **头发体积** | 帽层铺满头发 → 头看起来更"厚" |
| **外套/裙摆** | 躯干外套区做衣服的立体层 |
| **靴套** | 腿外套区做靴筒 |
| ❌ **整层填满纯色** | **变成白块/色块，角色废掉** |

**规则**：第二层**只在该有内容的地方有像素**，其余必须是透明的。

## 3.4 明暗分层

同一个物体用 **3–4 档明度**，不要平涂：

```
高光 / 受光面  →  1 档
基础色        →  1 档
阴影面        →  1 档
最暗 / 缝隙    →  1 档
```

**深色衣服配深色头发时**，必须靠**边缘高光**把两者分开，否则会糊成一团。

## 3.5 反面清单

| ❌ 不要做 | 原因 |
|---|---|
| 第二层填实色 | 角色变成色块 |
| 第一层留透明 | 身上有洞 |
| JPEG 转 PNG | 有损压缩会产生噪点 |
| 尺寸非 64×32 / 64×64 | 直接非法 |
| 用 LANCZOS/BOX 缩放到 64×64 | 会把像素风糊掉，必须 NEAREST |
| 画眉毛 / 口红 / 复杂五官 | 8px 承载不了 |
| 脸上放高对比花纹 | 远看是一坨 |

---

# 四、工具生态

## 4.1 编辑器

| 工具 | 星 | 说明 |
|---|---|---|
| [JannisX11/blockbench](https://github.com/JannisX11/blockbench) | ★6013 | **低多边形 3D 模型编辑器**，支持皮肤格式；**有 MCP（含无头模式）** |
| [NeedCoolerShoes/editor](https://github.com/NeedCoolerShoes/editor) | ★19 | 网页皮肤编辑器（NeedCoolerShoes 官方） |
| [hamza512b/mineskin](https://github.com/hamza512b/mineskin) | — | 轻量编辑器 |
| [chililisoup/mcskinshop](https://github.com/chililisoup/mcskinshop) | — | 皮肤编辑器 / 构建器 |
| [RedGradient/MinecraftSkinEditor](https://github.com/RedGradient/MinecraftSkinEditor) | — | 皮肤编辑器 |
| [tianer2820/BetterSkin2](https://github.com/tianer2820/BetterSkin2) | — | 功能丰富（2023 停更） |
| [KareemMAX/Minecraft-Skiner](https://github.com/KareemMAX/Minecraft-Skiner) | — | 已归档 |

## 4.2 渲染器（做预览图用）

| 工具 | 星 | 说明 |
|---|---|---|
| [bs-community/skinview3d](https://github.com/bs-community/skinview3d) | ★731 | **Three.js 皮肤查看器**，事实标准；有 React / Vue 绑定 |
| [NickAcPT/nmsr-rs](https://github.com/NickAcPT/nmsr-rs) | ★118 | Rust，**真实透视**渲染 |
| [daidr/minecraft-skin-renderer](https://github.com/daidr/minecraft-skin-renderer) | — | 零依赖，WebGL + WebGPU |
| [mineatar-io/skin-render](https://github.com/mineatar-io/skin-render) | ★50 | Go，2D/3D 等距渲染库 |
| [Bkm016/minecraft-skin-renderer](https://github.com/Bkm016/minecraft-skin-renderer) | — | Node.js 渲染服务，皮肤哈希 → 3D 头像 |

> ⚠️ **投毒警告**：`pkg.go.dev` 上的 `github.com/soulfulscul/skin-render` 是
> **冒名 `mineatar-io/skin-render` 的投毒包**（仓库不存在，文档里藏了下载执行远端 exe 的混淆代码）。
> 详见 [10-mc-skin-blockv0.6-实测.md](10-mc-skin-blockv0.6-实测.md)。

## 4.3 生成器（AI 路线）

| 项目 | 说明 |
|---|---|
| **[AliceKJ/BLOCKv0.6](https://huggingface.co/AliceKJ/BLOCKv0.6)** | **当前最好** —— 3D 预览图 → 64×64 皮肤，FLUX.2-klein-base-4B，apache-2.0 |
| [RandomGamingDev/MCSkinsGen](https://github.com/RandomGamingDev/MCSkinsGen) | 基于 Stable Diffusion v1.5 |
| [Monadical-SAS/minecraft_skin_generator](https://github.com/Monadical-SAS/minecraft_skin_generator) | 文本 → 皮肤（HuggingFace 上有对应模型） |
| [udu3324/PNGskin](https://github.com/udu3324/PNGskin) | 图片 → 皮肤 |
| [paulknewton/minecraft-skin-generator](https://github.com/paulknewton/minecraft-skin-generator) | 照片 → 皮肤 |
| [PaperMonoid/minecraft-skin-generator](https://github.com/PaperMonoid/minecraft-skin-generator) | 自编码器 |

**BLOCK 的两阶段方法论**（重要）：
```
① MLLM 出 3D 预览图（正/背双联斜视角）   ← 自由构图，MLLM 擅长
        ↓
② image-to-image 解码成 64×64 皮肤        ← 固定几何，专用模型
```
**不要让生图模型直接输出皮肤图集** —— 它不产出固定几何。

## 4.4 3D / 模型工具链

| 工具 | 说明 |
|---|---|
| [jasonjgardner/blockbench-mcp-plugin](https://github.com/jasonjgardner/blockbench-mcp-plugin) ★467 | Blockbench 的 MCP 服务，**含无头模式**（`npx -y github:jasonjgardner/blockbench-mcp-plugin --root ./models`） |
| [sosadly/blockbench-mcp](https://github.com/sosadly/blockbench-mcp) | MCP + 插件，直接控制 Blockbench |
| [Ru1n-dev/ruins-blockbench-mcp](https://github.com/Ru1n-dev/ruins-blockbench-mcp) | 模型 / UV / 贴图 / 动画 / 导出 |
| [zkonikishi/Minecraft-Blockbench-MCP](https://github.com/zkonikishi/Minecraft-Blockbench-MCP) | 建模 / 贴图 / 骨骼动画 |

> **注意**：Blockbench 官方插件仓库**不允许插件使用 AI 功能**，
> 所以这类插件只能从 URL 加载，装不进插件市场。

## 4.5 本项目自己的工具

| 脚本 | 用途 |
|---|---|
| `tools/validate_mc_skin.py` | **校验器** —— 尺寸 / 模式 / 第一层 36 面是否全不透明 |
| `tools/build_mc_skin_v2.py` | **手绘生成器** —— 代码逐像素画（最可控） |
| `tools/fix_block_skin.py` | **白层修复** —— 清掉第二层的近白背景 |
| `tools/render_skin_preview.py` | **预览渲染** —— 合成第二层后拼正/侧/背 |
| `tools/check_matte_rule.py` | 哑光色机制检测 |

---

# 五、我们踩过的坑（实测，都已修）

| # | 坑 | 现象 | 根因 | 修法 |
|---|---|---|---|---|
| 1 | **第二层全白** | 角色在游戏里是一坨白块 | 模型输出 RGB 无 alpha，把该透明的填成白色 | 清掉第二层近白像素 |
| 2 | **slim 包围盒误报** | 校验说"第一层被破坏"，其实没有 | slim 手臂 3px 宽，左臂区第 46–48 列本就不使用 | 改成**逐面**检查 |
| 3 | **512×512 当皮肤用** | 导入报格式错误 | 生图模型输出尺寸非法 | NEAREST 降到 64×64 |
| 4 | **LANCZOS 缩放** | 像素风全糊 | 混色 | 必须 NEAREST |
| 5 | **skin-spec 的坐标错误** | 按文档写会得到 `y2<y1` 的非法矩形 | 原文印刷错误 | 本文档第一节已修正 |
| 6 | **空提示词 + guidance=1.0** | 输出纯白空图，但脚本报"成功" | FLUX 关掉 CFG 会塌成空白 | guidance 必须 4.0；加空图检测 |
| 7 | **404 的预览图 URL** | 静默回退到模型自带示例，生成的不是目标角色 | 未验证 URL 存在性 | 加输入来源断言 |

**这七个坑的共同点：没有一个会报错。** 静默失败比报错危险得多 ——
所以校验器必须**主动检查**，不能只看"跑完了没有"。

---

# 六、一句话总结

> **合法性靠规范**（尺寸 64×64、第一层不透明、第二层按需透明），
> **好看靠设计**（8×8 的脸是硬上限、第二层做体积、3–4 档明暗），
> **不出错靠校验**（主动查，别信"跑完了"）。

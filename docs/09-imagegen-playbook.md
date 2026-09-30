# LYCO · 生图经验手册

> 本项目全部生图实测经验的沉淀。**可直接照着做。**
> 模型评价见 [08-model-evaluation.md](08-model-evaluation.md)，提示词库见 [../prompts/library.md](../prompts/library.md)

---

## 一、四条核心原则

### 原则 1 · 先分资产类型，再选工具

| 资产类型 | 输出特征 | 正确工具 |
|---|---|---|
| **自由构图类** | 立绘、氛围图、概念图、表情 | ✅ 生图 |
| **固定几何类** | MC 皮肤（64×64 UV）、Spine 图集（碎片矩形）、图集带 | ❌ 生图 → **写代码** |

**这是本项目最贵的一课。** 在 MC 皮肤上耗了很久，根源是**用自由构图的工具去做固定几何的活**。

生图模型**不产出固定几何**——它输出的是它认为好看的构图。
你要 64×64 UV 布局，它给你一张"看起来像皮肤图集"的示意图。**永远对不上。**

### 原则 2 · 否定句比肯定句重要

R1–R9 里**九条有七条是否定**（无文字 / 无徽章 / 无边框 / 不冷漠 / 不是装饰…）。

**发现**：模型对「不要什么」的遵守度，**低于**对「要什么」的遵守度。
所以否定项必须**单独成段、全大写、用 ABSOLUTELY NO 开头**，才有效。

### 原则 3 · 参考图必须给，但别指望它守设计

**实测**：给了三视图参考，豆包依然把黑发红内层的 Lyco 画成**银白长发**。

原因：一张参考图的约束力，**远小于**模型「二次元黑军装少女」这个强先验。

**对策**：
- 参考图**要给**（至少能定风格）
- 关键特征**用文字再钉一遍**（发色写 hex、发夹写形状和位置）
- 要真正守住 → **训 LoRA**（见原则 4）

### 原则 4 · 想守住原创角色，只有 LoRA

提示词写得再好，也压不过先验。**唯一的解法是让模型认识她。**

---

## 二、可复用否定块（★ 最重要的资产）

**每次生图都把这句原样贴到提示词末尾。**

```
ABSOLUTELY NO text, letters, numbers, captions, labels, watermark, signature,
border, frame, grid lines, colour swatches, background scenery, floor shadow,
badges, medals, epaulettes or emblems of any kind.
```

**为什么这串有效**（逐项对应我们踩过的坑）：

| 片段 | 挡住的坑 |
|---|---|
| `text, letters, numbers, captions, labels` | 模型爱写标题/说明 |
| `watermark, signature` | 右下角爱"签名" |
| `border, frame` | 爱加画框 |
| `grid lines, colour swatches` | **把 design sheet 理解成带色卡的图表**（高频翻车） |
| `background scenery` | 爱加背景风景 |
| `floor shadow` | 爱加地面投影 |
| `badges, medals, epaulettes, emblems` | `military` 一词触发的先验（违反 R2） |

---

## 三、关键措辞对照表

**同一个意思，换个说法效果差很多。**

| 你想要 | ❌ 别这么写 | ✅ 这么写 |
|---|---|---|
| 不笑 | `calm` | `relaxed closed mouth, NO smile` |
| 半垂眼 | `cold eyes` | `large soft eyes with the **upper eyelids slightly lowered**` |
| 黑白分明 | `high contrast` | `crisp line art, clear rim light separating hair from clothing` |
| 兵器要大 | `a weapon` | `a **huge** mechanical scythe, blade longer than her body` |
| 纯色底 | `simple background` | `plain flat pure white background` |
| 全身入画 | `full body` | `full body from head to feet, centred in frame` |
| 纤细 | `thin` | `slender, narrow shoulders, about 1.4 head-widths` |

**规律**：具体的**解剖/几何描述** > 形容词。
`upper eyelids slightly lowered` 远比 `cold` 有效。

---

## 四、失败模式速查表

| 现象 | 原因 | 对策 |
|---|---|---|
| 出现文字 / 签名 | 模型默认行为 | 否定块 |
| 出现色卡 / 网格 | 把 design sheet 理解成图表 | `no colour swatches, no grid lines` |
| 自加徽章 / 肩章 | `military` 先验 | `no badges, medals, epaulettes, emblems` |
| **画成微笑** | anime 默认表情 | `relaxed closed mouth, NO smile` |
| **眼睛上挑** | anime 默认眼型 | `upper eyelids slightly lowered` |
| **发色变白 / 变银** | 参考图遵循失效 | 提示词写发色 hex；根治要 LoRA |
| 加了金饰 / 纹章 | 模型"华丽军装"先验（Gemini 尤甚） | 换模型 + 否定块 |
| 兵器画小 | 默认比例 | 明写 `huge` / `oversized` |
| 黑发黑衣糊一起 | 缺轮廓光 | `crisp line art` + 要求边缘光 |
| 输出不是 64×64 | **模型不产固定几何** | **改走代码** |
| 多张之间不一致 | 无身份锁定 | LoRA |
| 四视图朝向乱 | 无姿势控制 | ControlNet OpenPose |

---

## 五、尺寸与宽高比

| 用途 | 尺寸 | 比例 | 说明 |
|---|---|---|---|
| 全身立绘 | 1024×1536 | 2:3 | |
| 战斗立绘 | 1024×1536 | 2:3 | |
| 三视图 / 精灵表 | 3072×1024 | 3:1 | **模型上限就是 3:1** |
| 方形概念图 | 1024×1024 | 1:1 | |
| 超长条（如图集带） | — | **>3:1 做不到** | 必须先 3:1 生成，再代码裁切/对齐 |

> ⚠️ **宽高比超过 3:1 的资产，生图直接放弃。** 武器图集带（786×121 ≈ 6.5:1）就是这么解决的：
> 先生成 3:1 的（杆身居中），再用代码缩放到目标宽度并吸附到中心线。

---

## 六、成本与时间（实测）

| 项 | 数值 |
|---|---|
| 单张耗时 | **85–125 秒** |
| 单张成本 | **$0.03** |
| 一轮（3 张） | 约 5 分钟 / $0.09 |
| 命令 | `oma image generate --vendor codex --size WxH --out DIR -y --format json -r REF1 -r REF2 "PROMPT"` |

**建议节奏**：一次出 1–3 张，**别批量刷**。
每张都要按 R1–R9 逐条检查，废图重出比批量刷便宜。

---

## 七、标准工作流

```
1. 写提示词
   ├── 主体描述（人设特征，尽量具体到解剖/几何）
   ├── 构图（尺寸、朝向、背景）
   ├── 风格（cel shading / line art / palette）
   └── 否定块（原样贴）

2. 挂 1–2 张参考图（-r）
   └── 优先用「三视图」，其次「立绘」

3. 出一版 → 按 R1–R9 逐条自查
   ├── 有文字/徽章/边框？→ 废
   ├── 笑了 / 眼睛上挑？→ 废
   ├── 发色不对？→ 改措辞重出
   └── 通过 → 收

4. 改的时候「一次只改一处措辞」
   └── 别同时改三处，否则不知道哪句起作用

5. ★ 设计稿与生产资产分开对待
   ├── 设计稿：容忍不精确，用来定方向
   └── 生产资产：必须精确 → 写代码
```

---

## 八、各类资产的实操结论

| 资产 | 结论 |
|---|---|
| 三视图 | 生图 + 人工筛选；**作为设计基准，不是生产资产** |
| 全身 / 战斗立绘 | 生图可用 ✅ |
| Q 版精灵表 | 生图可用 ✅（但各姿势比例会飘，需筛选） |
| 表情差分 | 生图可用 ✅ |
| 武器三形态 | 生图可用 ✅ |
| **武器图集带（>3:1）** | 生图出 3:1，**代码**缩放到目标并吸附中心线 |
| **MC 皮肤（64×64 UV）** | ⚠️ **修正**：直接出图集做不到；但**两阶段管线可以** —— 见下节 |
| **Spine 图集（碎片矩形）** | **代码按 UV 矩形替换** ❌ 生图 |
| 直播待机动画 | Live2D 绑定 ❌ 生图 |
| 3D 模型 | 建模 + 重定向 ❌ 生图 |

### ★ 修正：MC 皮肤并非「生图做不到」

本手册初版写的「MC 皮肤必须写代码」**不完整**。
后续调研找到 [BLOCK 论文](https://arxiv.org/abs/2603.03964) 与已开源的
[AliceKJ/BLOCKv0.6](https://huggingface.co/AliceKJ/BLOCKv0.6)，证明**两阶段管线可行**：

```
① MLLM 出 3D 预览图（正/背双联斜视角）  ← 自由构图，MLLM 擅长
        ↓
② image-to-image 模型解码成皮肤图集      ← BLOCKv0.6
```

**关键差别**：不要让模型**直接出皮肤图集**（那是它不擅长的固定几何任务），
而是让它出 **3D 预览**（自由构图），再交给专门的解码模型。

提示词与完整管线：**[../prompts/minecraft-skin.md](../prompts/minecraft-skin.md)**

**仍然成立的部分**：直接让模型出「皮肤图集」得到的只是**示意排版**，无法导入游戏。

---

## 九、一句话总结

> **生图负责「好看」，代码负责「准确」。**
>
> 想要原创角色在任何管线里都保持身份统一 —— **训 LoRA，别调提示词。**

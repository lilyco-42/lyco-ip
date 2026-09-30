# Minecraft 皮肤 · 提示词与管线

> **核心结论（来自 [BLOCK 论文](https://arxiv.org/abs/2603.03964) 的实测验证）：**
> **不要让模型直接出皮肤图集。** 分两阶段：
> **① 出 3D 预览图（正/背双联斜视角）→ ② 解码成皮肤图集。**
>
> 第一阶段是「自由构图」，MLLM 擅长；第二阶段交给专门的 image-to-image 模型。

---

## 路线 A（★ 推荐）· 两阶段

```
① GPT 出 3D 预览图          ← 本文 A1 提示词
        ↓
② BLOCKv0.6 解码成皮肤       ← AliceKJ/BLOCKv0.6（HuggingFace，已开源）
        ↓
③ 校验 64×64 RGBA 并导入
```

### A1 · 第一阶段提示词（GPT 生图用这个）

**尺寸** `1024x1024` ｜ **参考** 三视图 + Q 版精灵表

```
【角色特征块 —— 见 library.md 第 0.1 节，原样贴】

A DUAL-PANEL Minecraft character preview of the character described above.

LAYOUT
  Two panels side by side on a plain flat pure white background, separated by
  clear empty space.
  LEFT  panel — the character seen from the FRONT, the whole body rotated about
                30 degrees to one side (three-quarter oblique view).
  RIGHT panel — the SAME character seen from the BACK, rotated about 30 degrees
                the other way.
  Both panels show the FULL BODY from head to feet, at exactly the SAME size
  and the SAME camera height. Both are lit identically. Nothing else is in the
  frame.

STYLE
  The character is rendered as if she were a Minecraft player SKIN worn on a
  blocky Minecraft player model: visible BOXY limbs, a CUBIC head, flat
  unshaded pixel-art colours, HARD PIXEL EDGES, no anti-aliasing, no gradients,
  no soft shading, no rim light, no cast shadow.

COLOUR
  Every region must be a FLAT SOLID fill of a single colour, with the boundary
  between two colours being a hard step — because these colours will be sampled
  back into a 64×64 skin texture and any gradient or blur will destroy the
  result. Use only the palette of charcoal black, deep crimson red, warm white,
  gunmetal silver and pale skin.

SILHOUETTE
  The silhouette must stay clearly readable against the white background: the
  short bob hair, the X hairpin, the jacket edge, the asymmetric skirt panel
  and the boots must each be distinguishable as separate flat colour blocks.

ABSOLUTELY NO text, letters, numbers, captions, labels, arrows, measurement
lines, character names, watermark, signature, border, frame, grid lines,
colour swatches, background scenery, floor shadow, drop shadow, badges, medals,
epaulettes or emblems of any kind.

ALSO NO: skin texture atlas, UV layout, unwrapped texture sheet, flat texture
map, or any 2D texture diagram. This must be a 3D RENDERED PREVIEW, not a
texture sheet.
```

**为什么最后那段「ALSO NO」是关键**：不加这句，模型会自作聪明地给你画一张"皮肤图集"（就是你之前遇到的那张），而图集是第二阶段才产出的东西。**第一阶段只要 3D 预览。**

### A2 · 第二阶段（BLOCKv0.6）

用 [AliceKJ/BLOCKv0.6](https://huggingface.co/AliceKJ/BLOCKv0.6) 把 A1 的预览图转成 64×64 皮肤贴图。
它是公开的 image-to-image 模型，输入 = 3D 预览，输出 = 皮肤纹理文件。

---

## 路线 B · 直接出图集（★ 仅用于看设计方向）

> ⚠️ **产出的是"示意排版"，不是 64×64 UV 图集，无法直接导入游戏。**
> 唯一的合法用途是**看设计方向**，真正的皮肤仍需代码逐像素画。

### B1 · 像素网格锁定提示词

**关键技巧**：明确告诉模型「每个皮肤像素 = 整数倍图像像素」，这样降采样才是无损的。
我们之前失败就是因为模型画的是**非网格对齐**的高分图（实测自相关无干净周期）。

```
A Minecraft character skin texture atlas, drawn EXACTLY on a 64×64 pixel grid
and scaled up to the canvas by an EXACT INTEGER factor (each skin pixel
becomes a perfect square of identical image pixels).

GRID RULES
  Every skin pixel is a hard-edged square of the SAME size. Column boundaries
  fall at exactly 1/64, 2/64, 3/64 ... of the canvas width; row boundaries at
  exactly 1/64, 2/64, 3/64 ... of the canvas height. NO anti-aliasing, NO
  sub-pixel edges, NO blur, NO soft transitions anywhere in the image. Zooming
  in must reveal a perfect checkerboard of flat squares.

LAYOUT (standard Minecraft 64x64 skin, in skin-pixel coordinates)
  Head  main layer  — region (0,0) to (32,16):
      (8,0)-(16,8)    head TOP      = hair seen from above
      (16,0)-(24,8)   head BOTTOM   = neck skin
      (0,8)-(8,16)    head RIGHT    = profile, hair over ear
      (8,8)-(16,16)   head FRONT    = the FACE with both eyes
      (16,8)-(24,16)  head LEFT     = profile, hair over ear
      (24,8)-(32,16)  head BACK     = hair only
  Head  overlay      — same six faces repeated at (32,0) to (64,16)
  Torso main layer   — region (16,16) to (40,32)
  Torso overlay      — region (16,32) to (40,48)
  Right arm main     — region (40,16) to (56,32)
  Right arm overlay  — region (40,32) to (56,48)
  Right leg main     — region (0,16) to (16,32)
  Right leg overlay  — region (0,32) to (16,48)
  Left  leg main     — region (16,48) to (32,64)
  Left  leg overlay  — region (0,48) to (16,64)
  Left  arm main     — region (32,48) to (64,64)
  Left  arm overlay  — region (48,48) to (64,64)

CONTENT
【角色特征块 —— 见 library.md 第 0.1 节】

The face at (8,8)-(16,16) is the single most important tile: it must show the
grey half-lidded eyes, the relaxed closed mouth and the white X hairpin, using
the full 8x8 pixels.

MATERIALS AND COLOUR
  Flat solid colours only. NO gradients, NO shading ramps, NO dithering, NO
  outlines around the tiles. Use only charcoal black, deep crimson red, warm
  white, gunmetal silver, pale skin and dark grey tights.

ABSOLUTELY NO text, letters, numbers, captions, labels, watermark, signature,
border, frame, grid lines drawn on top of the art, colour swatches, colour
palette strips, background scenery, badges, medals, epaulettes or emblems of
any kind.
```

### B2 · 出图后的正确用法

1. 检查它是否**真的按 64×64 网格画**（放大看方块是否等大对齐）
2. 若对齐 → 用 **NEAREST** 降采样到 64×64（无损）
3. 若**没对齐** → 放弃，不要用 LANCZOS/BOX 硬压（会糊成我们之前那样）

**判别方法**：把图放大 8 倍看边缘。边缘是**硬台阶** → 对齐了；边缘有**灰色过渡带** → 没对齐。

---

## 路线 C · 代码逐像素画（★ 唯一保证可导入）

已实现：`tools/build_mc_skin_v2.py`

**适用场景**：需要**保证能导入游戏**、且要精确控制每一个像素时。

**优点**：100% 合法 64×64 RGBA，可复现，可版本管理
**缺点**：手感靠手写像素矩阵，细节受 8×8 的脸所限

**建议**：**A 路线出设计 → C 路线落地**。
用 A 拿到好看的 3D 预览确定方向，再用 C 把它精确画成能用的皮肤。

---

## 三条路线的分工

| 路线 | 产出 | 能直接导入？ | 用途 |
|---|---|---|---|
| **A** | 3D 预览 + BLOCKv0.6 解码 | ✅（经 BLOCKv0.6） | **推荐主路径** |
| **B** | 示意排版图集 | ❌ | 只看设计方向 |
| **C** | 代码生成的 64×64 | ✅ | 精确落地、可复现 |

---

## 附：Blockbench 工具链（本仓库相关）

调研结论：**Blockbench 有 MCP，也有无头 CLI**，可用于模型/UV/贴图/动画的自动化。

| 用途 | 命令 / 入口 |
|---|---|
| 桌面插件（HTTP MCP） | 插件 URL：`https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`，服务端 `http://localhost:3000/bb-mcp` |
| **无头模式（无需开 Blockbench）** | `npx -y github:jasonjgardner/blockbench-mcp-plugin --root ./models` |
| **Shell 脚本直接调单个工具** | `bun run headless/call.ts --root ./models bbmodel_edit @ops.json` |
| 模型读写 / 编辑 / 贴图 | `bbmodel_create` `bbmodel_edit` `bbmodel_add_texture`（含替换图片、面 UV） |
| 渲染 | `bbmodel_render` `bbmodel_contact_sheet`（内置 WebGPU，需 Node ≥ 23.6 + GPU） |
| 导出 | `bbmodel_export_bedrock_geometry` `bbmodel_export_java_block` `bbmodel_export_modded_entity` |
| 校验 | `bbmodel_validate` `bbmodel_validate_animations` |

**备选实现**（同类，可对比）：
[sosadly/blockbench-mcp](https://github.com/sosadly/blockbench-mcp) ·
[Ru1n-dev/ruins-blockbench-mcp](https://github.com/Ru1n-dev/ruins-blockbench-mcp) ·
[zkonikishi/Minecraft-Blockbench-MCP](https://github.com/zkonikishi/Minecraft-Blockbench-MCP) ·
[FFriends/Blockbench-MCP](https://github.com/FFriends/Blockbench-MCP)（Codex-ready）

> **注意**：Blockbench 官方插件仓库**不允许插件使用 AI 功能**，
> 所以这类插件必须从 URL 加载，不能从插件市场装。

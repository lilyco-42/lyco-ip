# LYCO · 提示词库

> 全部为**实测有效**的提示词，可直接复制使用。
>
> **做 Minecraft 皮肤请看单独一份：[minecraft-skin.md](minecraft-skin.md)**（两阶段管线 + Blockbench 工具链）
> 配套：[生图经验手册](../docs/09-imagegen-playbook.md) ｜ [出图铁律](../docs/05-art-rules.md)

---

## 0. 通用否定块（★ 每段提示词末尾都要贴）

```
ABSOLUTELY NO text, letters, numbers, captions, labels, watermark, signature,
border, frame, grid lines, colour swatches, background scenery, floor shadow,
badges, medals, epaulettes or emblems of any kind.
```

## 0.1 角色特征块（★ 每段提示词开头都要贴）

把这段放在最前面，用来钉住身份：

```
The character is an original anime girl with EXACTLY this design:
short black bob hair (#121016) with a heavy crimson red inner layer (#8E1B24)
showing through the tips, and one small white X-shaped hairpin on the right
side of the bangs; a calm aloof face with large soft grey eyes (#8E8A96) whose
upper eyelids are slightly lowered, and a relaxed closed mouth with NO smile;
a short fitted black double-breasted military jacket (#18181E) with thin
crimson piping, small silver buttons and a thin black belt with a small silver
O-ring; an asymmetric layered black skirt with deep crimson lining flaring
where the panels separate; sheer dark grey tights (#46424E); and mid-calf
black boots with red trim and thick red soles.
```

## 0.2 调用方式

```bash
oma image generate --vendor codex --size 1024x1536 \
  --out "OUT_DIR/name" -y --format json \
  -r "design/three-view/lyco_three_view.png" \
  "【特征块】+【构图段】+【风格段】+【否定块】"
```

---

## 1. 三视图（设计基准）

**尺寸** `3072x1024` ｜ **参考** 三视图旧版 或 立绘

```
【特征块】

Three orthographic views side by side — FRONT view, SIDE view, and BACK view —
all full body from head to feet, drawn at exactly the same scale and evenly
spaced on a plain flat light grey background. In every view she stands calmly
with her weight relaxed on one leg, arms relaxed at her sides, holding nothing.
Her upper body is completely still and composed while a light wind lifts the
long skirt panels and the hair tips to one side.

Clean simple anime illustration, soft cel shading, crisp line art, soft even
lighting, limited palette of charcoal black, deep crimson red, warm white and
gunmetal silver.

【否定块】
```

---

## 2. 全身立绘 · 正面站姿

**尺寸** `1024x1536` ｜ **参考** 三视图

```
【特征块】

She stands calmly with her weight relaxed on one leg, one hand lightly holding
the upper part of a slim long black rod weapon that has a circular red
mechanical hub at its top end and is resting on the ground beside her. A light
wind lifts the long skirt panels and the hair tips to one side while her upper
body stays completely still and composed. Full body from head to feet, centred
in frame, on a plain flat pure white background.

Clean simple anime illustration, soft cel shading, crisp line art, soft even
lighting, limited palette of charcoal black, deep crimson red, warm white and
gunmetal silver.

【否定块】
```

---

## 3. 战斗立绘 · 红色闪光

**尺寸** `1024x1536` ｜ **参考** 三视图

```
【特征块】

A dramatic full-body action illustration caught mid-technique. Her whole body
is rendered as a sharp black and crimson AFTERIMAGE streaking horizontally
across the frame, trailing long bands of red light and speed streaks, the
silhouette breaking apart into MOTION STREAKS at the edges — while her calm
half-lidded face stays READABLE and sharp at the centre of the blur. She holds
a huge red and black mechanical scythe whose long shaft sweeps horizontally and
whose crescent blade curves upward, the blade edge glowing faint crimson.
Dynamic diagonal composition, high speed, strong red rim light. Plain flat pure
white background.

The red light must be SHARP, ANGULAR STREAKS — never a soft round glow.

Clean anime game illustration, crisp hard edges, limited palette of charcoal
black, deep crimson red, warm white and gunmetal silver.

【否定块】
```

---

## 4. Q 版精灵表 · 9 姿势

**尺寸** `3072x1024` ｜ **参考** 三视图

```
【特征块】

A 2D game sprite sheet of the SAME character drawn in a small super-deformed
CHIBI style with a big head and a small body. Lay the poses out as many
separate, clearly separated figures in a tidy grid on a plain flat pure white
background with generous empty space between them — all figures the SAME size
and the SAME drawing style.

Include these nine poses, each as its own separate figure: standing idle facing
the front; standing idle facing the side; walking with one leg forward; running
at speed; jumping in the air; crouching low; a light forward attack swing;
holding a long slim black rod weapon upright; and lying knocked down on the
ground.

Clean anime game sprite art, crisp cel shading, clear silhouettes, soft even
lighting.

【否定块】
```

---

## 5. 表情差分

**尺寸** `2048x1024` ｜ **参考** 三视图

```
【特征块】

A character expression sheet: the SAME head-and-shoulders portrait repeated
four times in a single row at exactly the same size, same angle and same
lighting, on a plain flat pure white background. Only the face changes between
them — everything else is IDENTICAL.

Panel 1  the default: grey eyes with the upper eyelids slightly lowered, mouth
         relaxed and closed, NO smile — this is her neutral state
Panel 2  faint surprise: the eyes opened 1-2 pixels wider, the mouth UNCHANGED
Panel 3  eyes fully closed, a plain blink with no other expression change
Panel 4  side glance: only the pupils turn to one side, the head does NOT move

Clean simple anime illustration, soft cel shading, crisp line art.

【否定块】
```

---

## 6. 武器三形态

**尺寸** `3072x1024` ｜ **参考** 三视图

```
A weapon design sheet showing the SAME mechanical rod in THREE forms, laid out
left to right on a plain flat pure white background, all at the same visual
scale:

LEFT     STOWED form  — a short portable baton about one forearm long, with a
         circular red mechanical hub at one end, compact and clean
CENTRE   RIFLE form   — the rod extended into a long rifle about 1.2 times a
         human height, with a slim barrel, silver joints and the red hub
RIGHT    SCYTHE form  — a huge red and black mechanical scythe, shaft longer
         than a human body, with a large upward-curving crescent blade whose
         edge glows faint crimson

The shaft is slim matte black (#121218). The joints are small silver metal
(#C8CCD0). The red circular mechanical core (#B62833) is the ONLY permanently
lit element. Materials are MATTE — do not render mirror-like reflections.

Clean anime mechanical design illustration, crisp line art, limited palette of
charcoal black, deep crimson red and gunmetal silver.

【否定块】
```

---

## 7. Minecraft 皮肤设计稿（★ 仅作设计参考，不可直接导入）

**尺寸** `1024x1024` ｜ **参考** 三视图

> ⚠️ **生图产出的是"示意排版"，不是 64×64 UV 图集，无法直接导入游戏。**
> 真正的皮肤必须用代码逐像素画（见 `tools/build_mc_skin_v2.py`）。
> 这段提示词只用于**看设计方向**。

```
A Minecraft character skin texture sheet, pixel art, laid out in the standard
Minecraft 64x64 skin atlas layout: the top-left 8x8 block is the head front
face, surrounded by the head right, left, back, top and bottom faces; below
that the body front, back, right and left faces; then the right arm and right
leg in the same manner; and the left arm and left leg in the lower-left area.

【特征块】

Strict pixel art, crisp hard pixel edges, no anti-aliasing, flat colours only,
no shading gradients, no outlines.

【否定块】
```

---

## 8. 通用修改指令（迭代用）

出图后想微调，**一次只改一处**：

| 想改什么 | 追加这句 |
|---|---|
| 发色不对 | `Her hair must be BLACK with a crimson red inner layer — NOT white, NOT silver, NOT blonde.` |
| 笑了 | `Her mouth is a flat relaxed closed line. She is NOT smiling.` |
| 眼睛太凶 | `The upper eyelids are lowered, giving a calm and detached look — NOT a glare.` |
| 红太多 | `Reduce the red to under 20% of the image. Red appears only on the skirt lining, the hair underside and the boot soles.` |
| 加了装饰 | `Remove all decorative elements. The outfit is plain and minimal.` |
| 兵器太小 | `Make the weapon MUCH larger — the blade should be longer than her whole body.` |
| 有背景 | `Plain flat pure white background with nothing else in it.` |

---

## 9. 已产出的成品（可直接复用为参考图）

| 用途 | 参考图路径 |
|---|---|
| **首选参考** | `design/three-view/lyco_three_view.png` |
| 脸部细节 | `design/three-view/lyco_three_view_face_zoom.png` |
| 全身比例 | `design/illustration/lyco_fullbody_stand.png` |
| 动态风格 | `design/illustration/lyco_action_redflash.png` |
| Q 版风格 | `design/illustration/lyco_chibi_sheet_9pose.png` |
| 武器 | `design/weapon/lyco_weapon_scythe.png` |


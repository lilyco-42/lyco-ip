# LYCO · IP 资源库

> 原创角色 **Lyco** 的完整设计资产、形象规范与衍生开发基准。
> 所有下游产出（插画 / Live2D / 3D / 游戏模组 / 直播挂件 / 周边）**必须**以本仓库为唯一基准。

---

## 一句话认识她

> 一个穿黑色短款军装的少女，短黑发下藏着一层暗红。
> 她站着的时候像一张照片 —— 上半身一动不动，只有裙摆和发梢在走。
> 她动起来的时候，红色才从衣服里面透出来。
> 她不太看人，不是傲慢，是觉得没必要。

**核心锚点：静态的秩序，动态的锋芒。**

---

## 快速导航

| 我想… | 去看 |
|---|---|
| 认识这个角色 | [docs/01-character.md](docs/01-character.md) |
| 拿色值 | [docs/02-palette.md](docs/02-palette.md) ｜ [配色卡 PNG](design/palette/lyco_palette_card.png) |
| 画她 / 建模 | [docs/03-visual-spec.md](docs/03-visual-spec.md) ｜ [三视图](design/three-view/lyco_three_view.png) |
| **知道怎么让别人一眼认出这是 Lyco** | **[docs/07-recognition-anchors.md](docs/07-recognition-anchors.md)** |
| 做挂件 / 周边 / 直播素材 | [docs/04-accessories.md](docs/04-accessories.md) |
| 用 AI 出图 | [docs/05-art-rules.md](docs/05-art-rules.md) |
| **选哪个生图模型** | **[docs/08-model-evaluation.md](docs/08-model-evaluation.md)** |
| **生图怎么不出错** | **[docs/09-imagegen-playbook.md](docs/09-imagegen-playbook.md)** ｜ [提示词库](prompts/library.md) |
| **做 Minecraft 皮肤** | **[prompts/minecraft-skin.md](prompts/minecraft-skin.md)** |
| **皮肤格式规范 / 工具生态** | **[docs/11-minecraft-skin-spec-and-tools.md](docs/11-minecraft-skin-spec-and-tools.md)** |
| 找具体文件 | [docs/06-assets.md](docs/06-assets.md) |

---

## 仓库结构

```
lyco-ip/
├── docs/                       形象规范（文字，唯一权威）
│   ├── 01-character.md           核心人设 · 三条灵魂规则
│   ├── 02-palette.md             配色指南（含 hex 表）
│   ├── 03-visual-spec.md         外形 / 服装 / 表情 / 动作
│   ├── 04-accessories.md         挂件与配饰规范
│   ├── 05-art-rules.md           出图铁律 R1–R9
│   ├── 06-assets.md              资产清单
│   ├── 07-recognition-anchors.md 识别锚点体系（五层）
│   ├── 08-model-evaluation.md   生图模型评价与管线选择
│   ├── 09-imagegen-playbook.md   生图经验手册（可照做）
│   ├── 10-mc-skin-blockv0.6-实测.md  BLOCKv0.6 实测记录
│   └── 11-minecraft-skin-spec-and-tools.md ★ 皮肤规范与工具生态
├── design/                     设计基准图（只读，勿改）
│   ├── three-view/               三视图（★ 最高权威）
│   ├── palette/                  配色卡
│   ├── illustration/             立绘 / Q 版精灵表
│   ├── expression/               表情差分
│   ├── action/                   动作关键帧
│   ├── weapon/                   武器三形态
│   └── layers/                   立绘分层拆件
├── platform/                   各平台落地资产
│   ├── minecraft/                Minecraft 皮肤（64×64）
│   ├── live2d/                   Live2D / Inochi2D（预留）
│   └── streaming/                直播挂件 / 装饰（预留）
├── prompts/                    提示词库（实测有效，可直接复制）
│   ├── library.md                通用提示词（立绘/表情/武器/精灵表…）
│   └── minecraft-skin.md         ★ MC 皮肤两阶段管线 + Blockbench 工具链
├── tools/                      生成脚本（可复现）
└── LICENSE.md                  使用许可 —— 动手前先读
```

---

## 三条灵魂规则（不可违背）

1. **高冷 = 安静，不是冷漠。** 靠「没有情绪起伏」演，不靠压眉眼绷嘴角。
2. **极小的身体动作，极大的攻击效果。** 幅度给在兵器与裙摆上，身体本体尽量小。
3. **光从衣服里面透出来。** 红色是运动的结果，不是装饰。

---

## 识别锚点（别人凭什么一眼认出她）

**五层锚点，每层至少一个** —— 这样无论被缩小、换风格、裁切还是动起来，总有一层活下来。

| 层级 | 锚点 | 什么情况下起作用 |
|---|---|---|
| **L1 剪影** | 不对称裙（长片**固定在她右侧**）+ 长杆 + 窄肩 | 远距离、纯黑剪影 |
| **L2 色块** | **上黑下红** —— 红永远从下/内透出 | 缩小、模糊 |
| **L3 细节** | **白色 X 发夹**（右侧刘海、倾斜 15°） | 特写、头像 |
| **L4 动态** | **黑红锐利残影**（不是柔和光晕）+ 脸保持清晰 | 动画、游戏 |
| **L5 行为** | **上半身静止、下半身流动** | 任何动态媒介 |

**做减法时的保留顺序**：L2 → L3 → L1 → L4 → L5。
保住**前两条**就还能被认出。

完整规格 + 自检要求见 **[docs/07-recognition-anchors.md](docs/07-recognition-anchors.md)**。

---

## 使用许可（摘要）

本仓库为**原创角色 IP**。设计基准图（`design/`）**仅供参照，不得直接商用或二次分发**。
衍生创作请先读 [LICENSE.md](LICENSE.md)。

---

## 版本

`v1.0` ｜ 设计基准：三视图 v3





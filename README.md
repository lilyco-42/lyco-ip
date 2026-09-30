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
| 做挂件 / 周边 / 直播素材 | **[docs/04-accessories.md](docs/04-accessories.md)** |
| 用 AI 出图 | [docs/05-art-rules.md](docs/05-art-rules.md) |
| 找具体文件 | [docs/06-assets.md](docs/06-assets.md) |

---

## 仓库结构

```
lyco-ip/
├── docs/                       形象规范（文字，唯一权威）
│   ├── 01-character.md           核心人设 · 三条灵魂规则
│   ├── 02-palette.md             配色指南（含 hex 表）
│   ├── 03-visual-spec.md         外形 / 服装 / 表情 / 动作
│   ├── 04-accessories.md         ★ 挂件与配饰规范
│   ├── 05-art-rules.md           出图铁律 R1–R9
│   └── 06-assets.md              资产清单
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
├── tools/                      生成脚本（可复现）
└── LICENSE.md                  使用许可 —— 动手前先读
```

---

## 三条灵魂规则（不可违背）

1. **高冷 = 安静，不是冷漠。** 靠「没有情绪起伏」演，不靠压眉眼绷嘴角。
2. **极小的身体动作，极大的攻击效果。** 幅度给在兵器与裙摆上，身体本体尽量小。
3. **光从衣服里面透出来。** 红色是运动的结果，不是装饰。

---

## 使用许可（摘要）

本仓库为**原创角色 IP**。设计基准图（`design/`）**仅供参照，不得直接商用或二次分发**。
衍生创作请先读 [LICENSE.md](LICENSE.md)。

---

## 版本

`v1.0` ｜ 设计基准：三视图 v3

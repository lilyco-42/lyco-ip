# LYCO · 出图铁律

> **用 AI 出图 / 委托画师 / 自己做图，都适用。**
> 违反任何一条 = 废稿。

---

## 铁律 R1–R9

| 编号 | 规则 | 说明 |
|---|---|---|
| **R1** | **无文字** | 无字母、数字、标题、说明、水印、签名 |
| **R2** | **无徽章** | 无勋章、奖章、肩章、臂章、绶带、国徽类元素 |
| **R3** | **无边框** | 无画框、蓝图感、档案卡、网格线、分割线、色卡 |
| **R4** | **简约舒适风** | 干净、不堆砌装饰；不做华丽特效 |
| **R5** | **原配色** | 只用 [配色指南](02-palette.md) 的色值，不加新色 |
| **R6** | **高冷 = 安静** | 半垂眼、放松嘴、面部肌肉全松 |
| **R7** | **不是冷漠** | 不画皱眉 / 瞪眼 / 嘴角下压 / 咬牙 |
| **R8** | **小动作 · 大效果** | 动作幅度给在兵器与裙摆上，身体本体尽量小 |
| **R9** | **红是结果不是原因** | 红色只作内衬 / 滚边 / 运动残影，不做表面花纹 |

---

## AI 出图提示词模板

### 通用角色图

```
A single full-body illustration of the original character shown in the attached
character design sheet. Reproduce her design EXACTLY:

HAIR   short black bob with a heavy crimson red inner layer showing through the
       tips and a small white X-shaped hairpin on the right side of the bangs
FACE   calm aloof expression, large soft grey eyes with the upper eyelids
       slightly lowered, relaxed closed mouth, NO smile
OUTFIT short fitted black double-breasted military jacket with thin crimson
       piping, small silver buttons, a high collar and a thin black belt with a
       small silver O-ring; asymmetric layered black skirt with deep crimson
       lining flaring where the panels separate; sheer dark grey tights;
       mid-calf black boots with red trim and thick red soles
WEAPON a long slim matte-black mechanical rod with a round crimson core
SETTING plain flat white background, full body head to feet, centred
STYLE  clean simple anime illustration, soft cel shading, crisp line art,
       limited palette of charcoal black / deep crimson / warm white / gunmetal

ABSOLUTELY NO text, letters, numbers, captions, labels, watermark, signature,
border, frame, grid lines, colour swatches, background scenery, badges, medals,
epaulettes or emblems of any kind.
```

### 要点提醒

| 容易翻车的点 | 提示词里怎么写 |
|---|---|
| AI 默认会画笑 | 明写 `relaxed closed mouth, NO smile` |
| AI 默认眼睛上挑 | 明写 `upper eyelids slightly lowered` |
| AI 会加勋章 | 明写 `no badges, medals, epaulettes` |
| AI 会加背景 | 明写 `plain flat white background, no scenery` |
| AI 会加画框/色卡 | 明写 `no frame, no grid lines, no colour swatches` |
| 黑发黑衣服糊一起 | 明写 `crisp line art` + 要求边缘高光 |

---

## 出图后自查

- [ ] 画面里有任何文字吗？（包括 AI 自己"签"的名）
- [ ] 有徽章 / 肩章 / 勋章吗？
- [ ] 有边框 / 网格 / 色卡残留吗？
- [ ] 眼睛是半垂的吗？还是在瞪人？
- [ ] 她笑了吗？（笑了就是废稿）
- [ ] 红色占了多少？超过 25% 基本是错的
- [ ] 黑衣服和黑头发分得开吗？
- [ ] 兵器够大吗？（要能和纤细的身体形成反差）
- [ ] 色值都在配色指南里吗？
- [ ] X 发夹在吗？形状是 X 吗？

---

## 已知 AI 出图陷阱（实测）

| 陷阱 | 现象 | 对策 |
|---|---|---|
| **色板污染** | AI 会在画面角落画色卡 / 网格 | 提示词明写禁止；出图后裁掉 |
| **签名** | 右下角出现类签名笔迹 | 同上 |
| **过度装饰** | 自动加蕾丝、肩章、花纹 | 反复强调 `simple, no decoration` |
| **表情跑偏** | 默认画成微笑 | 强调 `NO smile` |
| **比例失真** | 兵器画得和身体同宽 | 强调 `huge mechanical weapon` |
| **色调漂移** | 出现蓝、紫、金等杂色 | 明确列出四色 palette |

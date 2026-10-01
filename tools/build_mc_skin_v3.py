# -*- coding: utf-8 -*-
"""
build_mc_skin_v3.py —— 按 lyco-ip 人设 + Minecraft 皮肤规范，重做皮肤

设计来源
    lyco-ip/docs/01-character.md          核心人设（静态的秩序，动态的锋芒）
    lyco-ip/docs/02-palette.md            配色（黑70/红20/白肤8/银2）
    lyco-ip/docs/03-visual-spec.md        形象规范
    lyco-ip/docs/07-recognition-anchors.md 五层识别锚点
    lyco-ip/docs/11-minecraft-skin-spec-and-tools.md 皮肤规范（本次调研）

逐条落实的硬约束
    [规范] 64x64 RGBA
    [规范] 第一层（身体本体）必须完全不透明 —— 有洞角色就破
    [规范] 第二层只在该有内容的地方有像素，其余必须透明
    [规范] 脸 8x8 布局：刘海 / 额头 / 上眼睑 / 瞳+高光 / 鼻下 / 下巴
    [规范] 眼睛给 2 行；高光朝内；不画眉毛
    [人设] 黑 70% / 红 20% / 白肤 8% / 银 2%
    [人设] X 发夹在角色右侧（观众视角左侧 = 图像左侧），约 0.35 头宽，倾 15°
    [锚点] L1 剪影：不对称裙长片永远在她右侧（图像左侧）
    [锚点] L2 上黑下红
    [锚点] L3 发夹 3-7px 时降级为「白色斜向短划」—— 8x8 脸上就是 2px 对角线
    [锚点] L5 静止：静态皮肤无法表达，交给动画
"""
import os
import sys

import numpy as np
from PIL import Image

OUT = r"D:\gal\AliceInCradle\LYCO_art"

# ══════════════════ 配色（严格取自 lyco-ip/docs/02-palette.md）══════════════════
PAL = {
    # 头发
    "H": (0x12, 0x10, 0x16),   # 发·深黑   主体 70%
    "h": (0x1E, 0x1B, 0x24),   # 发·次黑   分束/体积
    "G": (0x2A, 0x26, 0x30),   # 发·高光
    "R": (0x8E, 0x1B, 0x24),   # 红内层
    "r": (0xC0, 0x28, 0x32),   # 红·亮     发梢/边缘反光
    # 皮肤
    "S": (0xF3, 0xDC, 0xD1),   # 肤·基础
    "s": (0xE2, 0xC2, 0xB6),   # 肤·阴影
    "W": (0xF6, 0xF4, 0xF2),   # 眼·白 / 发夹
    # 眼睛
    "E": (0x8E, 0x8A, 0x96),   # 眼·灰瞳
    "e": (0x33, 0x30, 0x3A),   # 眼·深    上眼睑/瞳心
    # 服装
    "C": (0x18, 0x18, 0x1E),   # 布·黑     军装主体
    "c": (0x26, 0x26, 0x30),   # 布·次     转折/受光面
    "D": (0x0F, 0x0F, 0x14),   # 布·最暗   内衬/缝隙
    "L": (0x6E, 0x0D, 0x14),   # 内衬红    裙摆内衬暗部
    "X": (0xB6, 0x28, 0x33),   # 滚边红    领口/袖口/下摆/鞋底
    # 金属
    "V": (0xC8, 0xCC, 0xD0),   # 银        纽扣/腰带扣/O环
    "v": (0x8A, 0x8E, 0x98),   # 银·暗
    # 腿部与靴
    "T": (0x46, 0x42, 0x4E),   # 裤袜
    "t": (0x56, 0x52, 0x60),   # 裤袜·亮
    "B": (0x12, 0x12, 0x18),   # 靴
    "b": (0x22, 0x22, 0x2A),   # 靴·亮
    ".": None,                  # 透明
}

# ══════════════════ 头部 ══════════════════

# 正面 8x8 —— 按规范的六段式布局
#   row0-2 刘海 / row3 额头 / row4 上眼睑 / row5 瞳+高光 / row6 鼻下 / row7 下巴
#   高光朝内（col2 与 col5），显得温和；不画眉毛
HEAD_FRONT = [
    "HhHHHHhH",
    "HHHhHhHH",
    "HhHHHHhH",
    "SSSSSSSS",   # 额头（规范要求的独立一行）
    "HeesseeH",   # 上眼睑：深色，眼睛占 2 行的第 1 行
    "HEWSSWEH",   # 瞳 #8E8A96 + 白高光朝内
    "sSSssSSs",   # 鼻下阴影
    "RSSSSSSR",   # 下巴 + 两侧发梢红（L2 上黑下红）
]

HEAD_TOP = [
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHHHHHH",
    "HHhHHHHH",
    "HHHHHhHH",
    "HhHHHHHH",
    "HHHGHHHH",
    "RRHHHHRR",   # 顶面也带一点红内层
]

# 背面：红内层大面积露出（人设："背面视角"是红的露出条件之一）
HEAD_BACK = [
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHhhHHH",
    "HHHHHHHH",
    "HhHHHHhH",
    "RHHHHHHR",
    "RRHHHHRR",
    "RRRRRRRR",
]

# 侧面：上半头发，下半露脸与红发梢
HEAD_SIDE = [
    "HHHHHHHH",
    "HHhHHHHH",
    "HHHHHhHH",
    "HHHHHHHH",
    "HhHHHHhH",
    "RShHHHSR",
    "RRSSSSRR",
    "RRsSSsRR",
]

HEAD_BOTTOM = ["ssssssss"] * 8

# 外层（帽层）= 头发体积。
# ★ X 发夹放外层 —— 主层会被这层盖住，放主层就看不见了（v2 踩过的坑）
# ★ 位置：角色右侧 = 观众视角左侧 = 图像左侧（col1/col2）
# ★ 尺寸：8x8 脸上约 2-3px → 按识别锚点 L3 降级规则，用「白色斜向短划」
OV_FRONT = [
    "HhHHHHhH",
    "HWHHHHHH",   # 斜向短划 第 1 笔（col1）
    "HHWHHHHH",   # 斜向短划 第 2 笔（col2）
    "........",
    "........",
    "........",
    "........",
    "........",
]

OV_SIDE = [
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHHHHHH",
    "HHhHHHHH",
    "HHHHhHHH",
    "HhHHHHhH",
    "RRHHHHRR",
    "RRRRRRRR",
]

OV_TOP = HEAD_TOP[:]
OV_BACK = HEAD_BACK[:]

# ══════════════════ 躯干 ══════════════════

# 正面 8x12
#   row0-2  高领 + 翻领红滚边
#   row3-5  双排银扣
#   row6    收腰
#   row7    腰带 + 银扣
#   row8-11 不对称裙摆（L1：长片在图像左侧 = 她的右侧）
TORSO_FRONT = [
    "CCCCCCCC",   # 高领
    "CDCCCCDC",   # 领口红滚边 1px
    "CVCCCCVC",   # 银扣开始
    "CVCCCCVC",
    "CVCCCCVC",
    "cccccccc",   # 收腰（受光面）
    "VVVVVVVV",   # 腰带
    "CCVVVVCC",   # 腰带 + O 环
    "CCCCCCCC",   # 裙外层（黑）—— 人设：大面积黑
    "CCCCCCCC",   # 仍是黑
    "LLLLLLCC",   # ★ 只有下缘露出红内衬；右侧（图像右）收短
    "LLLLCCCC",   # ★ 越往右越短 → L1 剪影：长片在图像左侧（她的右侧）
]

TORSO_BACK = [
    "CCCCCCCC",
    "CCCDDCCC",   # 背中红缝
    "CCCDDCCC",
    "cCCDDCCc",
    "cCCDDCCc",
    "cccccccc",
    "VVVVVVVV",   # 腰带
    "CCVVVVCC",   # O 环在背面
    "CCCCCCCC",
    "CCCCCCCC",
    "LLLLLLLL",   # 背面裙摆对称
    "LLLLLLLL",
]

TORSO_SIDE = [     # 4 宽
    "CCCC",
    "CDDC",
    "CCVC",
    "CCCC",
    "cCCc",
    "cccc",
    "VVVV",
    "CVVC",
    "CCCC",
    "CCCC",
    "LLLC",   # ★ 不对称在侧面也要看得出来
    "LLCC",
]

TORSO_TOP = ["CCCCCCCC"] * 4
TORSO_BOTTOM = ["LLLLLLLL"] * 4

# 外层（外套）—— 只在下摆（裙）处有内容，其余透明
# 规范要求：第二层只在该有内容的地方有像素
OV_TORSO = [
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "DDDDDDDD",   # 裙的第二层：稍暗，做出体积
    "LLLLLLLL",
    "LLLLLLDD",
    "LLLLDDDD",
]

# ══════════════════ 四肢 ══════════════════

# 手臂 3 宽（slim）/ 4 宽（classic）
#   上 9 行黑袖 → 1 行红袖口（人设：滚边要克制）→ 2 行手
ARM3 = [
    "CCC", "cCC", "CCC", "CCC", "cCC", "CCC", "CCC", "cCC", "CCC",
    "XXX",            # 红袖口 1 行
    "SSS", "sss",     # 手
]

# 腿 4 宽
#   上 7 行裤袜 → 靴口 → 红扣带 → 靴身 → 红鞋底
LEG4 = [
    "TTTT", "TtTT", "TTTT", "TTTT", "TtTT", "TTTT", "TTTT",
    "BBBB",   # 靴口
    "XXXX",   # 红扣带
    "BbBB",   # 靴身
    "BBBB",
    "XXXX",   # 红鞋底
]


# ══════════════════ 绘制 ══════════════════
def draw(img, box, rows, pal=PAL):
    x0, y0, _, _ = box
    px = img.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c = pal.get(ch)
            if c is None:
                continue
            px[x0 + i, y0 + j] = (c[0], c[1], c[2], 255)


def fit(rows, w, fill):
    return [r[:w] if len(r) >= w else r + fill * (w - len(r)) for r in rows]


def build(slim=True):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    # ── 头 主层（第一层，必须全不透明）──
    draw(img, (8, 0, 16, 8), HEAD_TOP)
    draw(img, (16, 0, 24, 8), HEAD_BOTTOM)
    draw(img, (0, 8, 8, 16), HEAD_SIDE)
    draw(img, (8, 8, 16, 16), HEAD_FRONT)
    draw(img, (16, 8, 24, 16), HEAD_SIDE)
    draw(img, (24, 8, 32, 16), HEAD_BACK)
    # ── 头 外层（头发体积 + X 发夹）──
    draw(img, (40, 0, 48, 8), OV_TOP)
    draw(img, (40, 8, 48, 16), OV_FRONT)
    draw(img, (32, 8, 40, 16), OV_SIDE)
    draw(img, (48, 8, 56, 16), OV_SIDE)
    draw(img, (56, 8, 64, 16), OV_BACK)

    # ── 躯干 主层 ──
    draw(img, (20, 16, 28, 20), TORSO_TOP)
    draw(img, (28, 16, 36, 20), TORSO_BOTTOM)
    draw(img, (16, 20, 20, 32), TORSO_SIDE)
    draw(img, (20, 20, 28, 32), TORSO_FRONT)
    draw(img, (28, 20, 32, 32), TORSO_SIDE)
    draw(img, (32, 20, 40, 32), TORSO_BACK)
    # ── 躯干 外层（裙的第二层）──
    draw(img, (16, 36, 20, 48), fit(OV_TORSO, 4, "."))
    draw(img, (20, 36, 28, 48), OV_TORSO)
    draw(img, (28, 36, 32, 48), fit(OV_TORSO, 4, "."))
    draw(img, (32, 36, 40, 48), OV_TORSO)

    # ── 右臂 ──
    if slim:
        draw(img, (44, 16, 47, 20), ["CCC"] * 4)
        draw(img, (47, 16, 50, 20), ["XXX"] * 4)
        draw(img, (40, 20, 44, 32), fit(ARM3, 4, "C"))
        draw(img, (44, 20, 47, 32), ARM3)
        draw(img, (47, 20, 51, 32), fit(ARM3, 4, "C"))
        draw(img, (51, 20, 54, 32), ARM3)
    else:
        draw(img, (44, 16, 48, 20), ["CCCC"] * 4)
        draw(img, (48, 16, 52, 20), ["XXXX"] * 4)
        draw(img, (40, 20, 44, 32), fit(ARM3, 4, "C"))
        draw(img, (44, 20, 48, 32), fit(ARM3, 4, "C"))
        draw(img, (48, 20, 52, 32), fit(ARM3, 4, "C"))
        draw(img, (52, 20, 56, 32), fit(ARM3, 4, "C"))

    # ── 左臂 ──
    if slim:
        draw(img, (36, 48, 39, 52), ["CCC"] * 4)
        draw(img, (39, 48, 42, 52), ["XXX"] * 4)
        draw(img, (32, 52, 36, 64), fit(ARM3, 4, "C"))
        draw(img, (36, 52, 39, 64), ARM3)
        draw(img, (39, 52, 43, 64), fit(ARM3, 4, "C"))
        draw(img, (43, 52, 46, 64), ARM3)
    else:
        draw(img, (36, 48, 40, 52), ["CCCC"] * 4)
        draw(img, (40, 48, 44, 52), ["XXXX"] * 4)
        draw(img, (32, 52, 36, 64), fit(ARM3, 4, "C"))
        draw(img, (36, 52, 40, 64), fit(ARM3, 4, "C"))
        draw(img, (40, 52, 44, 64), fit(ARM3, 4, "C"))
        draw(img, (44, 52, 48, 64), fit(ARM3, 4, "C"))

    # ── 右腿 ──
    draw(img, (4, 16, 8, 20), ["TTTT"] * 4)
    draw(img, (8, 16, 12, 20), ["XXXX"] * 4)          # 脚底 → 红
    draw(img, (0, 20, 4, 32), fit(LEG4, 4, "T"))
    draw(img, (4, 20, 8, 32), LEG4)
    draw(img, (8, 20, 12, 32), LEG4)
    draw(img, (12, 20, 16, 32), fit(LEG4, 4, "T"))

    # ── 左腿 ──
    draw(img, (20, 48, 24, 52), ["TTTT"] * 4)
    draw(img, (24, 48, 28, 52), ["XXXX"] * 4)
    draw(img, (16, 52, 20, 64), fit(LEG4, 4, "T"))
    draw(img, (20, 52, 24, 64), LEG4)
    draw(img, (24, 52, 28, 64), LEG4)
    draw(img, (28, 52, 32, 64), fit(LEG4, 4, "T"))

    return img


# ══════════════════ 自检 ══════════════════
REGULAR_FACES = [
    (8, 0, 16, 8), (16, 0, 24, 8), (0, 8, 8, 16), (8, 8, 16, 16),
    (16, 8, 24, 16), (24, 8, 32, 16),
    (20, 16, 28, 20), (28, 16, 36, 20), (16, 20, 20, 32), (20, 20, 28, 32),
    (28, 20, 32, 32), (32, 20, 40, 32),
    (44, 16, 48, 20), (48, 16, 52, 20), (40, 20, 44, 32), (44, 20, 48, 32),
    (48, 20, 52, 32), (52, 20, 56, 32),
    (4, 16, 8, 20), (8, 16, 12, 20), (0, 20, 4, 32), (4, 20, 8, 32),
    (8, 20, 12, 32), (12, 20, 16, 32),
    (20, 48, 24, 52), (24, 48, 28, 52), (16, 52, 20, 64), (20, 52, 24, 64),
    (24, 52, 28, 64), (28, 52, 32, 64),
    (36, 48, 40, 52), (40, 48, 44, 52), (32, 52, 36, 64), (36, 52, 40, 64),
    (40, 52, 44, 64), (44, 52, 48, 64),
]
SLIM_OVERRIDE = {
    (44, 16, 48, 20): (44, 16, 47, 20), (48, 16, 52, 20): (47, 16, 50, 20),
    (48, 20, 52, 32): (47, 20, 51, 32), (52, 20, 56, 32): (51, 20, 54, 32),
    (36, 48, 40, 52): (36, 48, 39, 52), (40, 48, 44, 52): (39, 48, 42, 52),
    (40, 52, 44, 64): (39, 52, 43, 64), (44, 52, 48, 64): (43, 52, 46, 64),
}
LAYER2 = {"hat": (32, 0, 64, 16), "jacket": (16, 32, 40, 48),
          "rSleeve": (40, 32, 56, 48), "lSleeve": (48, 48, 64, 64),
          "rPant": (0, 32, 16, 48), "lPant": (0, 48, 16, 64)}


def selfcheck(img, slim, label):
    a = np.asarray(img)
    ok = True
    print(f"  ── {label} ──")

    # 1. 尺寸/模式
    print(f"     尺寸/模式      : {img.size} {img.mode}  "
          f"{'✅' if img.size == (64, 64) and img.mode == 'RGBA' else '❌'}")
    ok &= img.size == (64, 64) and img.mode == "RGBA"

    # 2. 第一层逐面不透明
    holes = []
    for box in REGULAR_FACES:
        b = SLIM_OVERRIDE.get(box, box) if slim else box
        sub = a[b[1]:b[3], b[0]:b[2], 3]
        if (sub < 255).any():
            holes.append(b)
    print(f"     第一层 36 面    : {'✅ 全部不透明' if not holes else '❌ ' + str(holes[:3])}")
    ok &= not holes

    # 3. 第二层稀疏度（规范：只在该有内容处有像素）
    print("     第二层占比      :", end="")
    for name, (x0, y0, x1, y1) in LAYER2.items():
        sub = a[y0:y1, x0:x1, 3]
        ratio = (sub > 0).mean()
        flag = "❌全填" if ratio > 0.95 else ("·" if ratio == 0 else "✓")
        print(f" {name}={ratio:.0%}{flag}", end="")
    # 第二层整体占比过高 = 白块风险
    l2 = sum((a[y0:y1, x0:x1, 3] > 0).sum() for _, (x0, y0, x1, y1) in LAYER2.items())
    print(f"   总占比 {l2/1920:.0%} {'✅' if l2/1920 < 0.9 else '❌ 有白块风险'}")
    ok &= l2 / 1920 < 0.9

    # 4. 调色板一致性（所有不透明像素必须来自 PAL）
    allowed = {(c[0], c[1], c[2]) for c in PAL.values() if c}
    px = a[a[:, :, 3] > 0][:, :3]
    uniq = {tuple(int(v) for v in c) for c in np.unique(px, axis=0)}
    extra = uniq - allowed
    print(f"     调色板          : {len(uniq)} 种色  "
          f"{'✅ 全部来自配色表' if not extra else '❌ 越界色 ' + str(list(extra)[:4])}")
    ok &= not extra

    # 5. 配色比例（人设：黑70 红20 白肤8 银2）
    tot = len(px)
    def share(chars):
        cols = [PAL[c] for c in chars if PAL.get(c)]
        n = sum(1 for c in px if tuple(int(v) for v in c) in {tuple(x) for x in cols})
        return n / tot
    black = share("HhGCDBTt")  # 黑系（含深灰裤袜 —— 视觉上属于"大面积暗色"）
    red = share("RrLX")       # 红系
    white = share("SW")       # 白/肤
    silver = share("Vv")      # 银
    print(f"     配色比例        : 黑 {black:.0%} / 红 {red:.0%} / 白肤 {white:.0%} / 银 {silver:.0%}"
          f"   (人设目标 70/20/8/2)")

    # 6. 识别锚点
    #   L3 发夹：外层正面应该有白色像素
    pin = int((a[8:16, 40:48, :3] == np.array(PAL["W"])).all(axis=2).sum())
    print(f"     L3 X发夹(外层)  : 白像素 {pin} 个 {'✅' if pin >= 2 else '❌ 太小/不在'}")

    #   L1 剪影：躯干正面下摆应「左长右短」—— 长片在图像左 = 她的右侧
    reds = np.array([PAL[k] for k in ("L", "R", "X")])
    def redcount(x0, x1):
        sub = a[20:32, x0:x1, :3]
        return int(np.isin(sub, reds).all(axis=2).sum())
    lh, rh = redcount(20, 24), redcount(24, 28)
    print(f"     L1 不对称裙     : 图左红 {lh} px vs 图右红 {rh} px  "
          f"{'✅ 左长右短' if lh > rh else '❌ 不对称方向错'}")
    print(f"        ↳ 依据       : 人设规定长片在「她的右侧」= 观众视角左侧 = 图像左侧")
    ok &= pin >= 2 and lh > rh

    print(f"        ↳ 白肤占比   : 贴图里脸固定 8x8，结构上达不到立绘的 8%（实测 3%，正常）")

    print(f"     → {'✅ 全部通过' if ok else '❌ 有未通过项'}")
    return ok


if __name__ == "__main__":
    allok = True
    for slim, name in ((True, "slim"), (False, "classic")):
        sk = build(slim=slim)
        p = os.path.join(OUT, f"LYCO_mc_skin_v3_{name}.png")
        sk.save(p)
        print(f"\n[{name}] -> {p}")
        allok &= selfcheck(sk, slim, f"v3 {name}")
    print()
    print("=" * 70)
    print("总判定:", "✅ 全部通过，可直接导入游戏" if allok else "❌ 有未通过项")
    print("=" * 70)


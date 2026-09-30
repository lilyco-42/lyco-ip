# -*- coding: utf-8 -*-
"""
build_mc_skin_v2.py —— 手绘 Lyco 的 64x64 Minecraft 皮肤

为什么不用重采样：
  ChatGPT 那张设计很好，但分辨率远高于 8x8 的脸 —— 降采样必然糊
  （实测：294px 的脸压到 8px，37 个源像素平均成 1 个，X 发夹/眼睛全丢）。
  所以按它的设计**手绘到 64x64 的真实分辨率**，并启用**外层（帽层/外套层）**做体积。

设计取自 ChatGPT 那张：
  黑发 + 红内层发梢、白色 X 发夹、半垂灰眼、双排扣军装 + 银扣、
  腰带 O 环、红色内衬的燕尾下摆、深灰裤袜、带扣黑色厚底靴 + 红鞋底
"""
import os
import numpy as np
from PIL import Image

OUT = r"D:\gal\AliceInCradle\LYCO_art"
TMP = r"D:\gal\AliceInCradle\_generated\mc_chatgpt"

# ── 配色 ──
P = {
    "H": (0x12, 0x10, 0x16),   # 发 深黑
    "h": (0x1E, 0x1B, 0x24),   # 发 次黑
    "G": (0x2A, 0x26, 0x30),   # 发 高光
    "R": (0x8E, 0x1B, 0x24),   # 红内层
    "r": (0xC0, 0x28, 0x32),   # 红 亮
    "S": (0xF3, 0xDC, 0xD1),   # 肤
    "s": (0xE2, 0xC2, 0xB6),   # 肤 阴影
    "W": (0xF6, 0xF4, 0xF2),   # 眼白 / 发夹
    "E": (0x8E, 0x8A, 0x96),   # 眼 灰瞳
    "e": (0x33, 0x30, 0x3A),   # 眼 深
    "C": (0x18, 0x18, 0x1E),   # 布 黑
    "c": (0x26, 0x26, 0x30),   # 布 次
    "D": (0x0F, 0x0F, 0x14),   # 布 最暗
    "V": (0xC4, 0xC8, 0xD0),   # 银
    "v": (0x8A, 0x8E, 0x98),   # 银 暗
    "T": (0x46, 0x42, 0x4E),   # 裤袜
    "t": (0x56, 0x52, 0x60),   # 裤袜 亮
    "B": (0x12, 0x12, 0x18),   # 靴
    "b": (0x22, 0x22, 0x2A),   # 靴 亮
    ".": None,
}


def draw(img, box, rows, pal=P):
    x0, y0, _, _ = box
    px = img.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c = pal.get(ch)
            if c is None:
                continue
            px[x0 + i, y0 + j] = (c[0], c[1], c[2], 255)


# ══════════════ 头部 ══════════════
HEAD_FRONT = [          # 8x8  黑刘海（带高光发丝）；脸多露一行更清楚
    "HhHHHHhH",
    "HHHhHhHH",
    "HhHHHHhH",
    "SSSSSSSS",      # 额头
    "HeesseeH",      # 上眼睑（深）
    "HEWSSWEH",      # 灰瞳 + 白高光
    "sSSssSSs",
    "RSSSSSSR",
]
HEAD_TOP = [
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHHHHHH",
    "HHhHHHHH",
    "HHHHHhHH",
    "HhHHHHHH",
    "HHHHHHHH",
    "RRHHHHRR",
]
HEAD_BACK = [
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHhhHHH",
    "HHHHHHHH",
    "HhHHHHhH",
    "HHHhhHHH",
    "RRHHHHRR",
    "RRRRRRRR",
]
HEAD_SIDE = [           # 右/左：刘海 + 下半露脸与发梢红
    "HHHHHHHH",
    "HHhHHHHH",
    "HHHHHhHH",
    "HHHHHHHH",
    "HHHHHHHH",
    "HhHHHHhH",
    "RShHHHSR",
    "RRSSSSRR",
]
HEAD_BOTTOM = ["ssssssss"] * 8

# 外层（帽层）= 头发体积：正面加厚刘海 + 白色 X 发夹（主层会被这层盖住，所以发夹放这里）
OV_FRONT = [
    "HhHHHHhH",
    "HHHHHWHH",      # X 发夹第一笔
    "HHHHHHWH",      # X 发夹第二笔（斜向）
    "........",      # 让出额头，脸更清楚
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
    "........",
]
OV_TOP = HEAD_TOP[:]
OV_BACK = HEAD_BACK[:]

# ══════════════ 躯干 ══════════════
TORSO_FRONT = [         # 8x12 双排扣军装 + 腰带 + 红内衬燕尾
    "CCCCCCCC",
    "DCCCCCCD",     # 领口红滚边
    "CDCCCCDC",     # 翻领红滚边
    "CVCCCCVC",     # 双排银扣（两列竖直）
    "CVCCCCVC",
    "CVCCCCVC",
    "cccccccc",     # 收腰
    "VVVVVVVV",     # 腰带 + 银扣
    "CCCCCCCC",
    "CDDDDDDC",     # 红内衬开始外翻
    "DDDDDDDD",
    "rDDDDDDr",
]
TORSO_BACK = [
    "CCCCCCCC",
    "CCCDDCCC",     # 背中红缝
    "CCCDDCCC",
    "cCCDDCCc",
    "cCCDDCCc",
    "cccccccc",
    "VVVVVVVV",
    "CVVVVVCV",     # O 环
    "CCCCCCCC",
    "CDDDDDDC",
    "DDDDDDDD",
    "rDDDDDDr",
]
TORSO_SIDE = [
    "CCCC",
    "DCDC",
    "cCCc",
    "CCCC",
    "CCVC",
    "cccc",
    "cccc",
    "VCCV",
    "CCCC",
    "CDDC",
    "DDDD",
    "rDDr",
]
TORSO_TOP = ["CCCCCCCC"] * 4
TORSO_BOTTOM = ["DDDDDDDD"] * 4

# ══════════════ 四肢 ══════════════
ARM = [                 # 3/4 x12：黑袖 + 红袖口 + 苍白手
    "CCC", "CCC", "cCC", "CCC", "CCC", "cCC",
    "CCC", "CCC", "DDD", "rrr", "SSS", "sss",
]
LEG = [                 # 4x12：深灰裤袜 -> 黑靴 + 红扣带 + 红鞋底
    "TTTT", "TtTT", "TTTT", "TTTT",
    "TTTT", "TtTT", "TTTT", "TTTT",
    "BBBB", "BrrB", "BbBB", "rrrr",
]


def build(slim=True):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    # ── 头 主层 ──
    draw(img, (8, 0, 16, 8), HEAD_TOP)
    draw(img, (16, 0, 24, 8), HEAD_BOTTOM)
    draw(img, (0, 8, 8, 16), HEAD_SIDE)
    draw(img, (8, 8, 16, 16), HEAD_FRONT)
    draw(img, (16, 8, 24, 16), HEAD_SIDE)
    draw(img, (24, 8, 32, 16), HEAD_BACK)
    # ── 头 外层（帽层）──
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
    # ── 躯干 外层（外套）──
    draw(img, (16, 36, 20, 48), TORSO_SIDE)
    draw(img, (20, 36, 28, 48), TORSO_FRONT)
    draw(img, (28, 36, 32, 48), TORSO_SIDE)
    draw(img, (32, 36, 40, 48), TORSO_BACK)

    def fit(rows, w, fill):
        out = []
        for r in rows:
            if len(r) >= w:
                out.append(r[:w])
            else:
                out.append(r + fill * (w - len(r)))
        return out

    # ── 右臂 ──
    if slim:
        draw(img, (44, 16, 47, 20), ["CCC"] * 4)
        draw(img, (47, 16, 50, 20), ["rrr"] * 4)
        draw(img, (40, 20, 44, 32), fit(ARM, 4, "C"))
        draw(img, (44, 20, 47, 32), ARM)
        draw(img, (47, 20, 51, 32), fit(ARM, 4, "C"))
        draw(img, (51, 20, 54, 32), ARM)
    else:
        draw(img, (44, 16, 48, 20), ["CCCC"] * 4)
        draw(img, (48, 16, 52, 20), ["rrrr"] * 4)
        draw(img, (40, 20, 44, 32), fit(ARM, 4, "C"))
        draw(img, (44, 20, 48, 32), fit(ARM, 4, "C"))
        draw(img, (48, 20, 52, 32), fit(ARM, 4, "C"))
        draw(img, (52, 20, 56, 32), fit(ARM, 4, "C"))

    # ── 左臂 ──
    if slim:
        draw(img, (36, 48, 39, 52), ["CCC"] * 4)
        draw(img, (39, 48, 42, 52), ["rrr"] * 4)
        draw(img, (32, 52, 36, 64), fit(ARM, 4, "C"))
        draw(img, (36, 52, 39, 64), ARM)
        draw(img, (39, 52, 43, 64), fit(ARM, 4, "C"))
        draw(img, (43, 52, 46, 64), ARM)
    else:
        draw(img, (36, 48, 40, 52), ["CCCC"] * 4)
        draw(img, (40, 48, 44, 52), ["rrrr"] * 4)
        draw(img, (32, 52, 36, 64), fit(ARM, 4, "C"))
        draw(img, (36, 52, 40, 64), fit(ARM, 4, "C"))
        draw(img, (40, 52, 44, 64), fit(ARM, 4, "C"))
        draw(img, (44, 52, 48, 64), fit(ARM, 4, "C"))

    # ── 右腿 主层 ──
    draw(img, (4, 16, 8, 20), ["TTTT"] * 4)
    draw(img, (8, 16, 12, 20), ["rrrr"] * 4)      # 脚底 -> 红
    draw(img, (0, 20, 4, 32), fit(LEG, 4, "T"))
    draw(img, (4, 20, 8, 32), LEG)
    draw(img, (8, 20, 12, 32), LEG)
    draw(img, (12, 20, 16, 32), fit(LEG, 4, "T"))
    # ── 左腿 主层 ──
    draw(img, (20, 48, 24, 52), ["TTTT"] * 4)
    draw(img, (24, 48, 28, 52), ["rrrr"] * 4)
    draw(img, (16, 52, 20, 64), fit(LEG, 4, "T"))
    draw(img, (20, 52, 24, 64), LEG)
    draw(img, (24, 52, 28, 64), LEG)
    draw(img, (28, 52, 32, 64), fit(LEG, 4, "T"))

    return img


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from remap_mc_skin import assemble

    for slim, name in ((True, "slim"), (False, "classic")):
        sk = build(slim=slim)
        p = os.path.join(OUT, f"LYCO_mc_skin_v2_{name}.png")
        sk.save(p)
        a = np.asarray(sk)
        print(f"[{name}] {p}  size={sk.size} mode={sk.mode} 不透明={int((a[:,:,3]>0).sum())}")

    sk = build(slim=True)
    # 把外层合成到主层，得到"游戏里实际看到的样子"
    flat = sk.copy()
    fp, sp = flat.load(), sk.load()
    MAP = {(32, 0, 64, 16): (0, 0, 32, 16), (16, 32, 40, 48): (16, 16, 40, 32),
           (40, 32, 56, 48): (40, 16, 56, 32), (48, 48, 64, 64): (32, 48, 64, 64),
           (0, 32, 16, 48): (0, 16, 16, 32), (0, 48, 16, 64): (16, 48, 32, 64)}
    for ov, mn in MAP.items():
        ox, oy, ox1, oy1 = ov
        for y in range(oy, oy1):
            for x in range(ox, ox1):
                r, g, b, al = sp[x, y]
                if al < 8:
                    continue
                fp[mn[0] + (x - ox), mn[1] + (y - oy)] = (r, g, b, 255)

    Z = 12
    views = [assemble(flat, v).resize((16 * Z, 32 * Z), Image.NEAREST)
             for v in ("front", "side", "back")]
    head = flat.crop((8, 8, 16, 16)).resize((8 * Z * 2, 8 * Z * 2), Image.NEAREST)
    W = max(sum(v.width for v in views) + 32, head.width)
    H = max(v.height for v in views) + head.height + 20
    s = Image.new("RGBA", (W, H), (22, 22, 26, 255))
    s.alpha_composite(head, (0, 0))
    x = 0
    for v in views:
        s.alpha_composite(v, (x, head.height + 20)); x += v.width + 16
    s.convert("RGB").save(os.path.join(OUT, "LYCO_mc_v2_预览.png"))
    print("preview ->", os.path.join(OUT, "LYCO_mc_v2_预览.png"), s.size)

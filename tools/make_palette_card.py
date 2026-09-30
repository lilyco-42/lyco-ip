# -*- coding: utf-8 -*-
"""make_palette_card.py —— 生成 Lyco 配色卡（带色值标注）"""
import os
from PIL import Image, ImageDraw

OUT = r"D:\gal\AliceInCradle\LYCO_art"
W, H = 1400, 1230
BG = (18, 18, 21)
CARD = (28, 28, 33)
LINE = (52, 52, 60)
TXT = (226, 226, 232)
DIM = (140, 140, 150)
ACC = (200, 40, 51)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def font(sz, bold=False):
    for name in (("msyhbd.ttc" if bold else "msyh.ttc"), "simhei.ttf", "arial.ttf"):
        try:
            from PIL import ImageFont
            return ImageFont.truetype(name, sz)
        except Exception:
            continue
    from PIL import ImageFont
    return ImageFont.load_default()


F_TITLE = font(38, True)
F_H = font(24, True)
F_L = font(19)
F_S = font(16)
F_MONO = font(18)

d.text((48, 36), "LYCO  ·  配色指南", font=F_TITLE, fill=TXT)
d.text((48, 88), "配色人物形象指南 — 全部色值可直接取用", font=F_S, fill=DIM)
d.line([48, 128, W - 48, 128], fill=LINE, width=2)

GROUPS = [
    ("头发  HAIR", [
        ("发·深黑",     "#121016", "主体，占发色 70%"),
        ("发·次黑",     "#1E1B24", "分束、体积"),
        ("发·高光",     "#2A2630", "发丝高光"),
        ("红内层",      "#8E1B24", "藏在发下的红外层"),
        ("红·亮",       "#C02832", "发梢、边缘反光"),
    ]),
    ("皮肤  SKIN", [
        ("肤·基础",     "#F3DCD1", "脸、手、颈"),
        ("肤·阴影",     "#E2C2B6", "下颌、颈下"),
        ("眼·白",       "#F6F4F2", "眼白、发夹"),
        ("眼·灰瞳",     "#8E8A96", "瞳色（高冷灰）"),
        ("眼·深",       "#33303A", "上眼睑、瞳心"),
    ]),
    ("服装  OUTFIT", [
        ("布·黑",       "#18181E", "军装主体"),
        ("布·次",       "#262630", "转折、受光面"),
        ("布·最暗",     "#0F0F14", "内衬、缝隙"),
        ("内衬红",      "#6E0D14", "裙摆内衬暗部"),
        ("滚边红",      "#B62833", "领口/袖口/下摆"),
    ]),
    ("腿部与靴  LEGS", [
        ("裤袜",        "#46424E", "深灰丝袜"),
        ("裤袜·亮",     "#565260", "腿部高光"),
        ("靴",          "#121218", "靴身"),
        ("靴·亮",       "#22222A", "靴面反光"),
        ("靴底红",      "#B62833", "鞋底、扣带"),
    ]),
    ("金属  METAL", [
        ("银",          "#C8CCD4", "纽扣、腰带扣、O 环"),
        ("银·暗",       "#8A8E98", "金属阴影"),
    ]),
]

y = 156
COLW = (W - 96 - 24) // 2
cur = [y, y]          # 两列各自的游标
for gi, (gname, items) in enumerate(GROUPS):
    col = gi % 2
    x = 48 + col * (COLW + 24)
    yy = cur[col]
    d.text((x, yy), gname, font=F_H, fill=ACC)
    yy += 38
    for name, hexv, usage in items:
        c = tuple(int(hexv[i:i + 2], 16) for i in (1, 3, 5))
        d.rounded_rectangle([x, yy, x + 62, yy + 52], 6, fill=c, outline=LINE)
        d.text((x + 76, yy + 4), name, font=F_L, fill=TXT)
        d.text((x + 76, yy + 28), f"{hexv}   {usage}", font=F_S, fill=DIM)
        yy += 56
    cur[col] = yy + 22

# 底部规则区
y = max(cur) + 6
d.line([48, y, W - 48, y], fill=LINE, width=2)
y += 20
d.text((48, y), "设计铁律", font=F_H, fill=ACC)
y += 38
RULES = [
    ("R1  无文字 · R2  无徽章/勋章/肩章 · R3  无边框/蓝图/档案风", TXT),
    ("R4  简约舒适风 · R5  原配色（黑 / 深红 / 暖白 / 枪灰）· R6  高冷 = 安静，不是冷漠", TXT),
    ("配色比例   黑 ~70%    红 ~20%    白/肤 ~8%    银 ~2%", TXT),
    ("红色用法   只作「运动的结果」与内衬，绝不做大面积装饰", TXT),
    ("对比核心   纤细的身体 × 巨大的机械兵器；安静的上半身 × 流动的裙摆", TXT),
]
for r, c in RULES:
    d.text((48, y), r, font=F_MONO, fill=c)
    y += 30

p = os.path.join(OUT, "LYCO_配色卡.png")
img.save(p)
print("->", p, img.size)


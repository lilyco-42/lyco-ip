# -*- coding: utf-8 -*-
"""inspect_seed7.py —— 细看 Kaggle v6 seed7 的 64x64 皮肤"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:\Users\liuqi\WorkBuddy\2026-09-28-23-25-03\tools")
from render_skin_preview import flatten, assemble  # noqa: E402

A = r"D:\gal\AliceInCradle\LYCO_art"
SEED7 = os.path.join(A, "LYCO_Kaggle_v6_seed7.png")
V3 = os.path.join(A, "LYCO_mc_skin_v3_slim.png")

PAL_NAME = {
    (0x12, 0x10, 0x16): "发深黑", (0x1E, 0x1B, 0x24): "发次黑",
    (0x2A, 0x26, 0x30): "发高光", (0x8E, 0x1B, 0x24): "红内层",
    (0xC0, 0x28, 0x32): "红亮", (0xF3, 0xDC, 0xD1): "肤",
    (0xE2, 0xC2, 0xB6): "肤影", (0xF6, 0xF4, 0xF2): "眼白",
    (0x8E, 0x8A, 0x96): "灰瞳", (0x33, 0x30, 0x3A): "眼深",
    (0x18, 0x18, 0x1E): "布黑", (0x26, 0x26, 0x30): "布次",
    (0x0F, 0x0F, 0x14): "布最暗", (0x6E, 0x0D, 0x14): "内衬红",
    (0xB6, 0x28, 0x33): "滚边红", (0xC8, 0xCC, 0xD0): "银",
    (0x8A, 0x8E, 0x98): "银暗", (0x46, 0x42, 0x4E): "裤袜",
    (0x56, 0x52, 0x60): "裤袜亮", (0x12, 0x12, 0x18): "靴",
    (0x22, 0x22, 0x2A): "靴亮",
}


def nearest_name(c):
    best, bd = None, 1e9
    for k, v in PAL_NAME.items():
        d = sum((int(c[i]) - k[i]) ** 2 for i in range(3))
        if d < bd:
            bd, best = d, v
    return best


def show_face(path, label):
    a = np.asarray(Image.open(path).convert("RGBA"))
    print(f"\n=== {label} · 头正面 8x8 (8,8)-(16,16) ===")
    for y in range(8, 16):
        row = []
        for x in range(8, 16):
            r, g, b, al = a[y, x]
            row.append("......" if al == 0 else "%02X%02X%02X" % (r, g, b))
        print("   " + " ".join(row))
    print("   主要颜色:")
    cnt = {}
    for y in range(8, 16):
        for x in range(8, 16):
            r, g, b, al = a[y, x]
            if al:
                cnt[(int(r), int(g), int(b))] = cnt.get((int(r), int(g), int(b)), 0) + 1
    for c, n in sorted(cnt.items(), key=lambda kv: -kv[1])[:6]:
        print("     #%02X%02X%02X  x%-3d ≈ %s" % (c[0], c[1], c[2], n, nearest_name(c)))


for p, lab in ((SEED7, "Kaggle v6 seed7"), (V3, "手绘 v3 slim")):
    if os.path.exists(p):
        show_face(p, lab)

# 对比渲染
Z = 6
LZ = 13
tiles = []
for p, lab, sl in ((SEED7, "v6 seed7 ★", False), (V3, "v3 手绘", True)):
    if not os.path.exists(p):
        continue
    sk = Image.open(p).convert("RGBA")
    flat = flatten(sk)
    head = flat.crop((8, 8, 16, 16)).resize((8 * LZ, 8 * LZ), Image.NEAREST)
    tiles.append((lab + " 脸", head))
    tiles.append((lab + " 图集", sk.resize((64 * Z, 64 * Z), Image.NEAREST)))
    for v in ("front", "back"):
        tiles.append((lab + " " + v, assemble(flat, v, sl).resize((16 * LZ // 2, 32 * LZ // 2), Image.NEAREST)))

W = sum(t.width for _, t in tiles) + 20 * (len(tiles) - 1) + 56
H = max(t.height for _, t in tiles) + 60
img = Image.new("RGB", (W, H), (20, 20, 24))
from PIL import ImageDraw, ImageFont  # noqa: E402


def F(s, b=False):
    for n in (("msyhbd.ttc" if b else "msyh.ttc"), "simhei.ttf"):
        try:
            return ImageFont.truetype(n, s)
        except Exception:
            pass
    return ImageFont.load_default()


d = ImageDraw.Draw(img)
d.text((28, 20), "Kaggle v6 seed7  vs  手绘 v3", font=F(22, True), fill=(235, 235, 240))
x = 28
for lab, t in tiles:
    bg = Image.new("RGB", t.size, (30, 30, 36))
    bg.paste(t, (0, 0), t)
    img.paste(bg, (x, 56))
    d.text((x, 56 + t.height + 4), lab, font=F(13), fill=(130, 130, 140))
    x += t.width + 20
out = os.path.join(A, "LYCO_v6seed7_vs_v3.png")
img.save(out)
print("\n->", out, img.size)

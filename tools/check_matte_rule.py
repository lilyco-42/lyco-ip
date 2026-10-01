# -*- coding: utf-8 -*-
"""
check_matte_rule.py —— 验证 skin-spec 里的「哑光色透明度」机制

规范原文：
    "Transparency must be based off of the upper left-hand pixel of the image.
     Though many skins use the standard alpha-channel, others use a solid matte."
    → 有些皮肤不用 alpha 通道，而是**用左上角像素的颜色当作"透明色"**。
      凡等于该颜色的像素，都应被视为透明。

这解释了 BLOCKv0.6 输出为什么会变成白块：
    它输出 RGB 无 alpha，把该透明的区域填成了白色。
    如果左上角恰好是白色，那按规范这些白像素本来就该是透明的。
"""
import glob
import os

import numpy as np
from PIL import Image

ART = r"D:\gal\AliceInCradle\LYCO_art"

FILES = [
    ("手绘 v2 slim",        os.path.join(ART, "LYCO_mc_skin_v2_slim.png")),
    ("手绘 v2 classic",     os.path.join(ART, "LYCO_mc_skin_v2_classic.png")),
    ("BLOCK seed0（未修白层）", os.path.join(ART, "LYCO_BLOCK生成皮肤_seed0.png")),
    ("BLOCK seed0（已修白层）", os.path.join(ART, "LYCO_BLOCK生成皮肤_seed0_fixed.png")),
    ("Kaggle v6 seed42",   os.path.join(ART, "LYCO_Kaggle_v6_seed42.png")),
]

print("=" * 86)
print("「哑光色透明度」机制验证")
print("=" * 86)
print("%-24s %-16s %-10s %-22s %s" % ("文件", "左上角(0,0)", "alpha", "同色像素数", "判读"))
print("-" * 86)

for label, path in FILES:
    if not os.path.exists(path):
        print("%-24s [缺]" % label)
        continue
    a = np.asarray(Image.open(path).convert("RGBA"))
    tl = a[0, 0]
    same = int(((a[:, :, 0] == tl[0]) & (a[:, :, 1] == tl[1]) &
                (a[:, :, 2] == tl[2]) & (a[:, :, 3] == tl[3])).sum())
    op = int((a[:, :, 3] > 0).sum())
    if tl[3] == 0:
        verdict = "标准 alpha 通道（左上角已透明）"
    elif same > 300:
        verdict = "★ 疑似哑光色皮肤：该色应视为透明"
    else:
        verdict = "左上角是不透明内容，无哑光机制"
    print("%-24s #%02X%02X%02X a=%-4d %-10s %-22d %s"
          % (label, tl[0], tl[1], tl[2], tl[3], "透明" if tl[3] == 0 else "不透明",
             same, verdict))

print()
print("=" * 86)
print("第二层（外套层）内容的透明度合规性")
print("=" * 86)
print("规范规定：第一层必须**不透明**；第二层**可以**透明。")
print()

LAYER2 = {"hat": (32, 0, 64, 16), "jacket": (16, 32, 40, 48),
          "rSleeve": (40, 32, 56, 48), "lSleeve": (48, 48, 64, 64),
          "rPant": (0, 32, 16, 48), "lPant": (0, 48, 16, 64)}

for label, path in FILES:
    if not os.path.exists(path):
        continue
    a = np.asarray(Image.open(path).convert("RGBA"))
    parts = []
    for name, (x0, y0, x1, y1) in LAYER2.items():
        sub = a[y0:y1, x0:x1]
        op = int((sub[:, :, 3] > 0).sum())
        parts.append("%s=%d%%" % (name, 100 * op // sub[:, :, 3].size))
    print("%-24s %s" % (label, "  ".join(parts)))

# -*- coding: utf-8 -*-
"""
build_mc_skin_v4.py —— v3 + 游戏内明度补偿

v3 的问题（实测）：
    感知亮度均值 53.7，极暗(<40)像素占 64%
    → 在 Minecraft 的固定光照下全部糊成一片黑，Blockbench 里就是一坨

根因：
    02-palette.md 里的配色是给**插画**用的。插画能自己打光，
    所以 #121016 的头发能读出「黑发 + 高光」。
    但 Minecraft 有固定光照、且会在贴图基础上继续压暗，
    近黑色直接失去分离度。

做法：
    保留色相与相对明暗关系，只把**明度整体抬高**。
    暗部抬得多、亮部几乎不动 —— 这样既保住「黑红」的识别度，
    又让游戏里能看出层次。

目标（对齐实测参考值）：
    感知亮度均值  ≥ 110（v6 seed7 = 122，参考皮肤 160-175）
    极暗(<40)占比 ≤ 25%（v6 seed7 = 19%，参考皮肤 0%）
"""
import colorsys
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:\Users\liuqi\WorkBuddy\2026-09-28-23-25-03\tools")


# ══════════════════ 原始配色（lyco-ip/docs/02-palette.md）══════════════════
BASE = {
    "H": (0x12, 0x10, 0x16), "h": (0x1E, 0x1B, 0x24), "G": (0x2A, 0x26, 0x30),
    "R": (0x8E, 0x1B, 0x24), "r": (0xC0, 0x28, 0x32),
    "S": (0xF3, 0xDC, 0xD1), "s": (0xE2, 0xC2, 0xB6), "W": (0xF6, 0xF4, 0xF2),
    "E": (0x8E, 0x8A, 0x96), "e": (0x33, 0x30, 0x3A),
    "C": (0x18, 0x18, 0x1E), "c": (0x26, 0x26, 0x30), "D": (0x0F, 0x0F, 0x14),
    "L": (0x6E, 0x0D, 0x14), "X": (0xB6, 0x28, 0x33),
    "V": (0xC8, 0xCC, 0xD0), "v": (0x8A, 0x8E, 0x98),
    "T": (0x46, 0x42, 0x4E), "t": (0x56, 0x52, 0x60),
    "B": (0x12, 0x12, 0x18), "b": (0x22, 0x22, 0x2A),
    ".": None,
}


def lift(rgb, lo_gain=2.30, mid_gain=1.55, hi_gain=1.04, target_floor=0.115):
    """保留 H/S，抬高 V。

    暗部（V<0.20）抬得最多，中调次之，亮部几乎不动。
    再加一个「地板」：任何颜色 V 不得低于 target_floor ——
    这样近黑色在游戏里也不会糊成纯黑。
    """
    r, g, b = [c / 255.0 for c in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if v < 0.20:
        v2 = v * lo_gain
    elif v < 0.50:
        v2 = v * mid_gain
    else:
        v2 = v * hi_gain
    v2 = max(v2, target_floor)
    # 抬高明度后饱和度会显脏，稍微降一点
    s2 = min(1.0, s * 0.92)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s2, min(1.0, v2))
    return (int(round(r2 * 255)), int(round(g2 * 255)), int(round(b2 * 255)))


PAL = {k: (lift(v) if v else None) for k, v in BASE.items()}

if __name__ == "__main__":
    print("=" * 78)
    print("明度补偿：原始 -> 补偿后")
    print("=" * 78)
    print("%-4s %-10s %-10s %-22s" % ("键", "原始", "补偿后", "感知亮度变化"))
    print("-" * 78)
    for k, v in BASE.items():
        if not v:
            continue
        n = PAL[k]
        L0 = 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
        L1 = 0.2126 * n[0] + 0.7152 * n[1] + 0.0722 * n[2]
        bar = "█" * max(1, int(L1 / 8))
        print("%-4s #%02X%02X%02X   #%02X%02X%02X   %5.1f -> %5.1f  %s"
              % (k, v[0], v[1], v[2], n[0], n[1], n[2], L0, L1, bar))

    # 写入一个供 build 使用的模块
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_palette_lifted.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write("# 由 build_mc_skin_v4.py 自动生成：游戏内明度补偿后的配色\n")
        f.write("PAL = {\n")
        for k, v in PAL.items():
            f.write(f"    {k!r}: {v!r},\n")
        f.write("}\n")
    print()
    print("已写出:", out)

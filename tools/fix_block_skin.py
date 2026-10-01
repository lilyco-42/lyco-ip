# -*- coding: utf-8 -*-
"""
fix_block_skin.py —— 修复 BLOCKv0.6 输出的「第二层全白」问题

问题：
    模型输出 RGB **没有 alpha 通道**，它把「应该透明」的第二层区域填成了白色
    （因为训练用的预览图背景就是白的）。
    Minecraft 的第二层是盖在第一层上面渲染的 → 全白 = 角色在游戏里是一坨白块。
    结构校验能过（不透明、尺寸对），但视觉上完全废掉。

修法：
    把第二层里的近白像素判为 background，置为透明；保留真正有内容的部分。
    若清完后第二层几乎空了，就整层清掉（退化成单层皮肤，安全可用）。
"""
import os
import sys

import numpy as np
from PIL import Image

# 第二层（外套层）在 64x64 UV 里的六块区域
OVERLAY_RECTS = {
    "hat":     (32, 0, 64, 16),
    "jacket":  (16, 32, 40, 48),
    "rSleeve": (40, 32, 56, 48),
    "lSleeve": (48, 48, 64, 64),
    "rPant":   (0, 32, 16, 48),
    "lPant":   (0, 48, 16, 64),
}

# 第一层（本体）区域 —— 这些绝不能动
# 注意：左臂主层是 (32,48)-(48,64)，外套层是 (48,48)-(64,64)，两者相邻不重叠
FIRST_LAYER_RECTS = [
    (0, 0, 32, 16),     # 头
    (16, 16, 40, 32),   # 躯干
    (40, 16, 56, 32),   # 右臂
    (0, 16, 16, 32),    # 右腿
    (16, 48, 32, 64),   # 左腿
    (32, 48, 48, 64),   # 左臂
]


def fix(path, out_path=None, white_thresh=235, keep_ratio=0.12):
    """white_thresh: 三通道都高于此值判为背景白
       keep_ratio:    某层清完后剩余内容少于该比例，则整层清空"""
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).copy()
    print(f"=== {os.path.basename(path)} ===")
    print(f"  阈值: 白>{white_thresh}  保留比<{keep_ratio:.0%}则整层清空")

    for name, (x0, y0, x1, y1) in OVERLAY_RECTS.items():
        sub = a[y0:y1, x0:x1]
        rgb = sub[:, :, :3].astype(np.int16)
        is_white = (rgb > white_thresh).all(axis=2)

        before = int((sub[:, :, 3] > 0).sum())
        if before == 0:
            print(f"  {name:<8} 本来就全透明，跳过")
            continue

        # 清掉白像素
        sub[:, :, 3][is_white] = 0
        after = int((sub[:, :, 3] > 0).sum())

        # 清完几乎空了 → 整层清掉
        if after < sub[:, :, 3].size * keep_ratio:
            sub[:, :, 3] = 0
            print(f"  {name:<8} 清掉 {before:>3} px 白 -> 剩余 {after:>3} px，整层清空")
        else:
            print(f"  {name:<8} 清掉 {before - after:>3} px 白，保留 {after:>3} px 内容")

    out = out_path or path.replace(".png", "_fixed.png")
    Image.fromarray(a, "RGBA").save(out)
    print(f"  -> {out}")

    # 校验：第一层有没有被误伤
    bad = []
    for (x0, y0, x1, y1) in FIRST_LAYER_RECTS:
        if (a[y0:y1, x0:x1, 3] < 255).any():
            bad.append((x0, y0, x1, y1))
    print(f"  第一层完整性: {'✅ 未受影响' if not bad else '❌ 被破坏 ' + str(bad)}")
    return out


if __name__ == "__main__":
    ART = r"D:\gal\AliceInCradle\LYCO_art"
    targets = sys.argv[1:] or [
        os.path.join(ART, "LYCO_BLOCK生成皮肤_seed0.png"),
        os.path.join(ART, "LYCO_BLOCK生成皮肤_seed42.png"),
        os.path.join(ART, "LYCO_BLOCK生成皮肤_seed1234.png"),
    ]
    for t in targets:
        fix(t)
        print()

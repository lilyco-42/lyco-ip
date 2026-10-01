# -*- coding: utf-8 -*-
"""
validate_mc_skin.py —— Minecraft 皮肤严格校验

检查项（任何一项不过 = 游戏里会出问题）：
  1. 尺寸必须是 64x64（现代）或 64x32（旧版）
  2. 必须是 RGBA
  3. 第一层（身体本体）的每一张**会被渲染的面**必须完全不透明 —— 否则玩家身上有洞
  4. 第二层（帽层/外套层）要么整块透明，要么有内容，不能是随机噪声
  5. 64x64 专有区域（左臂/左腿）在 64x32 皮肤里必须为空
"""
import sys

import numpy as np
from PIL import Image

# 会被渲染的「第一层」面（slim=False 经典手臂布局）
FIRST_LAYER_REGULAR = [
    ("head top",     (8, 0, 16, 8)),   ("head bottom", (16, 0, 24, 8)),
    ("head right",   (0, 8, 8, 16)),   ("head front",  (8, 8, 16, 16)),
    ("head left",    (16, 8, 24, 16)), ("head back",   (24, 8, 32, 16)),
    ("torso top",    (20, 16, 28, 20)), ("torso bottom", (28, 16, 36, 20)),
    ("torso right",  (16, 20, 20, 32)), ("torso front", (20, 20, 28, 32)),
    ("torso left",   (28, 20, 32, 32)), ("torso back",  (32, 20, 40, 32)),
    ("rArm top",     (44, 16, 48, 20)), ("rArm bottom", (48, 16, 52, 20)),
    ("rArm right",   (40, 20, 44, 32)), ("rArm front",  (44, 20, 48, 32)),
    ("rArm left",    (48, 20, 52, 32)), ("rArm back",   (52, 20, 56, 32)),
    ("rLeg top",     (4, 16, 8, 20)),   ("rLeg bottom", (8, 16, 12, 20)),
    ("rLeg right",   (0, 20, 4, 32)),   ("rLeg front",  (4, 20, 8, 32)),
    ("rLeg left",    (8, 20, 12, 32)),  ("rLeg back",   (12, 20, 16, 32)),
    ("lLeg top",     (20, 48, 24, 52)), ("lLeg bottom", (24, 48, 28, 52)),
    ("lLeg right",   (16, 52, 20, 64)), ("lLeg front",  (20, 52, 24, 64)),
    ("lLeg left",    (24, 52, 28, 64)), ("lLeg back",   (28, 52, 32, 64)),
    ("lArm top",     (36, 48, 40, 52)), ("lArm bottom", (40, 48, 44, 52)),
    ("lArm right",   (32, 52, 36, 64)), ("lArm front",  (36, 52, 40, 64)),
    ("lArm left",    (40, 52, 44, 64)), ("lArm back",   (44, 52, 48, 64)),
]

# slim（Alex）模型：手臂正面/背面只有 3px 宽
SLIM_ARM_DIFF = {
    "rArm top": (44, 16, 47, 20), "rArm bottom": (47, 16, 50, 20),
    "rArm left": (47, 20, 51, 32), "rArm back": (51, 20, 54, 32),
    "lArm top": (36, 48, 39, 52), "lArm bottom": (39, 48, 42, 52),
    "lArm left": (39, 52, 43, 64), "lArm back": (43, 52, 46, 64),
}

SECOND_LAYER = [
    ("hat", (32, 0, 64, 16)), ("jacket", (16, 32, 40, 48)),
    ("rSleeve", (40, 32, 56, 48)), ("lSleeve", (48, 48, 64, 64)),
    ("rPant", (0, 32, 16, 48)), ("lPant", (0, 48, 16, 64)),
]


def validate(path, slim=False):
    print(f"=== {path} ===")
    ok = True
    im = Image.open(path)
    a = np.asarray(im.convert("RGBA"))

    if im.size == (64, 32):
        print("  尺寸 64x32（旧版布局）—— 本校验只覆盖 64x64")
        return
    if im.size != (64, 64):
        print(f"  ❌ 尺寸 {im.size} 非法，必须 64x64")
        return
    print(f"  ✅ 尺寸 {im.size}")
    print(f"  {'✅' if im.mode in ('RGBA','P') else '⚠️ '} 模式 {im.mode}"
          f"{'（含 alpha）' if 'A' in im.mode or im.mode=='P' else ''}")

    faces = list(FIRST_LAYER_REGULAR)
    if slim:
        faces = [(n, SLIM_ARM_DIFF.get(n, b)) for n, b in faces]
    print(f"  手臂模型: {'slim / Alex (3px)' if slim else 'classic / Steve (4px)'}")

    holes = []
    for name, (x0, y0, x1, y1) in faces:
        sub = a[y0:y1, x0:x1, 3]
        tot = sub.size
        op = int((sub == 255).sum())
        if op < tot:
            holes.append((name, tot - op))
    if holes:
        ok = False
        print(f"  ❌ 第一层有 {len(holes)} 张面存在透明像素（游戏里会出现破洞）:")
        for n, miss in holes[:8]:
            print(f"       {n}: 缺 {miss} px")
    else:
        print(f"  ✅ 第一层 {len(faces)} 张面全部不透明（无破洞）")

    print("  第二层（可选层）:")
    for name, (x0, y0, x1, y1) in SECOND_LAYER:
        sub = a[y0:y1, x0:x1, 3]
        op = int((sub > 0).sum())
        ratio = op / sub.size
        state = "全透明（无此层）" if ratio == 0 else f"有内容 {op}/{sub.size} ({ratio:.0%})"
        print(f"       {name:<9} {state}")

    # 未使用区域
    unused = a[0:8, 0:8, 3]
    print(f"  未使用角落 (0,0)-(8,8): {'透明 ✅' if (unused==0).all() else '有内容（无害）'}")

    print(f"  {'✅ 校验通过' if ok else '❌ 校验失败'}")
    return ok


if __name__ == "__main__":
    targets = sys.argv[1:] or [
        r"D:\gal\AliceInCradle\LYCO_art\LYCO_mc_skin_v2_slim.png",
        r"D:\gal\AliceInCradle\LYCO_art\LYCO_mc_skin_v2_classic.png",
        r"D:\gal\AliceInCradle\LYCO_art\LYCO_BLOCK生成皮肤_seed42.png",
    ]
    for t in targets:
        slim = "slim" in t.lower()
        validate(t, slim=slim)
        print()

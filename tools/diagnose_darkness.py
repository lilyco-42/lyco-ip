# -*- coding: utf-8 -*-
"""
diagnose_darkness.py —— 为什么 v3 在游戏里是黑块

假设：我的配色表是给「插画」用的（画家能控制光照），
      但 Minecraft 有自己固定的光照，会**压暗**贴图。
      近黑的颜色（#121016 / #18181E）在游戏里全部糊成一片黑，失去分离度。

对照组：用户给过的两张参考皮肤（它们在游戏里是好看的）。
"""
import os

import numpy as np
from PIL import Image

A = r"D:\gal\AliceInCradle\LYCO_art"
REF = r"D:\gal\AliceInCradle\_generated\mc_ref"

SPECS = [
    ("v3 slim（我的，被吐槽）", os.path.join(A, "LYCO_mc_skin_v3_slim.png")),
    ("v2 slim（更早的）", os.path.join(A, "LYCO_mc_skin_v2_slim.png")),
    ("v6 seed7（AI，你说好）", os.path.join(A, "LYCO_Kaggle_v6_seed7.png")),
    ("混合体 v3脸+v6身", os.path.join(A, "LYCO_mc_hybrid_v3脸_v6身.png")),
    ("参考1（棕发绿装）", os.path.join(REF, "ref1.png")),
    ("参考2（粉发绿装）", os.path.join(REF, "ref2.png")),
]


def lum_stats(path):
    a = np.asarray(Image.open(path).convert("RGBA"))
    op = a[:, :, 3] > 0
    px = a[:, :, :3][op].astype(float)
    # 感知亮度
    L = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
    return {
        "mean": L.mean(),
        "median": np.median(L),
        "p10": np.percentile(L, 10),
        "p90": np.percentile(L, 90),
        "spread": np.percentile(L, 90) - np.percentile(L, 10),
        "very_dark": (L < 40).mean(),      # 游戏里会糊成一片黑的比例
        "bright": (L > 150).mean(),
    }


print("=" * 100)
print("感知亮度分析（0-255，Minecraft 会在此基础上再压暗）")
print("=" * 100)
print("%-26s %6s %6s %6s %6s %8s %10s %8s" %
      ("文件", "均值", "中位", "P10", "P90", "动态范围", "极暗(<40)占", "亮部>150"))
print("-" * 100)
rows = []
for lab, p in SPECS:
    if not os.path.exists(p):
        print("%-26s [缺]" % lab)
        continue
    s = lum_stats(p)
    rows.append((lab, s))
    print("%-26s %6.1f %6.1f %6.1f %6.1f %8.1f %9.0f%% %7.0f%%" %
          (lab, s["mean"], s["median"], s["p10"], s["p90"],
           s["spread"], 100 * s["very_dark"], 100 * s["bright"]))

print()
print("=" * 100)
print("诊断")
print("=" * 100)
mine = next((s for l, s in rows if "v3" in l), None)
ref = [s for l, s in rows if "参考" in l]
good = next((s for l, s in rows if "seed7" in l), None)

if mine and ref:
    r_mean = np.mean([s["mean"] for s in ref])
    r_dark = np.mean([s["very_dark"] for s in ref])
    r_spread = np.mean([s["spread"] for s in ref])
    print(f"  我的 v3      均值 {mine['mean']:.1f}  极暗占比 {100*mine['very_dark']:.0f}%  动态范围 {mine['spread']:.1f}")
    print(f"  参考皮肤平均  均值 {r_mean:.1f}  极暗占比 {100*r_dark:.0f}%  动态范围 {r_spread:.1f}")
    print()
    print(f"  → 均值低 {r_mean - mine['mean']:.1f} 档")
    print(f"  → 极暗像素多 {100*(mine['very_dark']-r_dark):.0f} 个百分点（这些在游戏里全糊成一片黑）")
    print(f"  → 动态范围窄 {r_spread - mine['spread']:.1f}（明暗没有拉开）")
    print()
    print("  结论：我的配色表是给「插画」用的 —— 画家能自己打光。")
    print("        但 Minecraft 有固定光照且会压暗贴图，近黑色全糊在一起。")
    print("        需要把**中间调的明度整体抬高**，而不是改配色本身。")

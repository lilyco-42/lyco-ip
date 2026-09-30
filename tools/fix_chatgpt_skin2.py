# -*- coding: utf-8 -*-
"""
fix_chatgpt_skin2.py —— 把 ChatGPT 的高分皮肤图修成合法 64x64

结论（已实测验证）：那张 1254x1254 的图**就是标准 64x64 布局的高分渲染**
（内容区约 1202x1191，≈18.7 px / 皮肤像素），只是分辨率太高导致直接当皮肤导入报错。

做法：内容区裁切 -> 面积平均降到 64x64 -> 吸附回源图主色板（恢复像素风）
"""
import os
import numpy as np
from PIL import Image

SRC = r"D:\gal\AliceInCradle\_generated\mc_chatgpt\src.png"
OUT = r"D:\gal\AliceInCradle\LYCO_art"
TMP = r"D:\gal\AliceInCradle\_generated\mc_chatgpt"


def content_bbox(im):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    m = a.sum(axis=2) > 60
    ys, xs = np.where(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def palette_of(im, n=26):
    sa = np.asarray(im.convert("RGB")).reshape(-1, 3)
    sa = sa[sa.sum(axis=1) > 60]
    tmp = Image.fromarray(sa.reshape(-1, 1, 3).astype(np.uint8), "RGB")
    q = tmp.quantize(colors=n, method=Image.MEDIANCUT)
    return np.array(q.getpalette()[:n * 3], dtype=np.float32).reshape(-1, 3)


def quantize(skin, pal):
    a = np.asarray(skin.convert("RGBA")).astype(np.float32)
    h, w, _ = a.shape
    d = ((a[:, :, :3].reshape(-1, 1, 3) - pal.reshape(1, -1, 3)) ** 2).sum(axis=2)
    out = a.copy()
    out[:, :, :3] = pal[d.argmin(axis=1)].reshape(h, w, 3)
    return Image.fromarray(out.astype(np.uint8), "RGBA")


# 六个「外层」（帽层 / 外套层 / 靴套层）在标准 UV 里的位置。
# ★ 必须清空：实测证明 AI 那张图的排版**不符合外层语义**，
#   把它的内容留在外层会在游戏里叠成红黑糊块（已渲染验证）。
OVERLAY_RECTS = [
    (32, 0, 64, 16),      # 头 帽层
    (16, 32, 40, 48),     # 躯干 外套层
    (40, 32, 56, 48),     # 右臂 外套层
    (48, 48, 64, 64),     # 左臂 外套层
    (0, 32, 16, 48),      # 右腿 靴套层
    (0, 48, 16, 64),      # 左腿 靴套层
]


def clear_overlays(skin):
    a = np.asarray(skin.convert("RGBA")).copy()
    for (x0, y0, x1, y1) in OVERLAY_RECTS:
        a[y0:y1, x0:x1] = 0
    return Image.fromarray(a, "RGBA")


if __name__ == "__main__":
    src = Image.open(SRC).convert("RGBA")
    bb = content_bbox(src)
    print("内容区:", bb, " 尺寸", bb[2] - bb[0], "x", bb[3] - bb[1])
    crop = src.crop(bb)
    pal = palette_of(src, 26)

    # 面积平均降采样（正确的缩小方式）+ 吸附回源图主色板（恢复像素风）
    final = quantize(crop.resize((64, 64), Image.BOX).convert("RGBA"), pal)
    final = clear_overlays(final)

    p = os.path.join(OUT, "LYCO_mc_skin_chatgpt.png")
    final.save(p)
    a = np.asarray(final)
    print(f"-> {p}  size={final.size} mode={final.mode} 不透明={int((a[:,:,3]>0).sum())}")

    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from remap_mc_skin import assemble

    Z = 11
    views = [assemble(final, v).resize((16 * Z, 32 * Z), Image.NEAREST)
             for v in ("front", "side", "back")]
    W = sum(v.width for v in views) + 32
    H = max(v.height for v in views)
    s = Image.new("RGBA", (W, H), (24, 24, 28, 255))
    x = 0
    for v in views:
        s.alpha_composite(v, (x, 0)); x += v.width + 16
    s.convert("RGB").save(os.path.join(OUT, "LYCO_mc_chatgpt_预览.png"))
    print("preview ->", os.path.join(OUT, "LYCO_mc_chatgpt_预览.png"), s.size)

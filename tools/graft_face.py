# -*- coding: utf-8 -*-
"""
graft_face.py —— 把 v3 手绘的头，移植到 v6 seed7 的身体上

为什么要这么做：
    v6 seed7（AI 出）  身体层次好、有明暗过渡 —— 但 8x8 的脸全是中间色，糊、没结构
    v3（手绘）         脸干净（黑刘海 / 灰瞳 / 白高光 / 上眼睑）—— 但身体偏"平"

    两者各有一半是对的，拼起来取长补短。

移植范围：整个头部
    主层   (0,0)-(32,16)
    帽层   (32,0)-(64,16)
    身体、四肢、第二层外套 全部保留 seed7
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:\Users\liuqi\WorkBuddy\2026-09-28-23-25-03\tools")
from render_skin_preview import flatten, assemble  # noqa: E402

A = r"D:\gal\AliceInCradle\LYCO_art"
BODY = os.path.join(A, "LYCO_Kaggle_v6_seed7.png")     # AI：身体好
HEAD = os.path.join(A, "LYCO_mc_skin_v3_slim.png")      # 手绘：脸好

HEAD_RECTS = [(0, 0, 32, 16), (32, 0, 64, 16)]


def graft(body_path, head_path, out_path):
    b = Image.open(body_path).convert("RGBA")
    h = Image.open(head_path).convert("RGBA")
    ba, ha = np.asarray(b).copy(), np.asarray(h)
    for (x0, y0, x1, y1) in HEAD_RECTS:
        ba[y0:y1, x0:x1] = ha[y0:y1, x0:x1]
    out = Image.fromarray(ba, "RGBA")
    out.save(out_path)
    print(f"-> {out_path}")
    return out


if __name__ == "__main__":
    out = os.path.join(A, "LYCO_mc_hybrid_v3脸_v6身.png")
    sk = graft(BODY, HEAD, out)

    # 校验：第一层必须仍然全不透明
    a = np.asarray(sk)
    FACES = [(8, 0, 16, 8), (16, 0, 24, 8), (0, 8, 8, 16), (8, 8, 16, 16),
             (16, 8, 24, 16), (24, 8, 32, 16), (20, 16, 28, 20), (28, 16, 36, 20),
             (16, 20, 20, 32), (20, 20, 28, 32), (28, 20, 32, 32), (32, 20, 40, 32),
             (44, 16, 48, 20), (48, 16, 52, 20), (40, 20, 44, 32), (44, 20, 48, 32),
             (48, 20, 52, 32), (52, 20, 56, 32),
             (4, 16, 8, 20), (8, 16, 12, 20), (0, 20, 4, 32), (4, 20, 8, 32),
             (8, 20, 12, 32), (12, 20, 16, 32),
             (20, 48, 24, 52), (24, 48, 28, 52), (16, 52, 20, 64), (20, 52, 24, 64),
             (24, 52, 28, 64), (28, 52, 32, 64),
             (36, 48, 40, 52), (40, 48, 44, 52), (32, 52, 36, 64), (36, 52, 40, 64),
             (40, 52, 44, 64), (44, 52, 48, 64)]
    holes = [f for f in FACES if (a[f[1]:f[3], f[0]:f[2], 3] < 255).any()]
    print(f"   第一层 36 面: {'✅ 全不透明' if not holes else '❌ ' + str(holes[:3])}")

    # 三方对比
    Z, LZ = 6, 13
    specs = [(os.path.join(A, "LYCO_Kaggle_v6_seed7.png"), "v6 seed7（AI）", False),
             (out, "混合体（v3脸+v6身）", False),
             (os.path.join(A, "LYCO_mc_skin_v3_slim.png"), "v3（手绘）", True)]
    tiles = []
    for p, lab, sl in specs:
        s = Image.open(p).convert("RGBA")
        fl = flatten(s)
        tiles.append((lab + " · 脸", fl.crop((8, 8, 16, 16)).resize((8 * LZ, 8 * LZ), Image.NEAREST)))
        tiles.append((lab + " · 正面", assemble(fl, "front", sl).resize((16 * LZ // 2, 32 * LZ // 2), Image.NEAREST)))
        tiles.append((lab + " · 背面", assemble(fl, "back", sl).resize((16 * LZ // 2, 32 * LZ // 2), Image.NEAREST)))

    from PIL import ImageDraw, ImageFont

    def F(s, b=False):
        for n in (("msyhbd.ttc" if b else "msyh.ttc"), "simhei.ttf"):
            try:
                return ImageFont.truetype(n, s)
            except Exception:
                pass
        return ImageFont.load_default()

    W = sum(t.width for _, t in tiles) + 20 * (len(tiles) - 1) + 56
    H = max(t.height for _, t in tiles) + 62
    img = Image.new("RGB", (W, H), (20, 20, 24))
    d = ImageDraw.Draw(img)
    d.text((28, 18), "换脸对比：AI 的身体 + 手绘的脸", font=F(22, True), fill=(235, 235, 240))
    d.text((28, 44), "v6 seed7 的脸是中间色（糊） · v3 的脸干净但身体偏平 · 混合体取两者之长",
           font=F(13), fill=(140, 140, 150))
    x = 28
    for lab, t in tiles:
        bg = Image.new("RGB", t.size, (30, 30, 36))
        bg.paste(t, (0, 0), t)
        img.paste(bg, (x, 62))
        d.text((x, 62 + t.height + 4), lab, font=F(12), fill=(130, 130, 140))
        x += t.width + 20
    o2 = os.path.join(A, "LYCO_换脸对比.png")
    img.save(o2)
    print("->", o2, img.size)

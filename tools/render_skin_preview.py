# -*- coding: utf-8 -*-
"""render_skin_preview.py —— 把 64x64 皮肤渲染成「游戏里实际看到的样子」

把第二层（帽层/外套层）合成到第一层上，再按 UV 拼成正/侧/背视图。
"""
import os
import sys

from PIL import Image

# 第二层 -> 第一层的对应偏移
OVERLAY_MAP = {
    (32, 0, 64, 16): (0, 0, 32, 16),        # 头帽层
    (16, 32, 40, 48): (16, 16, 40, 32),     # 躯干外套
    (40, 32, 56, 48): (40, 16, 56, 32),     # 右臂外套
    (48, 48, 64, 64): (32, 48, 64, 64),     # 左臂外套
    (0, 32, 16, 48): (0, 16, 16, 32),       # 右腿靴套
    (0, 48, 16, 64): (16, 48, 32, 64),      # 左腿靴套
}


def flatten(skin: Image.Image) -> Image.Image:
    """把第二层合成到第一层，得到渲染时的实际外观"""
    flat = skin.copy()
    fp, sp = flat.load(), skin.load()
    for ov, mn in OVERLAY_MAP.items():
        ox, oy, ox1, oy1 = ov
        for y in range(oy, oy1):
            for x in range(ox, ox1):
                r, g, b, al = sp[x, y]
                if al < 8:
                    continue
                tx, ty = mn[0] + (x - ox), mn[1] + (y - oy)
                if tx < mn[2] and ty < mn[3]:
                    fp[tx, ty] = (r, g, b, 255)
    return flat


def assemble(skin: Image.Image, view: str = "front", slim: bool = False) -> Image.Image:
    """按 UV 拼成人形（1px = 1px，之后放大）"""
    g = skin.load()
    out = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    o = out.load()

    def blit(box, dx, dy):
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                tx, ty = dx + (x - x0), dy + (y - y0)
                if 0 <= tx < 16 and 0 <= ty < 32:
                    o[tx, ty] = g[x, y]

    aw = 3 if slim else 4          # 手臂宽度
    ax = 44 if slim else 44
    bx = 36 if slim else 36

    if view == "front":
        blit((8, 8, 16, 16), 4, 0)
        blit((40, 20, 40 + aw, 32), 0, 8)                 # 右臂（观者左）
        blit((20, 20, 28, 32), 4, 8)
        blit((bx, 52, bx + aw, 64), 16 - aw, 8)           # 左臂
        blit((4, 20, 8, 32), 4, 20)
        blit((20, 52, 24, 64), 8, 20)
    elif view == "back":
        blit((24, 8, 32, 16), 4, 0)
        blit((52 - (4 - aw), 20, 56, 32), 0, 8)           # 右臂背
        blit((32, 20, 40, 32), 4, 8)
        blit((44 - (4 - aw), 52, 48, 64), 16 - aw, 8)     # 左臂背
        blit((12, 20, 16, 32), 4, 20)
        blit((28, 52, 32, 64), 8, 20)
    else:  # side
        blit((0, 8, 8, 16), 4, 0)
        blit((40, 20, 44, 32), 6, 8)
        blit((16, 20, 20, 32), 8, 8)
        blit((0, 20, 4, 32), 6, 20)
    return out


def sheet(skins, labels, slim_flags, z=8, bg=(22, 22, 26)):
    tiles = []
    for sk, lab, sl in zip(skins, labels, slim_flags):
        flat = flatten(sk)
        tiles.append((lab, sk.resize((64 * z // 2, 64 * z // 2), Image.NEAREST)))
        for v in ("front", "side", "back"):
            tiles.append((lab, assemble(flat, v, sl).resize((16 * z, 32 * z), Image.NEAREST)))
    W = sum(t.width for _, t in tiles) + 14 * (len(tiles) - 1)
    H = max(t.height for _, t in tiles)
    s = Image.new("RGBA", (W, H), bg + (255,))
    x = 0
    for _, t in tiles:
        s.alpha_composite(t, (x, 0))
        x += t.width + 14
    return s.convert("RGB")


if __name__ == "__main__":
    ART = r"D:\gal\AliceInCradle\LYCO_art"
    specs = [
        (os.path.join(ART, "LYCO_mc_skin_v2_slim.png"), "手绘v2 slim", True),
        (os.path.join(ART, "LYCO_BLOCK生成皮肤_seed42.png"), "BLOCK seed42", False),
    ]
    skins = [Image.open(p).convert("RGBA") for p, _, _ in specs if os.path.exists(p)]
    labels = [l for p, l, _ in specs if os.path.exists(p)]
    slims = [s for p, _, s in specs if os.path.exists(p)]
    out = os.path.join(ART, "LYCO_mc_最终对比.png")
    sheet(skins, labels, slims).save(out)
    print("->", out)

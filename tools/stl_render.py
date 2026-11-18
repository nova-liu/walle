#!/usr/bin/env python3
"""极简正交渲染：把 STL 画成三视图 PNG，用来肉眼确认模型长什么样。

用法:
    python3 tools/stl_render.py out.png file1.STL [file2.STL ...]
"""
import os
import struct
import sys

import numpy as np
from PIL import Image, ImageDraw

VIEWS = {
    "front(-Y)": (0, 1, 2, -1),   # 投影轴 u=X, v=Z, 深度轴 Y, 相机在 -Y 看 +Y
    "side(+X)": (1, 2, 0, 1),     # u=Y, v=Z, 深度 X
    "top(+Z)": (0, 1, 2, 1),      # u=X, v=Y, 深度 Z
}
CELL = 400
PAD = 8


def load(path):
    with open(path, "rb") as f:
        head = f.read(84)
        n = struct.unpack("<I", head[80:84])[0]
        data = f.read(n * 50)
    arr = np.frombuffer(data, dtype=np.uint8).reshape(n, 50)
    v = arr[:, 12:48].copy().view("<f4").reshape(n, 3, 3)
    return v.astype(np.float64)


def render(tris, view, size=CELL):
    ua, va, da, sign = view
    img = Image.new("RGB", (size, size), (250, 250, 248))
    dr = ImageDraw.Draw(img)

    p = tris[:, :, [ua, va, da]]
    lo = p.reshape(-1, 3).min(axis=0)
    hi = p.reshape(-1, 3).max(axis=0)
    span = np.maximum(hi[:2] - lo[:2], 1e-6)
    scale = (size - 2 * PAD) / span.max()

    # 法向 → 面向相机的光照
    e1 = tris[:, 1] - tris[:, 0]
    e2 = tris[:, 2] - tris[:, 0]
    nrm = np.cross(e1, e2)
    ln = np.linalg.norm(nrm, axis=1)
    ln[ln < 1e-12] = 1e-12
    nrm = nrm / ln[:, None]

    # 只画朝向相机的面（背面剔除），避免内部面画出来
    facing = (nrm[:, da] * sign) > 0
    depth = p[:, :, 2].mean(axis=1)
    order = np.argsort(depth * -sign)  # 由远及近
    light = np.array([0.35, 0.55, 0.75])
    light = light / np.linalg.norm(light)

    cx = (lo[ua] + hi[ua]) / 2
    cy = (lo[va] + hi[va]) / 2
    for i in order:
        if not facing[i]:
            continue
        poly = []
        for k in range(3):
            x = size / 2 + (p[i, k, 0] - cx) * scale
            y = size / 2 - (p[i, k, 1] - cy) * scale
            poly.append((x, y))
        sh = 0.30 + 0.70 * max(0.0, float(np.dot(nrm[i], light)))
        c = int(90 + 150 * min(1.0, sh))
        dr.polygon(poly, fill=(c, int(c * 0.96), int(c * 0.88)))
    return img


def main():
    out = sys.argv[1]
    paths = sys.argv[2:]
    cols = list(VIEWS.items())
    W, H = CELL * len(cols), CELL * len(paths)
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    for r, path in enumerate(paths):
        tris = load(path)
        for c, (name, view) in enumerate(cols):
            cell = render(tris, view)
            sheet.paste(cell, (c * CELL, r * CELL))
            dr.rectangle([c * CELL, r * CELL, c * CELL + CELL - 1, r * CELL + CELL - 1],
                         outline=(200, 200, 200))
        dr.text((10, r * CELL + 6), f"{os.path.basename(path)}", fill=(0, 0, 0))
    for c, (name, _) in enumerate(cols):
        dr.text((c * CELL + 10, 24), name, fill=(180, 60, 0))
    sheet.save(out)
    print("wrote", out, sheet.size)


if __name__ == "__main__":
    main()

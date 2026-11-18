#!/usr/bin/env python3
"""STL 几何体检：结构、水密性、法向朝向、退化面、独立壳体数。

用法:
    python3 tools/stl_check.py file1.STL [file2.STL ...]
    python3 tools/stl_check.py --all stl/
"""
import glob
import os
import struct
import sys
from collections import defaultdict

EPS = 1e-4  # 顶点量化精度 (mm)


def load_tris(path):
    with open(path, "rb") as f:
        head = f.read(84)
        if len(head) < 84:
            raise ValueError("文件不足 84 字节")
        n = struct.unpack("<I", head[80:84])[0]
        if os.path.getsize(path) != 84 + n * 50:
            raise ValueError(f"字节数与三角面数不符 (期望 {84 + n * 50})")
        data = f.read(n * 50)
    tris, normals = [], []
    for i in range(n):
        off = i * 50
        normals.append(struct.unpack_from("<3f", data, off))
        v = struct.unpack_from("<9f", data, off + 12)
        tris.append((v[0:3], v[3:6], v[6:9]))
    return tris, normals


def key(p):
    return (round(p[0] / EPS), round(p[1] / EPS), round(p[2] / EPS))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def norm(v):
    return (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) ** 0.5


def check(path):
    tris, normals = load_tris(path)
    res = {"file": os.path.basename(path), "tris": len(tris)}

    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    vol = area = 0.0
    degen = 0
    bad_normal = 0.0  # 存储法向与几何法向反向的三角形数

    for (a, b, c), sn in zip(tris, normals):
        for p in (a, b, c):
            for k in range(3):
                lo[k] = min(lo[k], p[k])
                hi[k] = max(hi[k], p[k])
        cr = cross(sub(b, a), sub(c, a))
        n2 = norm(cr)
        area += n2 / 2.0
        if n2 < 1e-12:
            degen += 1
        vol += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
        sn_len = norm(sn)
        if sn_len > 1e-9 and n2 > 1e-12:
            if (sn[0] * cr[0] + sn[1] * cr[1] + sn[2] * cr[2]) < 0:
                bad_normal += 1

    # 边统计（水密性 + 朝向一致性）
    undirected = defaultdict(int)
    directed = defaultdict(int)
    for a, b, c in tris:
        ks = [key(a), key(b), key(c)]
        for i in range(3):
            u, v = ks[i], ks[(i + 1) % 3]
            directed[(u, v)] += 1
            undirected[(u, v) if u <= v else (v, u)] += 1

    boundary = sum(1 for k, n in undirected.items() if n == 1)
    nonmanifold = sum(1 for k, n in undirected.items() if n > 2)
    flipped = sum(1 for n in directed.values() if n > 1)

    # 独立壳体数（顶点并查集）
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b, c in tris:
        ka, kb, kc = key(a), key(b), key(c)
        union(ka, kb)
        union(kb, kc)
    shells = len({find(x) for x in list(parent)})

    res.update(
        bbox=tuple(round(hi[k] - lo[k], 2) for k in range(3)),
        vol_cm3=vol / 1000.0,
        area_cm2=area / 100.0,
        degen=degen,
        bad_normal=bad_normal,
        boundary_edges=boundary,
        nonmanifold_edges=nonmanifold,
        flipped_edges=flipped,
        shells=shells,
        watertight=(boundary == 0 and nonmanifold == 0 and flipped == 0),
        normals_outward=(vol > 0),
    )
    return res


def fmt(r):
    w = "水密" if r["watertight"] else "不水密"
    o = "法向朝外" if r["normals_outward"] else "法向朝内(体积为负)"
    lines = [
        f"{r['file']}",
        f"  三角面 {r['tris']}   包围盒 {r['bbox'][0]}×{r['bbox'][1]}×{r['bbox'][2]} mm",
        f"  体积 {abs(r['vol_cm3']):.2f} cm³   表面积 {r['area_cm2']:.1f} cm²   {o}",
        f"  独立壳体 {r['shells']}   退化面 {r['degen']}   存储法向反向 {r['bad_normal']:.0f}",
        f"  边检查: 边界边 {r['boundary_edges']}   非流形边 {r['nonmanifold_edges']}   "
        f"同向重复边 {r['flipped_edges']}  → {w}",
    ]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--all":
        root = args[1] if len(args) > 1 else "stl"
        paths = sorted(glob.glob(os.path.join(root, "*.STL")) + glob.glob(os.path.join(root, "*.stl")))
    else:
        paths = args
    bad = 0
    for p in paths:
        r = check(p)
        print(fmt(r))
        if not (r["watertight"] and r["normals_outward"] and r["degen"] == 0):
            bad += 1
        print()
    if len(paths) > 1:
        print(f"共 {len(paths)} 个文件，异常 {bad} 个")


if __name__ == "__main__":
    main()

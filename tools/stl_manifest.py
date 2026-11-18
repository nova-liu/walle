#!/usr/bin/env python3
"""扫描 STL 目录，校验文件并生成加工清单（CSV + Markdown）。

用法:
    python3 tools/stl_manifest.py [stl_dir]

输出:
    stl/parts-manifest.csv
    stl/parts-manifest.md
"""
import csv
import os
import re
import struct
import sys

QTY_RE = re.compile(r"-x(\d+)\.stl$", re.IGNORECASE)
VARIANT_RE = re.compile(r"-\d+\.stl$", re.IGNORECASE)
VARIANT_WORDS = ("larger", "replica", "longer")

# 文件名里没有 -xN、但实际要打多份的，在这里覆写。
# eye-camera-replica / eye-camera-mount 是同一只眼的互换件（外径同为 ⌀40.9，
# 中心孔 ⌀2.3 / ⌀12.0），官方默认只打 replica×2。本项目选择两套各打一对，
# 两种眼睛方案都能试错。
QTY_OVERRIDE = {
    "eye-camera-replica": 2,
    "eye-camera-mount": 2,
}


def read_binary(path):
    """返回 (triangles, bbox, volume_mm3)；非二进制 STL 返回 None。"""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(84)
        if len(head) < 84:
            return None
        n = struct.unpack("<I", head[80:84])[0]
        if size != 84 + n * 50:
            return None
        data = f.read(n * 50)
    tris = []
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    vol = 0.0
    for i in range(n):
        off = i * 50 + 12  # 跳过法向量
        v = struct.unpack_from("<9f", data, off)
        a, b, c = v[0:3], v[3:6], v[6:9]
        for p in (a, b, c):
            for k in range(3):
                lo[k] = min(lo[k], p[k])
                hi[k] = max(hi[k], p[k])
        # 有符号四面体体积求和
        vol += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
        tris.append(None)
    return n, (lo, hi), abs(vol)


def read_ascii(path):
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    n = 0
    with open(path, "r", errors="ignore") as f:
        for line in f:
            s = line.split()
            if len(s) == 4 and s[0] == "vertex":
                n += 1
                p = [float(x) for x in s[1:]]
                for k in range(3):
                    lo[k] = min(lo[k], p[k])
                    hi[k] = max(hi[k], p[k])
    return n // 3, (lo, hi), None


def print_name(name):
    """交付用文件名：去掉 -xN 数量后缀，扩展名统一小写 .stl。

    数量只写在清单里；扩展名小写是因为部分代加工平台的扩展名校验区分大小写，
    .STL 会被判为不支持的类型直接拒绝上传。
    """
    stem = re.sub(r"-x\d+(\.stl)$", r"\1", name, flags=re.IGNORECASE)
    return re.sub(r"\.stl$", ".stl", stem, flags=re.IGNORECASE)


def qty_from_name(name):
    m = QTY_RE.search(name)
    return int(m.group(1)) if m else 1


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "stl"
    rows = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            if not fn.lower().endswith(".stl"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            info = read_binary(path)
            fmt = "binary"
            if info is None:
                info = read_ascii(path)
                fmt = "ascii"
            n, (lo, hi), vol = info
            size = [hi[k] - lo[k] for k in range(3)]
            worst = max(size)
            note = []
            is_ref = "notforprinting" in fn.lower()
            qty = qty_from_name(fn)
            stem = os.path.splitext(fn)[0]
            if stem in QTY_OVERRIDE:
                qty = QTY_OVERRIDE[stem]
                note.append("数量按项目口径覆写")
            alt = bool(VARIANT_RE.search(fn))
            if is_ref:
                note.append("装配总成，不打印")
            if qty == 0:
                note.append("数量 0，可选件")
            if alt:
                note.append("同族变体，与无后缀件三选一")
            if any(w in fn.lower() for w in VARIANT_WORDS):
                note.append("替换/可选版本")
            if worst > 256:
                note.append("超出 256mm 打印床，需切分")
            # 建议数量：装配总成与同族变体不计入
            suggest = 0 if (is_ref or alt) else qty
            rows.append(
                {
                    "file": rel,
                    "print_name": print_name(rel),
                    "qty_in_name": qty,
                    "suggest_qty": suggest,
                    "format": fmt,
                    "triangles": n,
                    "size_mm": "x".join(f"{s:.1f}" for s in size),
                    "max_dim_mm": round(worst, 1),
                    "volume_cm3": None if vol is None else round(vol / 1000.0, 2),
                    "bytes": os.path.getsize(path),
                    "note": "; ".join(note),
                }
            )

    rows.sort(key=lambda r: r["file"])
    csv_path = os.path.join(root, "parts-manifest.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    total_qty = sum(r["suggest_qty"] for r in rows)
    total_files = sum(1 for r in rows if r["suggest_qty"] > 0)
    total_vol = sum((r["volume_cm3"] or 0) * r["suggest_qty"] for r in rows)
    md = os.path.join(root, "parts-manifest.md")
    with open(md, "w") as f:
        f.write("# WALL·E 3D 打印件清单\n\n")
        f.write(f"- STL 文件总数：**{len(rows)}**；需打印的文件：**{total_files}**\n")
        f.write(f"- 需打印件数（按文件名 xN 累加，已剔除变体/装配件）：**{total_qty}**\n")
        f.write(f"- 实体体积合计：**{total_vol:.0f} cm³**（100% 实心；按 15% 填充 + 3 层墙估算，实际耗材约 600–900 g）\n\n")
        f.write("| # | 文件 | 数量 | 尺寸 mm | 三角面 | 体积 cm³ | 备注 |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(rows, 1):
            f.write(
                f"| {i} | `{r['file']}` | {r['suggest_qty']} | {r['size_mm']} | {r['triangles']} "
                f"| {r['volume_cm3'] if r['volume_cm3'] is not None else '-'} | {r['note']} |\n"
            )
    print(f"files={len(rows)} qty={total_qty} volume={total_vol:.0f}cm3")
    print(f"wrote {csv_path}")
    print(f"wrote {md}")


if __name__ == "__main__":
    main()

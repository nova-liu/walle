#!/usr/bin/env python3
"""把 to-print/ 的二进制 STL 转成 ASCII STL，生成兜底包 to-print-ascii/ + zip。

用途：少数代加工平台只支持 ASCII STL，二进制会被判为无法识别。
ASCII 版体积约为二进制的 5–6 倍，但兼容性最好——任何解析器都能读。

用法:
    python3 tools/make_ascii_fallback.py
"""
import os
import shutil
import struct
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "to-print")
OUT = os.path.join(ROOT, "to-print-ascii")
ZIP_PATH = os.path.join(ROOT, "to-print-ascii.zip")


def convert(src, dst):
    raw = open(src, "rb").read()
    n = struct.unpack("<I", raw[80:84])[0]
    name = os.path.splitext(os.path.basename(src))[0]
    out = [f"solid {name}"]
    for i in range(n):
        off = 84 + i * 50
        nx, ny, nz = struct.unpack_from("<3f", raw, off)
        v = struct.unpack_from("<9f", raw, off + 12)
        out.append(f"  facet normal {nx:.6e} {ny:.6e} {nz:.6e}")
        out.append("    outer loop")
        for k in range(3):
            x, y, z = v[k * 3:k * 3 + 3]
            out.append(f"      vertex {x:.6e} {y:.6e} {z:.6e}")
        out.append("    endloop")
        out.append("  endfacet")
    out.append(f"endsolid {name}")
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")
    return n


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"缺少源目录 {SRC}")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    stls = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".stl"))
    total = 0
    for f in stls:
        total += convert(os.path.join(SRC, f), os.path.join(OUT, f))
    for extra in ("数量表.csv", "加工说明.md"):
        p = os.path.join(SRC, extra)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(OUT, extra))

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    base = os.path.basename(OUT)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in sorted(os.listdir(OUT)):
            z.write(os.path.join(OUT, n), f"{base}/{n}")

    # 回读校验：ASCII 能被"朴素解析器"按 facet 数量正确解析
    bad = []
    for f in stls:
        txt = open(os.path.join(OUT, f), "rb").read()
        nf = txt.count(b"facet normal")
        nv = txt.count(b"vertex ")
        if nf == 0 or nv != nf * 3:
            bad.append(f)
    print(f"转换 {len(stls)} 个文件，合计 {total} 个三角面")
    print(f"输出目录 : {OUT}")
    print(f"压缩包   : {ZIP_PATH}  ({os.path.getsize(ZIP_PATH)/1048576:.2f} MB)")
    print("回读校验 :", "全部通过" if not bad else f"异常 {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

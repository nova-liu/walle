#!/usr/bin/env python3
"""从 parts-manifest.csv 生成可交付的打印包（文件夹 + zip）。

用法:
    python3 tools/make_print_set.py            # 生成 to-print/ 和 to-print.zip

做的事:
    1. 读 stl/parts-manifest.csv，取出 suggest_qty > 0 的文件
    2. 建 out_dir（默认 to-print/），按 print_name 复制（文件名不含 -xN，数量只写在表里）
    3. 额外放两份非模型文件：数量表.csv / 加工说明.md
    4. 打 zip（顶层目录名 = out_dir 名）
    5. 自检：件数、文件数、每个 STL 的二进制结构、zip CRC
"""
import binascii
import csv
import re
import os
import shutil
import struct
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "stl")
MANIFEST = os.path.join(SRC, "parts-manifest.csv")
OUT_DIR = os.path.join(ROOT, "to-print")
ZIP_PATH = os.path.join(ROOT, "to-print.zip")
QTY_SHEET = "数量表.csv"
NOTE = "加工说明.md"


def load_manifest():
    rows = list(csv.DictReader(open(MANIFEST)))
    keep = [r for r in rows if int(r["suggest_qty"]) > 0]
    return sorted(keep, key=lambda r: r["file"])


# 80 字节的 STL 头是自由文本。作者的导出器把文件名写进去，导致二进制 STL 的头
# 恰好以 "solid " 开头。按规范 sniff 格式的解析器（见到 solid 就当 ASCII）会把它
# 读成 0 个三角面，于是代加工平台显示 "尺寸 0*0*0 / 体积 0"。
# 这里把头部改写成不以 solid 开头的普通注释，几何数据一个字节都不动。
HEADER_PREFIX = b"WALL-E print set - binary STL, units mm"


def sanitize_header(path):
    """重写 80 字节头，返回 (旧头, 新头)；几何数据保持逐字节不变。"""
    with open(path, "r+b") as f:
        old = f.read(80)
        new = HEADER_PREFIX[:80].ljust(80, b" ")
        if old[:5].lower() == b"solid":
            f.seek(0)
            f.write(new)
            f.flush()
            return old, new
        return old, old


def stl_ok(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(84)
    if len(head) < 84:
        return False
    n = struct.unpack("<I", head[80:84])[0]
    return size == 84 + n * 50


def main():
    rows = load_manifest()
    total_qty = sum(int(r["suggest_qty"]) for r in rows)

    # 重建输出目录（先删旧产物，避免残留过期文件）
    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    missing = []
    seen = {}
    fixed_headers = 0
    for r in rows:
        src = os.path.join(SRC, r["file"])
        if not os.path.exists(src):
            missing.append(r["file"])
            continue
        dst_name = r["print_name"]
        if dst_name in seen:
            sys.exit(f"交付文件名冲突: {dst_name} <- {seen[dst_name]} / {r['file']}")
        seen[dst_name] = r["file"]
        dst = os.path.join(OUT_DIR, dst_name)
        shutil.copy2(src, dst)
        old_h, new_h = sanitize_header(dst)
        if old_h != new_h:
            fixed_headers += 1
    if missing:
        sys.exit(f"缺少文件: {missing}")

    # 数量表：加工厂照这张表摆盘，数量只此一处
    with open(os.path.join(OUT_DIR, QTY_SHEET), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["文件名", "数量"])
        for r in sorted(rows, key=lambda r: -int(r["suggest_qty"])):
            w.writerow([r["print_name"], r["suggest_qty"]])
        w.writerow(["合计", total_qty])

    src_note = os.path.join(SRC, NOTE)
    if os.path.exists(src_note):
        shutil.copy2(src_note, os.path.join(OUT_DIR, NOTE))

    # 打 zip
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    base = os.path.basename(OUT_DIR)
    names = sorted(os.listdir(OUT_DIR))
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in names:
            z.write(os.path.join(OUT_DIR, n), f"{base}/{n}")

    # ---- 自检 ----
    errs = []
    stls = [n for n in os.listdir(OUT_DIR) if n.lower().endswith(".stl")]
    if len(stls) != len(rows):
        errs.append(f"STL 数 {len(stls)} != 清单可打印文件数 {len(rows)}")
    solid_head = [n for n in stls if open(os.path.join(OUT_DIR, n), "rb").read(5).lower() == b"solid"]
    if solid_head:
        errs.append(f"仍有以 solid 开头的二进制头: {solid_head}")
    leftover = [n for n in stls if re.search(r"-x\d+\.stl$", n, re.I)]
    if leftover:
        errs.append(f"交付文件名仍含 -xN: {leftover}")
    bad = [n for n in stls if not stl_ok(os.path.join(OUT_DIR, n))]
    if bad:
        errs.append(f"结构非法的 STL: {bad}")
    with zipfile.ZipFile(ZIP_PATH) as z:
        if z.testzip():
            errs.append("zip 自检失败")
        for info in z.infolist():
            p = os.path.join(OUT_DIR, os.path.basename(info.filename))
            if (binascii.crc32(open(p, "rb").read()) & 0xFFFFFFFF) != info.CRC:
                errs.append(f"zip 内 CRC 不符: {info.filename}")

    print(f"输出目录 : {OUT_DIR}")
    print(f"压缩包   : {ZIP_PATH}  ({os.path.getsize(ZIP_PATH)/1048576:.2f} MB)")
    print(f"STL 文件 : {len(stls)}   合计件数: {total_qty}")
    print(f"附件     : {QTY_SHEET} / {NOTE}")
    print(f"头清洗   : {fixed_headers} 个文件的 80 字节头已改写（几何未动）")
    print("自检     :", "全部通过" if not errs else errs)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

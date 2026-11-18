#!/usr/bin/env python3
"""把 STL 的 80 字节头改写成不以 "solid" 开头的注释（几何数据不动）。

背景：作者的导出器把文件名写进二进制 STL 的头 80 字节，导致头部以 "solid "
开头。按规范 sniff 格式的解析器会据此判定为 ASCII STL，在二进制文件里找不到
facet 关键字，于是报 0 个三角面（代加工平台显示 "尺寸 0*0*0 / 体积 0"）。

80 字节头在 STL 规范里是自由文本注释，改写不影响任何几何。

用法:
    python3 tools/stl_fix_headers.py <dir> [<dir> ...]
    python3 tools/stl_fix_headers.py --check <dir>     # 只检查不改
"""
import os
import sys

HEADER = b"WALL-E print set - binary STL, units mm"


def fix_one(path):
    with open(path, "r+b") as f:
        old = f.read(80)
        if old[:5].lower() != b"solid":
            return False
        f.seek(0)
        f.write(HEADER[:80].ljust(80, b" "))
        f.flush()
        return True


def main():
    args = sys.argv[1:]
    check_only = False
    if args and args[0] == "--check":
        check_only = True
        args = args[1:]
    if not args:
        sys.exit(__doc__)
    total = fixed = bad = 0
    for d in args:
        for name in sorted(os.listdir(d)):
            if not name.lower().endswith(".stl"):
                continue
            total += 1
            p = os.path.join(d, name)
            if open(p, "rb").read(5).lower() == b"solid":
                if check_only:
                    bad += 1
                    print(f"  solid 头: {p}")
                elif fix_one(p):
                    fixed += 1
    if check_only:
        print(f"{d}: 检查 {total} 个，仍以 solid 开头 {bad} 个")
        return 1 if bad else 0
    print(f"扫描 {total} 个 STL，改写头部 {fixed} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())

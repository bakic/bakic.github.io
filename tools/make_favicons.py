#!/usr/bin/env python3
"""Rasterise the favicon geometry (same as static/favicon.svg) to PNG + ICO. Stdlib only."""
import math, struct, zlib, sys

BG, FG = (0x0b, 0x3b, 0x3d), (0x8e, 0xe5, 0xda)
SEGS = [((20, 50), (32, 14)), ((32, 14), (44, 50)), ((24.5, 38), (39.5, 38))]
W, R = 6.5, 14

def dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def in_round_rect(x, y):
    cx = min(max(x, R), 64 - R); cy = min(max(y, R), 64 - R)
    return math.hypot(x - cx, y - cy) <= R

def render(size, ss=4):
    rows = []
    for j in range(size):
        row = bytearray()
        for i in range(size):
            r = g = b = a = 0
            for sj in range(ss):
                for si in range(ss):
                    x = (i + (si + .5) / ss) * 64 / size
                    y = (j + (sj + .5) / ss) * 64 / size
                    if not in_round_rect(x, y):
                        continue
                    fg = any(dist((x, y), s, e) <= W / 2 for s, e in SEGS)
                    c = FG if fg else BG
                    r += c[0]; g += c[1]; b += c[2]; a += 255
            n = ss * ss
            if a:
                cnt = a // 255
                row += bytes((r // cnt, g // cnt, b // cnt, a // n))
            else:
                row += bytes(4)
        rows.append(bytes(row))
    return rows

def png(size):
    raw = b"".join(b"\x00" + r for r in render(size))
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

out = sys.argv[1] if len(sys.argv) > 1 else "static"
p180, p32 = png(180), png(32)
open(f"{out}/apple-touch-icon.png", "wb").write(p180)
open(f"{out}/favicon-32.png", "wb").write(p32)
# ICO with one embedded 32x32 PNG
ico = struct.pack("<HHH", 0, 1, 1) + struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(p32), 22) + p32
open(f"{out}/favicon.ico", "wb").write(ico)

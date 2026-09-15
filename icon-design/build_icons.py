#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TimeDisplay 图标生成器
=====================

用途：用纯矢量（SVG）定义 TimeDisplay 的新 App Icon，并渲染成
macOS 资产目录需要的全部尺寸。

设计要点
--------
1. 图标底板使用**真正的 Apple superellipse（|x/a|^n + |y/a|^n = 1, n = 5）**，
   而不是 CSS 那种圆弧圆角矩形。n = 5 的 superellipse 在 45° 方向的收敛点与
   Apple 规范（824 安全区 / 184.3 圆角）几乎完全重合，因此底板轮廓是真的对。
2. 画布 1024×1024，内容限制在居中 824×824 安全区内（四周各留白 100px），
   这是 Big Sur 之后 macOS App Icon 的网格规范。
3. 三个概念（A/B/C）共用同一套几何骨架与底板，只替换前景母题，
   方便对比与一键切换。

用法
----
    python3 icon-design/build_icons.py               # 渲染全部概念 + 安装 A
    python3 icon-design/build_icons.py --concept A   # 指定安装哪个概念（A/B/C）
    python3 icon-design/build_icons.py --render-only # 只渲染，不动资产目录
"""

import argparse
import math
import os
import shutil
import subprocess
import sys

from PIL import Image

# ---------------------------------------------------------------- 常量与网格

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGN_DIR = os.path.join(ROOT, "icon-design")
RENDER_DIR = os.path.join(DESIGN_DIR, "render")
APPICON_DIR = os.path.join(ROOT, "TimeDisplay", "Assets.xcassets", "AppIcon.appiconset")
MENUBAR_DIR = os.path.join(ROOT, "TimeDisplay", "Assets.xcassets", "MenuBarIcon.imageset")

CANVAS = 1024          # 画布边长
BODY = 824             # 安全区边长（Big Sur 规范）
MARGIN = (CANVAS - BODY) / 2   # 100
SUPERELLIPSE_N = 5.0   # Apple squircle 的等价指数

# 资产目录要求的 10 档尺寸（文件名 -> 像素）
ICON_SIZES = [
    ("Icon-16.png", 16),
    ("Icon-16@2x.png", 32),
    ("Icon-32.png", 32),
    ("Icon-32@2x.png", 64),
    ("Icon-128.png", 128),
    ("Icon-128@2x.png", 256),
    ("Icon-256.png", 256),
    ("Icon-256@2x.png", 512),
    ("Icon-512.png", 512),
    ("Icon-512@2x.png", 1024),
]

SS = 4  # 超采样倍率：先按 4 倍渲染再用 LANCZOS 缩回，边缘最干净


# ---------------------------------------------------------------- 路径工具

def squircle_path(cx, cy, w, h, n=SUPERELLIPSE_N, steps=1440):
    """生成 superellipse 的多边形路径（高密度折线在光栅化时等同曲线）。"""
    a, b = w / 2.0, h / 2.0
    pts = []
    for i in range(steps):
        t = 2.0 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = cx + a * math.copysign(abs(ct) ** (2.0 / n), ct)
        y = cy + b * math.copysign(abs(st) ** (2.0 / n), st)
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    return d


def rrect_path(x, y, w, h, r):
    """普通圆角矩形路径（前景母题用）。"""
    r = min(r, w / 2.0, h / 2.0)
    return (
        f"M{x + r:.2f},{y:.2f} H{x + w - r:.2f} "
        f"A{r:.2f},{r:.2f} 0 0 1 {x + w:.2f},{y + r:.2f} "
        f"V{y + h - r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + w - r:.2f},{y + h:.2f} "
        f"H{x + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x:.2f},{y + h - r:.2f} "
        f"V{y + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + r:.2f},{y:.2f} Z"
    )


def circle_path(cx, cy, r):
    return f"M{cx - r:.2f},{cy:.2f} a{r:.2f},{r:.2f} 0 1 0 {2 * r:.2f},0 a{r:.2f},{r:.2f} 0 1 0 {-2 * r:.2f},0 Z"


def svg_document(defs, body):
    """把 defs 与前景内容包成完整 SVG。"""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS}" height="{CANVAS}" '
        f'viewBox="0 0 {CANVAS} {CANVAS}">\n'
        f"<defs>\n{defs}\n</defs>\n{body}\n</svg>\n"
    )


# ---------------------------------------------------------------- 共用底板

def plate(plate_from, plate_to, edge_opacity=0.07):
    """深色底板：垂直渐变 + 顶部环境光 + 极细边缘高光，不含任何投影。"""
    c = CANVAS / 2.0
    defs = f"""  <linearGradient id="plate" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{plate_from}"/>
    <stop offset="1" stop-color="{plate_to}"/>
  </linearGradient>
  <linearGradient id="toplight" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/>
    <stop offset="34%" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>"""
    body = (
        f'<path d="{squircle_path(c, c, BODY, BODY)}" fill="url(#plate)"/>\n'
        f'<path d="{squircle_path(c, c, BODY, BODY)}" fill="url(#toplight)"/>\n'
        f'<path d="{squircle_path(c, c, BODY, BODY)}" fill="none" '
        f'stroke="#FFFFFF" stroke-opacity="{edge_opacity}" stroke-width="2"/>'
    )
    return defs, body


# ---------------------------------------------------------------- 概念 A《断秒》

PALETTE_DARK = {
    "plate_from": "#1A2027", "plate_to": "#11161B",
    "top_from": "#F5F3EE", "top_to": "#DCD9D2",
    "bot_from": "#A3AEBA", "bot_to": "#828E99",
    "seam": "#7FE3C4", "seam_in": 0.34, "seam_out": 0.10,
    "edge": 0.07,
}

PALETTE_LIGHT = {
    "plate_from": "#F6F4EF", "plate_to": "#E6E3DC",
    "top_from": "#1E2228", "top_to": "#2C3138",
    "bot_from": "#949BA4", "bot_to": "#767D86",
    "seam": "#12A57F", "seam_in": 0.22, "seam_out": 0.07,
    "edge": 0.10,
}


def concept_a(pal=PALETTE_DARK):
    """《断秒 / The Interval》—— 冒号本体被放大成主角。

    上方块 = 时，下方块 = 分，两块的间隙就是冒号，也是"秒"发生的地方；
    间隙里那层薄荷青呼吸光是全图唯一彩色，面积 < 5%。
    """
    c = CANVAS / 2.0
    bar_w = BODY * 0.46          # 379.0
    bar_h = BODY * 0.30          # 247.2
    side = MARGIN + (BODY - bar_w) / 2.0
    top_y = MARGIN + BODY * 0.08
    bot_y = top_y + bar_h + BODY * 0.24

    defs = f"""  <linearGradient id="barTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{pal['top_from']}"/>
    <stop offset="1" stop-color="{pal['top_to']}"/>
  </linearGradient>
  <linearGradient id="barBot" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{pal['bot_from']}"/>
    <stop offset="1" stop-color="{pal['bot_to']}"/>
  </linearGradient>
  <radialGradient id="seam" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{pal['seam']}" stop-opacity="{pal['seam_in']}"/>
    <stop offset="50%" stop-color="{pal['seam']}" stop-opacity="{pal['seam_out']}"/>
    <stop offset="100%" stop-color="{pal['seam']}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="plateClip"><path d="{squircle_path(c, c, BODY, BODY)}"/></clipPath>"""

    p_defs, p_body = plate(pal["plate_from"], pal["plate_to"], pal["edge"])
    defs = p_defs + "\n" + defs

    r = bar_w * 0.224   # 85.0：与底板同源的曲率，形成"小 squircle"自相似
    body = p_body + "\n" + f"""<path d="{rrect_path(side, top_y, bar_w, bar_h, r)}" fill="url(#barTop)"/>
<path d="{rrect_path(side, bot_y, bar_w, bar_h, r)}" fill="url(#barBot)"/>
<g clip-path="url(#plateClip)">
  <ellipse cx="{c}" cy="{c}" rx="286" ry="132" fill="url(#seam)"/>
</g>"""
    return svg_document(defs, body)


# ---------------------------------------------------------------- 概念 B《密度》

def concept_b():
    """《密度 / Cadence》—— 不画时间，画时间的密度。

    左侧密实的梳齿向右逐根变窄变矮变淡，唯一一根高饱和强调色代表"此刻"。
    """
    c = CANVAS / 2.0
    n = 12
    area_w = BODY * 0.72          # 593.3
    area_x = MARGIN + (BODY - area_w) / 2.0
    base_y = MARGIN + BODY * 0.79 # 共同底边
    h_max, h_min = BODY * 0.58, BODY * 0.58 * 0.34
    accents = [1.0, 1.0, 1.0, 0.62, 0.62, 0.62, 0.38, 0.38, 0.38, 0.22, 0.22, 0.22]
    accent_i = 8

    # 棒宽递减、间隙递增，再整体缩放铺满 area_w
    w0, w1 = 40.0, 12.0
    g0, g1 = 6.0, 30.0
    raw = sum(w0 + (w1 - w0) * i / (n - 1) for i in range(n)) + \
          sum(g0 + (g1 - g0) * i / (n - 2) for i in range(n - 1))
    k = area_w / raw

    defs = """  <radialGradient id="seam" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#FF6B4A" stop-opacity="0.30"/>
    <stop offset="100%" stop-color="#FF6B4A" stop-opacity="0"/>
  </radialGradient>"""
    p_defs, p_body = plate("#1F232A", "#161A20")
    defs = p_defs + "\n" + defs

    x = area_x
    bars = []
    for i in range(n):
        w = (w0 + (w1 - w0) * i / (n - 1)) * k
        if i == accent_i:
            w *= 1.4
        h = h_min + (h_max - h_min) * (1 - i / (n - 1)) ** 1.3
        if i == accent_i:
            fill, op = "#FF6B4A", 1.0
        else:
            fill, op = "#FFFFFF", accents[i]
        bars.append(
            f'<path d="{rrect_path(x, base_y - h, w, h, w / 2)}" '
            f'fill="{fill}" fill-opacity="{op}"/>'
        )
        if i < n - 1:
            x += w + (g0 + (g1 - g0) * i / (n - 2)) * k

    body = p_body + "\n" + "\n".join(bars)
    return svg_document(defs, body)


# ---------------------------------------------------------------- 概念 C《穿过》

def concept_c():
    """《穿过 / The Pass-Through》—— 把"菜单栏"画成主角。

    一条横贯的胶囊＝菜单栏本身；两枚圆点＝时与分；横线在竖线处被挖空，
    竖线（秒）正在穿过它。
    """
    c = CANVAS / 2.0
    line_w, line_h = BODY * 0.76, BODY * 0.055      # 626.2 × 45.3
    line_x = MARGIN + (BODY - line_w) / 2.0
    line_cy = c
    dot_d = BODY * 0.10                              # 82.4：读数珠，不是第二主体
    dot1_cx = line_x + line_w * 0.145
    dot2_cx = line_x + line_w * 0.355
    vbar_w, vbar_h = BODY * 0.050, BODY * 0.50       # 41.2 × 412.0
    vbar_cx = MARGIN + BODY * 0.68
    gap = BODY * 0.02                                # 16.5 断口

    left_w = (vbar_cx - vbar_w / 2 - gap) - line_x
    right_x = vbar_cx + vbar_w / 2 + gap
    right_w = (line_x + line_w) - right_x

    defs = """  <linearGradient id="mint" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#45D9A0"/>
    <stop offset="1" stop-color="#2FB784"/>
  </linearGradient>"""
    p_defs, p_body = plate("#131922", "#0C1016")
    defs = p_defs + "\n" + defs

    body = p_body + "\n" + f"""<path d="{rrect_path(line_x, line_cy - line_h / 2, left_w, line_h, line_h / 2)}" fill="#F5F5F7"/>
<path d="{rrect_path(right_x, line_cy - line_h / 2, right_w, line_h, line_h / 2)}" fill="#F5F5F7"/>
<path d="{circle_path(dot1_cx, line_cy, dot_d / 2)}" fill="#FFFFFF"/>
<path d="{circle_path(dot2_cx, line_cy, dot_d / 2)}" fill="#FFFFFF"/>
<path d="{rrect_path(vbar_cx - vbar_w / 2, c - vbar_h / 2, vbar_w, vbar_h, vbar_w / 2)}" fill="url(#mint)"/>"""
    return svg_document(defs, body)


CONCEPTS = {
    "A": ("《断秒》The Interval", concept_a),
    "B": ("《密度》Cadence", concept_b),
    "C": ("《穿过》The Pass-Through", concept_c),
    "A-light": ("《断秒》浅色版（自定义浅色主题）", lambda: concept_a(PALETTE_LIGHT)),
}


# ---------------------------------------------------------------- 渲染

def render_svg(svg_path, out_png, size):
    """SVG -> PNG：先 4 倍超采样渲染，再 LANCZOS 缩到目标尺寸。"""
    big = out_png.replace(".png", f"@{SS}x.png")
    subprocess.run(
        ["rsvg-convert", "-w", str(size * SS), "-h", str(size * SS), svg_path, "-o", big],
        check=True,
    )
    img = Image.open(big).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(out_png, "PNG")
    os.remove(big)
    return out_png


def render_all(concept_key):
    """渲染一个概念的全部尺寸；矢量源每个概念只保留一份 icon.svg。"""
    svg_text = CONCEPTS[concept_key][1]()
    out_dir = os.path.join(RENDER_DIR, concept_key)
    os.makedirs(out_dir, exist_ok=True)
    svg_path = os.path.join(out_dir, "icon.svg")
    with open(svg_path, "w") as f:
        f.write(svg_text)
    for s in (1024, 512, 256, 128, 64, 32, 16):
        render_svg(svg_path, os.path.join(out_dir, f"icon-{s}.png"), s)
    return out_dir, os.path.join(out_dir, "icon-1024.png")


# ---------------------------------------------------------------- 安装

def install_appicon(master_png):
    """把主图铺进 AppIcon.appiconset 的全部 10 档。"""
    src = Image.open(master_png).convert("RGBA")
    for name, size in ICON_SIZES:
        src.resize((size, size), Image.Resampling.LANCZOS).save(
            os.path.join(APPICON_DIR, name), "PNG"
        )
    shutil.copyfile(master_png, os.path.join(ROOT, "app_icon.png"))
    print(f"  ✓ 已写入 {len(ICON_SIZES)} 档 PNG 到 AppIcon.appiconset")
    print("  ✓ 已更新仓库主图 app_icon.png")


def build_menubar_template():
    """菜单栏模板图标：app 图标母题的等缩版（两枚圆角块 + 一道缝）。

    必须提交为 template image（纯黑 + alpha），系统会自动适配深浅菜单栏。
    """
    def glyph(px):
        u = px / 36.0
        w, h, r = 13 * u, 11 * u, 3.6 * u
        x = (px - w) / 2.0
        y1, y2 = 5.0 * u, 20.0 * u
        d = rrect_path(x, y1, w, h, r) + " " + rrect_path(x, y2, w, h, r)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" '
            f'viewBox="0 0 {px} {px}"><path d="{d}" fill="#000000"/></svg>'
        )

    os.makedirs(MENUBAR_DIR, exist_ok=True)
    for name, px in (("menubar-18.png", 18), ("menubar-18@2x.png", 36)):
        p = os.path.join(MENUBAR_DIR, name)
        svg_path = p.replace(".png", ".svg")
        with open(svg_path, "w") as f:
            f.write(glyph(px))
        render_svg(svg_path, p, px)

    with open(os.path.join(MENUBAR_DIR, "Contents.json"), "w") as f:
        f.write("""{
  "images" : [
    { "filename" : "menubar-18.png", "idiom" : "mac", "scale" : "1x" },
    { "filename" : "menubar-18@2x.png", "idiom" : "mac", "scale" : "2x" }
  ],
  "info" : { "author" : "xcode", "version" : 1 },
  "properties" : { "template-rendering-intent" : "template" }
}
""")
    print("  ✓ 已生成菜单栏模板图标 MenuBarIcon.imageset")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept", default="A", choices=list(CONCEPTS))
    ap.add_argument("--render-only", action="store_true")
    args = ap.parse_args()

    for key, (title, _) in CONCEPTS.items():
        out_dir, _ = render_all(key)
        print(f"  ✓ 概念 {key} {title} -> {os.path.relpath(out_dir, ROOT)}")

    if args.render_only:
        return

    print(f"安装概念 {args.concept} {CONCEPTS[args.concept][0]} ...")
    _, master = render_all(args.concept)
    install_appicon(master)
    build_menubar_template()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Zenith Icons: original file and folder icons in the Atom Material style.

Style: 24x24 viewBox rendered at 16px, one solid saturated glyph per type (no page
outline), dark detail cut-ins; folders are solid tinted folders with a lighter emblem
bottom-right. All artwork is drawn here; no third-party icons or brand logos.

Usage: python3 brand/icons/generate.py
Writes brand/icons/zenith-icons/ (a Zed icon-theme extension) and mockups/zenith-icons.html.
"""
import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
EXT = HERE / "zenith-icons"
SHEET = HERE.parent.parent / "mockups/zenith-icons.html"
DK = "#263238"  # detail colour cut into glyphs

C = dict(grey="#90a4ae", slate="#78909c", blue="#42a5f5", sky="#4fc3f7", cyan="#26c6da",
         green="#8bc34a", leaf="#66bb6a", teal="#26a69a", yellow="#ffca28", amber="#ffb300",
         ochre="#f9a825", orange="#ff7043", red="#ef5350", pink="#ec407a", purple="#9c8cff",
         indigo="#7986cb", brown="#a1887f", zenith="#ff7a3d")

def st(w=2.4, c="{c}"):
    return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'

def gear_path():
    import math
    teeth = "".join(
        f'<path d="M{12 + 7.6 * math.cos(a):.2f} {12 + 7.6 * math.sin(a):.2f}L{12 + 10.6 * math.cos(a):.2f} {12 + 10.6 * math.sin(a):.2f}" {st(3.6)}/>'
        for a in [i * math.pi / 4 for i in range(8)])
    return teeth + f'<circle cx="12" cy="12" r="6.2" {st(3.6)}/>'

# Each glyph is drawn in a 24x24 box; {c} = main colour.
G = {
 "doc":    f'<path d="M5 3.5A1.5 1.5 0 0 1 6.5 2H14l5 5v13.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 5 20.5z" fill="{{c}}"/><path d="M14 2v5h5" fill="{DK}" fill-opacity=".25"/><path d="M8.5 12h7M8.5 15.5h7M8.5 19h4.5" {st(1.6, DK)} stroke-opacity=".55"/>',
 "docfold":f'<path d="M5 3.5A1.5 1.5 0 0 1 6.5 2H14l5 5v13.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 5 20.5z" fill="{{c}}"/><path d="M14 2v5h5" fill="{DK}" fill-opacity=".25"/><path d="M8 17.5c2.5-1 5-4.5 5.5-7.5.3-1.8-1.4-1.8-1.4 0 0 3 2.6 6.4 4.4 6.7 1.3.2 1.3-1.4-.3-1.5-3-.2-6.5 1.6-8.2 2.3" {st(1.3, DK)} stroke-opacity=".7"/>',
 "php":    f'<ellipse cx="12" cy="12" rx="11" ry="7.2" fill="{{c}}"/><path d="M5.2 9.6v5.8M5.2 10.3h1.7a1.55 1.55 0 0 1 0 3.1H5.2M9.7 7.9v5.6M9.7 11a1.5 1.5 0 0 1 3 0v2.5M15.3 9.6v5.8M15.3 10.3H17a1.55 1.55 0 0 1 0 3.1h-1.7" {st(1.55, DK)}/>',
 "js":     f'<rect x="2.5" y="2.5" width="19" height="19" rx="2.5" fill="{{c}}"/><path d="M11.2 11v5.2a1.9 1.9 0 0 1-3.4 1.1M18.3 11.8a2 2 0 0 0-1.8-.9c-1.1 0-1.9.6-1.9 1.5 0 2.1 3.9 1.3 3.9 3.5 0 .9-.9 1.6-2 1.6a2.3 2.3 0 0 1-2-1" {st(1.9, DK)}/>',
 "ts":     f'<rect x="2.5" y="2.5" width="19" height="19" rx="2.5" fill="{{c}}"/><path d="M6.6 11.3h5.4M9.3 11.3v6.9M18.3 11.8a2 2 0 0 0-1.8-.9c-1.1 0-1.9.6-1.9 1.5 0 2.1 3.9 1.3 3.9 3.5 0 .9-.9 1.6-2 1.6a2.3 2.3 0 0 1-2-1" {st(1.9, DK)}/>',
 "orbit":  f'<g {st(1.6)}><ellipse cx="12" cy="12" rx="10" ry="3.9"/><ellipse cx="12" cy="12" rx="10" ry="3.9" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="3.9" transform="rotate(120 12 12)"/></g><circle cx="12" cy="12" r="2" fill="{{c}}"/>',
 "flask":  f'<path d="M8.5 2h7v2.2h-1.2v4.6l5.6 9.7A2.3 2.3 0 0 1 17.9 22H6.1a2.3 2.3 0 0 1-2-3.5l5.6-9.7V4.2H8.5z" fill="{{c}}"/><path d="M6.2 16h11.6" {st(1.4, DK)} stroke-opacity=".45"/>',
 "gear":   gear_path(),
 "bolt":   '<path d="M13.5 1.5L4 13.8h7.2L9.8 22.5 20 9.8h-7.3z" fill="{c}"/>',
 "brush":  '<path d="M21 3a1.4 1.4 0 0 0-2 0l-9.4 9.4 2 2L21 5a1.4 1.4 0 0 0 0-2z" fill="{c}"/><path d="M8.6 13.8c-3 0-4.8 2-4.8 4.4 0 1-.7 1.7-1.8 2 3.9 1.7 9 .6 9.4-3.6z" fill="{c}"/>',
 "shield": f'<path d="M12 1.8l8.5 3.2v6.6c0 5.3-3.6 9.2-8.5 10.9-4.9-1.7-8.5-5.6-8.5-10.9V5z" fill="{{c}}"/><path d="M8 12l3 3 5.5-6" {st(2, DK)}/>',
 "shieldq":f'<path d="M12 1.8l8.5 3.2v6.6c0 5.3-3.6 9.2-8.5 10.9-4.9-1.7-8.5-5.6-8.5-10.9V5z" fill="{{c}}"/><circle cx="11.2" cy="10.8" r="3.2" {st(1.9, DK)}/><path d="M13.6 13.2l2.6 2.6" {st(2, DK)}/>',
 "checkc": f'<circle cx="12" cy="12" r="10" fill="{{c}}"/><path d="M7 12.4l3.4 3.4L17.2 9" {st(2.3, DK)}/>',
 "hash":   f'<path d="M9.5 2.5L7.3 21.5M16.7 2.5l-2.2 19M3.5 8.2h17.5M2.8 15.8h17.5" {st(2.7)}/>',
 "angle":  f'<path d="M7.5 5L1.8 12l5.7 7M16.5 5l5.7 7-5.7 7" {st(2.6)}/><path d="M14 3.5L10 20.5" {st(2.1)}/>',
 "vee":    '<path d="M1.5 3h5L12 13 17.5 3h5L12 21.5z" fill="{c}"/><path d="M6.5 3H9.6L12 7.4 14.4 3h3.1L12 13z" fill="#263238" fill-opacity=".35"/>',
 "sparkle":'<path d="M12 1.5l2.4 7.1 7.1 2.4-7.1 2.4L12 20.5l-2.4-7.1L2.5 11l7.1-2.4z" fill="{c}"/><path d="M19 15.5l.9 2.6 2.6.9-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9z" fill="{c}"/>',
 "braces": f'<path d="M8.3 3C5.8 3 5.3 4.2 5.3 6v3c0 1.5-.8 2.5-2.6 3 1.8.5 2.6 1.5 2.6 3v3c0 1.8.5 3 3 3M15.7 3c2.5 0 3 1.2 3 3v3c0 1.5.8 2.5 2.6 3-1.8.5-2.6 1.5-2.6 3v3c0 1.8-.5 3-3 3" {st(2.5)}/><circle cx="12" cy="12" r="1.6" fill="{{c}}"/>',
 "box":    f'<path d="M2.8 6.8L12 2l9.2 4.8v10.4L12 22l-9.2-4.8z" fill="{{c}}"/><path d="M2.8 6.8L12 11.6l9.2-4.8M12 11.6V22" {st(1.5, DK)} stroke-opacity=".5"/>',
 "note":   f'<path d="M9 18.5V5.2l11-2.7v13" {st(2.5)}/><circle cx="6.3" cy="18.6" r="3.2" fill="{{c}}"/><circle cx="17.3" cy="15.9" r="3.2" fill="{{c}}"/>',
 "lock":   f'<path d="M7.3 10V7.2a4.7 4.7 0 0 1 9.4 0V10" {st(2.6)}/><rect x="4" y="10" width="16" height="12" rx="2.2" fill="{{c}}"/><circle cx="12" cy="15.2" r="1.7" fill="{DK}"/><path d="M12 15.5v3" {st(1.7, DK)}/>',
 "palette":f'<path d="M12 2C6.3 2 2 6 2 11.2c0 4.5 3.5 8.3 8.2 8.3h1.4a1.8 1.8 0 0 0 1.3-3.1 1.8 1.8 0 0 1 1.3-3h2.4c3.2 0 5.4-2.5 5.4-5.4C22 4.6 17.5 2 12 2z" fill="{{c}}"/><g fill="{DK}" fill-opacity=".6"><circle cx="7" cy="11" r="1.5"/><circle cx="9.5" cy="6.6" r="1.5"/><circle cx="14.6" cy="6.4" r="1.5"/></g>',
 "cube":   '<path d="M12 2l9 4.9-9 4.9-9-4.9z" fill="{c}"/><path d="M3 6.9l9 4.9V22l-9-4.9z" fill="{c}" fill-opacity=".72"/><path d="M21 6.9l-9 4.9V22l9-4.9z" fill="{c}" fill-opacity=".5"/>',
 "plug":   f'<path d="M8.5 2v5M15.5 2v5M12 17v5" {st(2.5)}/><path d="M5 7h14v3.3a7 7 0 0 1-14 0z" fill="{{c}}"/>',
 "globe":  f'<circle cx="12" cy="12" r="10" fill="{{c}}"/><path d="M2.5 12h19M12 2.3c-3.6 4.4-3.6 15 0 19.4M12 2.3c3.6 4.4 3.6 15 0 19.4" {st(1.4, DK)} stroke-opacity=".5"/>',
 "md":     f'<rect x="1.5" y="5" width="21" height="14" rx="2.2" fill="{{c}}"/><path d="M5 15.5v-7l3 3.3 3-3.3v7M17 8.5v7M14.4 13l2.6 2.6 2.6-2.6" {st(1.8, DK)}/>',
 "book":   '<path d="M2 5.2C4.6 3.8 8 3.8 11 5.8v14.4c-3-2-6.4-2-9-.6zM22 5.2c-2.6-1.4-6-1.4-9 .6v14.4c3-2 6.4-2 9-.6z" fill="{c}"/>',
 "clock":  f'<circle cx="12" cy="12" r="10" fill="{{c}}"/><path d="M12 6.5V12l3.8 2.6" {st(2.1, DK)}/>',
 "ribbon": f'<path d="M7.5 13.5L5 22l4-2 3 2.2 3-2.2 4 2-2.5-8.5" fill="{{c}}" fill-opacity=".75"/><circle cx="12" cy="9" r="7" fill="{{c}}"/><circle cx="12" cy="9" r="3.2" {st(1.6, DK)} stroke-opacity=".55"/>',
 "bot":    f'<rect x="3" y="7.5" width="18" height="13" rx="3.5" fill="{{c}}"/><path d="M12 2.5v5" {st(2.2)}/><circle cx="12" cy="2.6" r="1.6" fill="{{c}}"/><circle cx="8.6" cy="13.8" r="1.7" fill="{DK}"/><circle cx="15.4" cy="13.8" r="1.7" fill="{DK}"/>',
 "yaml":   f'<path d="M3 4.5h11M7 9.5h14M7 14.5h11M3 19.5h15" {st(2.8)}/>',
 "db":     f'<path d="M4 5.2C4 3.4 7.6 2 12 2s8 1.4 8 3.2v13.6c0 1.8-3.6 3.2-8 3.2s-8-1.4-8-3.2z" fill="{{c}}"/><path d="M4 5.2c0 1.8 3.6 3.2 8 3.2s8-1.4 8-3.2M4 12c0 1.8 3.6 3.2 8 3.2s8-1.4 8-3.2" {st(1.4, DK)} stroke-opacity=".45"/>',
 "term":   f'<rect x="2" y="3.5" width="20" height="17" rx="2.5" fill="{{c}}"/><path d="M6.5 9l3.5 3-3.5 3M12.5 16h5" {st(2, DK)}/>',
 "key":    f'<circle cx="7.5" cy="12" r="5" fill="{{c}}"/><path d="M11 10.5h11v3h-2.3v3.3h-3.2v-3.3H11z" fill="{{c}}"/><circle cx="6.8" cy="12" r="1.7" fill="{DK}"/>',
 "hexnodes":f'<path d="M12 2.5l8.2 4.75v9.5L12 21.5l-8.2-4.75v-9.5z" {st(1.6)}/><path d="M12 12L12 2.5M12 12l8.2 4.75M12 12l-8.2 4.75" {st(1.4)}/><g fill="{{c}}"><circle cx="12" cy="12" r="2.6"/><circle cx="12" cy="2.5" r="2"/><circle cx="20.2" cy="16.75" r="2"/><circle cx="3.8" cy="16.75" r="2"/></g>',
 "code":   f'<path d="M8 6l-6 6 6 6M16 6l6 6-6 6" {st(2.8)}/>',
 "image":  f'<rect x="2" y="3.5" width="20" height="17" rx="2.5" fill="{{c}}"/><path d="M4.5 18l5-6.4 3.8 4.4 2.6-3 3.6 5z" fill="{DK}" fill-opacity=".55"/><circle cx="16.3" cy="8.3" r="1.9" fill="{DK}" fill-opacity=".55"/>',
 "nib":    f'<path d="M12 2l5.5 9.5L13.6 22h-3.2L6.5 11.5z" fill="{{c}}"/><circle cx="12" cy="12.6" r="1.6" fill="{DK}"/><path d="M12 2v9" {st(1.2, DK)}/>',
 "zip":    f'<rect x="4" y="2" width="16" height="20" rx="2" fill="{{c}}"/><path d="M12 2v2.5M10.5 4.5h3M12 6.5v2M10.5 8.5h3M12 10.5v2" {st(1.4, DK)} stroke-opacity=".7"/><rect x="10" y="13" width="4" height="5" rx="1" fill="{DK}" fill-opacity=".7"/>',
 "lines":  f'<path d="M4 5h16M4 10h16M4 15h10M4 20h13" {st(2.6)}/>',
 "grid":   f'<rect x="2.5" y="3.5" width="19" height="17" rx="2" fill="{{c}}"/><path d="M2.5 9.2h19M2.5 14.8h19M9 3.5v17M15.5 3.5v17" {st(1.3, DK)} stroke-opacity=".5"/>',
 "font":   '<path fill-rule="evenodd" d="M2.5 21.5L10.2 2.5h3.6l7.7 19h-3.7l-1.8-4.6H8l-1.8 4.6zM9.2 13.8h5.6L12 6.6z" fill="{c}"/>',
 "play":   f'<rect x="2" y="4" width="20" height="16" rx="3" fill="{{c}}"/><path d="M10 8.5v7l5.8-3.5z" fill="{DK}"/>',
 "branch": f'<path d="M6 7.5v9M18 9.6c0 5.4-12 3-12 7.4" {st(2.4)}/><g fill="{{c}}"><circle cx="6" cy="5" r="2.7"/><circle cx="6" cy="19" r="2.7"/><circle cx="18" cy="7" r="2.7"/></g>',
 "stack":  '<g fill="{c}"><rect x="2.5" y="12.5" width="8.5" height="8.5" rx="1.6"/><rect x="13" y="12.5" width="8.5" height="8.5" rx="1.6"/><rect x="7.75" y="3" width="8.5" height="8.5" rx="1.6"/></g>',
 "hook":   f'<path d="M8 3v11.5a5 5 0 0 0 10 0V11" {st(2.8)}/><path d="M15 13.5l3-3 3 3" {st(2.4)}/><circle cx="8" cy="3" r="2" fill="{{c}}"/>',
 "route":  f'<path d="M5 21.5v-7.5a5 5 0 0 1 5-5h9.5" {st(2.8)}/><path d="M15.5 4.8L19.7 9l-4.2 4.2" {st(2.8)}/>',
 "blade":  '<path d="M21.8 2.2l-.4 4L11 16.6 7.4 13 17.8 2.6z" fill="{c}"/><path d="M5.2 12.2l6.6 6.6-1.7 1.7-1.5-1.5-3.3 3.3-1.8-1.8 3.3-3.3-1.5-1.5z" fill="{c}" fill-opacity=".75"/>',
 "twig":   f'<path d="M4 21.5C8 13 13 8.5 20.5 4" {st(2.2)}/><g fill="{{c}}"><path d="M10.8 12.2C7.6 12.4 5.3 10.4 5 7c3.4-.2 5.6 1.8 5.8 5.2z"/><path d="M14.2 8.6c-.2-3.3 1.8-5.6 5.2-5.8.2 3.3-1.8 5.6-5.2 5.8z"/><path d="M14.6 11.3c3.2.3 5.2 2.6 4.9 5.9-3.2-.3-5.2-2.6-4.9-5.9z"/></g>',
 "check":  f'<path d="M3.5 12.5l5.5 5.5L20.5 6.5" {st(3.2)}/>',
 "eye":    f'<path d="M1.5 12C4 6.5 7.8 4 12 4s8 2.5 10.5 8C20 17.5 16.2 20 12 20S4 17.5 1.5 12z" fill="{{c}}"/><circle cx="12" cy="12" r="3.6" fill="{DK}" fill-opacity=".7"/>',
 "wrench": '<path d="M21.3 6.3a5.5 5.5 0 0 1-7.2 6.6l-8.4 8.4a2.1 2.1 0 0 1-3-3l8.4-8.4a5.5 5.5 0 0 1 6.6-7.2l-3.3 3.3.7 2.9 2.9.7z" fill="{c}"/>',
 "mail":   f'<rect x="2" y="4.5" width="20" height="15" rx="2.5" fill="{{c}}"/><path d="M3.5 6.5L12 13l8.5-6.5" {st(1.8, DK)} stroke-opacity=".6"/>',
 "users":  '<circle cx="9" cy="7.5" r="4" fill="{c}"/><path d="M1.5 20.5c0-4.2 3.3-7 7.5-7s7.5 2.8 7.5 7z" fill="{c}"/><circle cx="17.5" cy="8.5" r="3" fill="{c}" fill-opacity=".7"/><path d="M17.3 13.6c3 0 5.2 2.2 5.2 5.8h-4.4" fill="{c}" fill-opacity=".7"/>',
}

SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">{}</svg>\n'

def file_svg(glyph, color):
    return SVG.format(G[glyph].replace("{c}", color))

def tint(hex_, k=0.55):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(v + (255 - v) * k) for v in (r, g, b))

FOLDER = "M2.5 5.5A1.8 1.8 0 0 1 4.3 3.7h5.2l2.2 2.2h8a1.8 1.8 0 0 1 1.8 1.8v10.8a1.8 1.8 0 0 1-1.8 1.8H4.3a1.8 1.8 0 0 1-1.8-1.8z"
OPEN_BACK = "M2.5 5.5A1.8 1.8 0 0 1 4.3 3.7h5.2l2.2 2.2h8a1.8 1.8 0 0 1 1.8 1.8v1.6H6.6a2 2 0 0 0-1.9 1.4L2.5 17.2z"
OPEN_FRONT = "M4.8 11.6a1.6 1.6 0 0 1 1.5-1.1h15.4a1 1 0 0 1 1 1.3l-2.1 7.3a1.8 1.8 0 0 1-1.7 1.3H3.6a1 1 0 0 1-1-1.3z"

def folder_svg(color, glyph=None, open_=False):
    body = (f'<path d="{OPEN_BACK}" fill="{color}"/><path d="{OPEN_FRONT}" fill="{color}" fill-opacity=".85"/>'
            if open_ else f'<path d="{FOLDER}" fill="{color}"/>')
    if glyph:
        body += f'<g transform="translate(10.6 9.6) scale(.46)">{G[glyph].replace("{c}", tint(color))}</g>'
    return SVG.format(body)

# --- file icons: key -> (glyph, colour) ------------------------------------------
F = {
 "default": ("doc", "grey"), "php": ("php", "purple"), "php-entry": ("php", "purple"), "php-hook": ("hook", "orange"),
 "php-config": ("gear", "purple"), "php-route": ("route", "red"), "php-cli": ("term", "purple"), "php-fixer": ("brush", "purple"),
 "blade": ("blade", "red"), "twig": ("twig", "leaf"), "js": ("js", "yellow"), "jsx": ("orbit", "cyan"), "ts": ("ts", "blue"),
 "tsx": ("orbit", "blue"), "dts": ("ts", "indigo"), "js-test": ("flask", "yellow"), "ts-test": ("flask", "blue"),
 "php-test": ("flask", "purple"), "js-config": ("gear", "yellow"), "ts-config": ("gear", "blue"), "js-build": ("bolt", "amber"),
 "ts-build": ("bolt", "amber"), "js-style": ("brush", "cyan"), "ts-style": ("brush", "cyan"), "js-lint": ("shield", "indigo"),
 "js-testcfg": ("flask", "leaf"), "ts-testcfg": ("flask", "leaf"), "css": ("hash", "blue"), "scss": ("hash", "pink"),
 "less": ("hash", "indigo"), "css-theme": ("brush", "pink"), "html": ("angle", "orange"), "vue": ("vee", "leaf"),
 "svelte": ("angle", "red"), "astro": ("sparkle", "orange"), "json": ("braces", "ochre"), "json-pkg": ("box", "red"),
 "json-composer": ("note", "ochre"), "json-lock": ("lock", "ochre"), "json-config": ("gear", "ochre"), "json-ts": ("gear", "blue"),
 "json-theme": ("palette", "pink"), "json-block": ("cube", "yellow"), "json-mcp": ("plug", "purple"), "json-web": ("globe", "leaf"),
 "json-style": ("brush", "pink"), "json-lint": ("shield", "indigo"), "md": ("md", "sky"), "mdx": ("md", "yellow"),
 "md-readme": ("book", "sky"), "md-agent": ("sparkle", "zenith"), "md-changelog": ("clock", "slate"), "txt": ("doc", "grey"),
 "txt-readme": ("book", "sky"), "license": ("ribbon", "amber"), "robots": ("bot", "grey"), "yaml": ("yaml", "red"),
 "yaml-ci": ("bolt", "red"), "yaml-lock": ("lock", "red"), "xml": ("angle", "amber"), "xml-phpunit": ("checkc", "leaf"),
 "xml-rules": ("shield", "red"), "toml": ("gear", "grey"), "ini": ("gear", "grey"), "neon": ("gear", "leaf"),
 "neon-stan": ("shieldq", "leaf"), "sql": ("db", "teal"), "prisma": ("db", "indigo"), "sqlite": ("db", "sky"),
 "sh": ("term", "leaf"), "make": ("term", "grey"), "env": ("key", "yellow"), "http": ("globe", "leaf"), "gql": ("hexnodes", "pink"),
 "py": ("code", "blue"), "rs": ("code", "orange"), "go": ("code", "cyan"), "rb": ("code", "red"), "java": ("code", "orange"),
 "kt": ("code", "purple"), "swift": ("code", "orange"), "c": ("code", "blue"), "h": ("code", "purple"), "cpp": ("code", "blue"),
 "cs": ("code", "purple"), "lua": ("code", "indigo"), "dart": ("code", "sky"), "wasm": ("code", "indigo"),
 "image": ("image", "teal"), "svg": ("nib", "amber"), "icon": ("image", "yellow"), "pdf": ("docfold", "red"),
 "archive": ("zip", "brown"), "log": ("lines", "grey"), "csv": ("grid", "leaf"), "font": ("font", "purple"),
 "video": ("play", "pink"), "audio": ("note", "pink"), "i18n": ("globe", "blue"), "map": ("code", "grey"),
 "lock": ("lock", "grey"), "diff": ("branch", "orange"), "git": ("branch", "orange"), "docker": ("stack", "blue"),
 "editorconfig": ("gear", "grey"), "htaccess": ("gear", "grey"), "nvm": ("gear", "leaf"), "npmrc": ("box", "red"),
}

SUFFIX = {
 "php": "php", "phtml": "php", "inc": "php", "blade.php": "blade", "twig": "twig",
 "js": "js", "mjs": "js", "cjs": "js", "jsx": "jsx", "ts": "ts", "mts": "ts", "cts": "ts", "tsx": "tsx", "d.ts": "dts",
 "css": "css", "scss": "scss", "sass": "scss", "less": "less", "html": "html", "htm": "html",
 "vue": "vue", "svelte": "svelte", "astro": "astro",
 "json": "json", "jsonc": "json", "json5": "json", "md": "md", "markdown": "md", "mdx": "mdx", "txt": "txt",
 "yml": "yaml", "yaml": "yaml", "xml": "xml", "xml.dist": "xml", "toml": "toml", "ini": "ini", "conf": "ini", "cfg": "ini",
 "neon": "neon", "neon.dist": "neon", "sql": "sql", "prisma": "prisma", "sqlite": "sqlite", "db": "sqlite",
 "sh": "sh", "bash": "sh", "zsh": "sh", "fish": "sh", "http": "http", "rest": "http", "graphql": "gql", "gql": "gql",
 "py": "py", "rs": "rs", "go": "go", "rb": "rb", "java": "java", "kt": "kt", "swift": "swift", "c": "c", "h": "h",
 "cpp": "cpp", "cc": "cpp", "hpp": "cpp", "cs": "cs", "lua": "lua", "dart": "dart", "wasm": "wasm",
 "svg": "svg", "ico": "icon", "pdf": "pdf", "log": "log", "csv": "csv", "tsv": "csv", "map": "map",
 "lock": "lock", "patch": "diff", "diff": "diff", "po": "i18n", "pot": "i18n", "mo": "i18n",
}
for e in "png jpg jpeg gif webp avif bmp tiff heic".split(): SUFFIX[e] = "image"
for e in "zip gz tgz tar rar 7z bz2 xz".split(): SUFFIX[e] = "archive"
for e in "woff woff2 ttf otf eot".split(): SUFFIX[e] = "font"
for e in "mp4 mov webm mkv avi".split(): SUFFIX[e] = "video"
for e in "mp3 wav ogg flac m4a".split(): SUFFIX[e] = "audio"
for lang, key in (("js", "js-test"), ("jsx", "js-test"), ("mjs", "js-test"), ("ts", "ts-test"), ("tsx", "ts-test")):
    for kind in ("test", "spec", "e2e"):
        SUFFIX[f"{kind}.{lang}"] = key
for kind, key in (("js", "js-config"), ("mjs", "js-config"), ("cjs", "js-config"), ("ts", "ts-config"), ("mts", "ts-config")):
    SUFFIX[f"config.{kind}"] = key

STEM = {
 "composer.json": "json-composer", "composer.lock": "json-lock", "package.json": "json-pkg",
 "package-lock.json": "json-lock", "yarn.lock": "lock", "pnpm-lock.yaml": "yaml-lock", "bun.lockb": "lock", "bun.lock": "lock",
 "tsconfig.json": "json-ts", "jsconfig.json": "json-ts", "theme.json": "json-theme", "block.json": "json-block",
 ".mcp.json": "json-mcp", "manifest.json": "json-web", "pint.json": "json-style", ".prettierrc": "json-style",
 ".prettierrc.json": "json-style", ".eslintrc": "json-lint", ".eslintrc.json": "json-lint", ".stylelintrc.json": "json-lint",
 "phpunit.xml": "xml-phpunit", "phpunit.xml.dist": "xml-phpunit", "phpcs.xml": "xml-rules", "phpcs.xml.dist": "xml-rules",
 ".phpcs.xml.dist": "xml-rules", "psalm.xml": "xml-rules", "phpstan.neon": "neon-stan", "phpstan.neon.dist": "neon-stan",
 ".php-cs-fixer.php": "php-fixer", ".php-cs-fixer.dist.php": "php-fixer", "rector.php": "php-fixer",
 "functions.php": "php-hook", "wp-config.php": "php-config", "wp-config-sample.php": "php-config",
 "index.php": "php-entry", "artisan": "php-cli", "web.php": "php-route", "api.php": "php-route",
 "console.php": "php-route", "channels.php": "php-route", "style.css": "css-theme",
 "vite.config.js": "js-build", "vite.config.ts": "ts-build", "webpack.config.js": "js-build", "rollup.config.js": "js-build",
 "next.config.js": "js-build", "next.config.mjs": "js-build", "next.config.ts": "ts-build",
 "tailwind.config.js": "js-style", "tailwind.config.ts": "ts-style", "postcss.config.js": "js-style",
 "prettier.config.js": "js-style", "eslint.config.js": "js-lint", "eslint.config.mjs": "js-lint",
 "jest.config.js": "js-testcfg", "vitest.config.ts": "ts-testcfg", "playwright.config.ts": "ts-testcfg",
 "README.md": "md-readme", "readme.md": "md-readme", "README": "txt-readme", "readme.txt": "txt-readme",
 "CHANGELOG.md": "md-changelog", "CLAUDE.md": "md-agent", "AGENTS.md": "md-agent", "GEMINI.md": "md-agent",
 "LICENSE": "license", "LICENSE.md": "license", "LICENSE.txt": "license", "license.txt": "license", "robots.txt": "robots",
 ".env": "env", ".env.example": "env", ".env.local": "env", ".env.testing": "env", ".env.production": "env",
 ".gitignore": "git", ".gitattributes": "git", ".gitmodules": "git", ".gitkeep": "git",
 "Dockerfile": "docker", "docker-compose.yml": "docker", "docker-compose.yaml": "docker", "compose.yaml": "docker",
 "compose.yml": "docker", ".dockerignore": "docker", "Makefile": "make", ".editorconfig": "editorconfig",
 ".htaccess": "htaccess", ".nvmrc": "nvm", ".node-version": "nvm", ".npmrc": "npmrc",
 "dependabot.yml": "yaml-ci", ".gitlab-ci.yml": "yaml-ci", "favicon.ico": "icon",
}

# --- folders: names -> (colour, emblem glyph) -------------------------------------
D = {}
def d(names, color, glyph):
    for n in names.split():
        D[n] = (C[color], glyph)
d("src source", "blue", "code"); d("app", "purple", "sparkle"); d("core kernel", "purple", "cube")
d("includes inc", "purple", "code"); d("lib libs", "slate", "box")
d("tests test __tests__ spec specs e2e", "leaf", "check"); d("fixtures mocks __mocks__ stubs", "leaf", "flask")
d("build dist out release", "orange", "box"); d("public static www", "teal", "globe")
d("assets resources", "amber", "image"); d("images img icons media uploads", "teal", "image")
d("styles css scss sass", "pink", "hash"); d("js scripts bin", "yellow", "term")
d("components blocks block patterns parts", "yellow", "cube"); d("hooks webhooks", "orange", "hook")
d("config configs settings", "slate", "gear"); d("routes router", "red", "route")
d("database migrations seeders factories db", "teal", "db"); d("models entities", "indigo", "cube")
d("views templates template-parts layouts pages", "red", "eye"); d("lang languages i18n locales", "blue", "globe")
d("docs doc documentation plan plans", "sky", "book"); d("vendor node_modules", "slate", "box")
d(".git", "orange", "branch"); d(".github .gitlab", "slate", "branch"); d(".claude .zenith .cursor", "zenith", "sparkle")
d("admin dashboard", "red", "shield"); d("api http", "leaf", "globe"); d("storage", "slate", "db")
d("cache tmp temp", "slate", "clock"); d("logs", "slate", "lines"); d("bootstrap", "orange", "bolt")
d("types @types typings interfaces", "blue", "ts"); d("utils helpers support", "slate", "wrench")
d("middleware guards policies auth security", "indigo", "shield"); d("providers plugins mu-plugins extensions", "purple", "plug")
d("services actions jobs queue", "purple", "bolt"); d("controllers handlers", "blue", "route")
d("console commands cli", "leaf", "term"); d("events listeners", "orange", "bolt"); d("cron schedule", "slate", "clock")
d("mail mails emails notifications", "blue", "mail"); d("fonts", "purple", "font"); d("themes theme", "pink", "palette")
d("wp-content wp-includes", "purple", "plug"); d("users accounts", "blue", "users")
d("scratches", "sky", "lines"); d(".vscode .idea .zed", "slate", "gear"); d("docker .docker", "blue", "stack")

def write(rel, svg):
    p = EXT / "icons" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg)
    return "./icons/" + rel

def main():
    bad = sorted({k for k in list(STEM.values()) + list(SUFFIX.values()) if k not in F})
    assert not bad, f"unmapped icon keys: {bad}"
    file_icons = {k: {"path": write(f"files/{k}.svg", file_svg(g, C[c]))} for k, (g, c) in F.items()}
    named, slugs = {}, {}
    for name, (color, g) in D.items():
        slug = name.strip("._@") or name
        named[name] = {"collapsed": write(f"folders/{slug}.svg", folder_svg(color, g)),
                       "expanded": write(f"folders/{slug}-open.svg", folder_svg(color, g, True))}
    theme = {"$schema": "https://zed.dev/schema/icon_themes/v0.3.0.json", "name": "Zenith Icons",
             "author": "Zenith contributors",
             "themes": [{"name": "Zenith Icons", "appearance": "dark",
                         "directory_icons": {"collapsed": write("folders/folder.svg", folder_svg(C["grey"])),
                                             "expanded": write("folders/folder-open.svg", folder_svg(C["grey"], None, True))},
                         "named_directory_icons": named, "file_stems": STEM, "file_suffixes": SUFFIX,
                         "file_icons": file_icons}]}
    (EXT / "icon_themes").mkdir(parents=True, exist_ok=True)
    (EXT / "icon_themes/zenith-icons.json").write_text(json.dumps(theme, indent=2) + "\n")
    (EXT / "extension.toml").write_text(
        'id = "zenith-icons"\nname = "Zenith Icons"\nversion = "0.1.0"\nschema_version = 1\n'
        'description = "Original file and folder icons for Zenith, in the Atom Material style."\n'
        'authors = ["Zenith contributors"]\nrepository = "https://github.com/wp-sigmadevs/zenith"\n')
    sheet(theme["themes"][0])
    print(f"{len(F)} file icons, {len(set(D.values()))} folder designs for {len(D)} folder names, "
          f"{len(STEM)} file names, {len(SUFFIX)} extensions")

def sheet(t):
    uri = lambda p: "data:image/svg+xml;base64," + base64.b64encode((EXT / p).read_bytes()).decode()
    users = {}
    for k, v in list(t["file_stems"].items()) + [("." + k, v) for k, v in t["file_suffixes"].items()]:
        users.setdefault(v, []).append(k)
    cell = lambda src, a, b: (f'<figure><span class="pair"><img src="{src}" width="16" height="16" alt="">'
                              f'<img src="{src}" width="32" height="32" alt=""></span>'
                              f'<figcaption><b>{html.escape(a)}</b><span>{html.escape(b)}</span></figcaption></figure>')
    files = "".join(cell(uri(v["path"]), k, ", ".join(users.get(k, ["fallback"])[:4])) for k, v in t["file_icons"].items())
    groups = {}
    for n, (color, g) in D.items():
        groups.setdefault((color, g), []).append(n)
    folders = cell(uri(t["directory_icons"]["collapsed"]), "folder", "any other name")
    for ns in groups.values():
        v = t["named_directory_icons"][ns[0]]
        folders += cell(uri(v["collapsed"]), ns[0], ", ".join(ns[1:5]) or "—")
    tree_rows = [(0, "dir", "lumen-gallery", 1), (1, "includes", "includes", 1), (2, "core", "Core", 1),
                 (3, "f:php", "Assets.php", 0), (3, "f:php", "Rest.php", 0), (2, "admin", "Admin", 0),
                 (1, "src", "src", 0), (1, "build", "build", 0), (1, "tests", "tests", 1), (2, "f:php", "AssetsTest.php", 0),
                 (1, "f:json-composer", "composer.json", 0), (1, "f:json-pkg", "package.json", 0),
                 (1, "f:xml-rules", "phpcs.xml.dist", 0), (1, "f:xml-phpunit", "phpunit.xml.dist", 0),
                 (1, "f:env", ".env", 0), (1, "f:md-agent", "CLAUDE.md", 0), (1, "f:txt-readme", "readme.txt", 0)]
    tree = ""
    for depth, key, name, open_ in tree_rows:
        if key.startswith("f:"):
            src = uri(t["file_icons"][key[2:]]["path"])
        elif key == "dir":
            src = uri(t["directory_icons"]["expanded"])
        else:
            src = uri(t["named_directory_icons"][key]["expanded" if open_ else "collapsed"])
        tree += f'<div class="tr" style="padding-left:{12 + depth * 16}px"><img src="{src}" width="16" height="16" alt="">{html.escape(name)}</div>'
    stats = (f'{len(F)} file icons · {len(groups)} folder designs ({len(D)} folder names) · '
             f'{len(t["file_stems"])} file names · {len(t["file_suffixes"])} extensions')
    SHEET.write_text(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Zenith Icons</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap">
<style>
/* Layout: a project tree preview beside the rules, then the full sheet. Single dark look = the Driftwood panel. */
:root{{--bg:#2b2d30;--card:#1e1f22;--line:#393b40;--fg:#dfe1e5;--dim:#8c8f96;--acc:#71a1fe;--sel:#2a4371;
  --ui:"Inter",-apple-system,system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font:14px/1.5 var(--ui);margin:0;padding-block:32px;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:1180px;margin:0 auto;display:grid;gap:28px}}
h1{{font-size:26px;margin:0}} h2{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 12px}}
p{{margin:6px 0 0;color:var(--dim);max-width:68ch}}
.stats{{font:12px var(--mono);color:var(--acc);margin-top:10px}}
.top{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:20px;align-items:start}}
.tree{{background:var(--card);border-radius:10px;padding:8px 0;font-size:13px}}
.tr{{display:flex;align-items:center;gap:7px;height:24px}} .tr:nth-child(4){{background:var(--sel)}}
.rules{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}
.rules div{{background:var(--card);border-radius:8px;padding:10px 12px;font-size:13px;color:var(--dim)}}
.rules b{{display:block;color:var(--fg);font-weight:500}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:4px}}
figure{{margin:0;display:flex;gap:10px;align-items:center;padding:7px;border-radius:6px;min-width:0}}
figure:hover{{background:rgba(255,255,255,.06)}}
.pair{{display:flex;gap:8px;align-items:center;flex:none}}
figcaption{{min-width:0;display:flex;flex-direction:column}}
figcaption b{{font:500 12px var(--mono);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
figcaption span{{font-size:11px;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
@media (max-width:640px){{.top{{grid-template-columns:minmax(0,1fr)}}}}
</style>
</head>
<body>
<main>
<header><h1>Zenith Icons</h1>
<p>Original file and folder icons in the Atom Material style: one solid glyph per file type, saturated folders with a lighter emblem. No third-party artwork or brand logos.</p>
<div class="stats">{stats}</div></header>
<section class="top"><div class="tree" aria-label="Project tree preview">{tree}</div>
<div class="rules">
<div><b>Glyph, not page</b>Each file type is a single solid symbol at full size, like Atom Material, so the type reads before the name.</div>
<div><b>Context first</b>composer.json is a note, package.json a box, phpunit.xml a check, phpcs.xml a shield, functions.php a hook, CLAUDE.md the agent sparkle.</div>
<div><b>Folders by role</b>Solid folder in the role colour with a lighter emblem bottom-right: tests check, src code, config gear, views eye.</div>
<div><b>One generator</b>brand/icons/generate.py draws every SVG and writes the Zed icon theme, so the set stays consistent.</div>
</div></section>
<section><h2>Files</h2><div class="grid">{files}</div></section>
<section><h2>Folders</h2><div class="grid">{folders}</div></section>
</main>
</body>
</html>
''')

if __name__ == "__main__":
    main()

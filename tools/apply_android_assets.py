#!/usr/bin/env python3
"""Aplica el logo de PewTify al proyecto Android generado por Capacitor.

Se ejecuta DESPUES de `npx cap add android` y genera:
  - iconos del launcher (clasico, redondo y adaptable) a partir de resources/
  - pantalla de carga (splash) con el logo PewTify sobre fondo oscuro
  - color de fondo del icono adaptable y de la splash de Android 12+
"""
import os, re, sys
from PIL import Image, ImageDraw

BG = (10, 11, 20)            # #0a0b14  fondo oscuro del icono
BG_HEX = "#0a0b14"
RING = (63, 63, 143)         # borde morado oscuro del icono original

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "android", "app", "src", "main", "res")
SRC = os.path.join(ROOT, "resources")

if not os.path.isdir(RES):
    sys.exit("No existe %s. Ejecuta primero: npx cap add android" % RES)

icon_full = Image.open(os.path.join(SRC, "icon_full.png")).convert("RGBA")
glyph = Image.open(os.path.join(SRC, "icon_glyph.png")).convert("RGBA")
wordmark = Image.open(os.path.join(SRC, "logo.png")).convert("RGBA")

DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}


def fit(img, box_w, box_h):
    s = min(box_w / img.width, box_h / img.height)
    return img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS)


def centered(canvas, img):
    canvas.alpha_composite(img, ((canvas.width - img.width) // 2, (canvas.height - img.height) // 2))


def round_icon(size):
    big = size * 4
    c = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.ellipse((0, 0, big - 1, big - 1), fill=RING + (255,))
    inset = round(big * 0.035)
    d.ellipse((inset, inset, big - 1 - inset, big - 1 - inset), fill=BG + (255,))
    centered(c, fit(glyph, big * 0.46, big * 0.46))
    return c.resize((size, size), Image.LANCZOS)


for name, k in DENS.items():
    d = os.path.join(RES, "mipmap-" + name)
    os.makedirs(d, exist_ok=True)
    legacy, adaptive = round(48 * k), round(108 * k)
    icon_full.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(d, "ic_launcher.png"))
    round_icon(legacy).save(os.path.join(d, "ic_launcher_round.png"))
    fg = Image.new("RGBA", (adaptive, adaptive), (0, 0, 0, 0))
    centered(fg, fit(glyph, adaptive * 0.40, adaptive * 0.40))   # dentro de la zona segura (66dp de 108dp)
    fg.save(os.path.join(d, "ic_launcher_foreground.png"))

# color de fondo del icono adaptable
with open(os.path.join(RES, "values", "ic_launcher_background.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">%s</color>\n</resources>\n' % BG_HEX)

# splash: se regenera cada splash.png con su mismo tamano
n = 0
for dp, _, files in os.walk(RES):
    for fn in files:
        if fn == "splash.png":
            p = os.path.join(dp, fn)
            w, h = Image.open(p).size
            c = Image.new("RGBA", (w, h), BG + (255,))
            centered(c, fit(wordmark, min(w, h) * 0.42, min(w, h) * 0.42 * wordmark.height / wordmark.width))
            c.convert("RGB").save(p)
            n += 1
print("splash regeneradas:", n)

# Android 12+: fondo oscuro en la pantalla de inicio del sistema
sp = os.path.join(RES, "values", "styles.xml")
s = open(sp, encoding="utf-8").read()
if "windowSplashScreenBackground" not in s:
    s = s.replace('<item name="android:background">@drawable/splash</item>',
                  '<item name="android:background">@drawable/splash</item>\n        <item name="windowSplashScreenBackground">@color/ic_launcher_background</item>')
    open(sp, "w", encoding="utf-8").write(s)
print("Listo: iconos y splash de PewTify aplicados.")

# PewTify (APK)

La app web esta en `www/index.html`. GitHub la convierte en APK con Capacitor.

## Como obtener el APK
1. Sube **todo el contenido** de esta carpeta a un repositorio de GitHub (incluida la carpeta oculta `.github`).
2. Ve a la pestana **Actions** → **Build PewTify APK** (corre solo al subir; o usa **Run workflow**).
3. Cuando termine (unos 5-8 min), abre la ejecucion y descarga **PewTify-APK** en *Artifacts*.
4. Descomprime el zip: dentro esta `app-debug.apk`. Instalalo en tu Android (permite "instalar apps desconocidas").

## Logos
- `resources/logo.png` → logo con texto (barra lateral y pantalla de carga)
- `resources/icon_full.png` / `icon_glyph.png` → icono del launcher
- `tools/apply_android_assets.py` genera todos los tamanos de Android al compilar.

#!/usr/bin/env python3
"""
Genera el logo oficial de Noutrora (Timón de barco) en formato SVG y PNGs multi-resolución.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "config" / "branding"

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b192c"/>
      <stop offset="100%" stop-color="#1e3e62"/>
    </linearGradient>
    <linearGradient id="wheelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f5c45e"/>
      <stop offset="50%" stop-color="#e78b48"/>
      <stop offset="100%" stop-color="#be5b50"/>
    </linearGradient>
    <linearGradient id="hubGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff3d1"/>
      <stop offset="100%" stop-color="#f5c45e"/>
    </linearGradient>
  </defs>

  <!-- Fondo circular marino profundo -->
  <circle cx="256" cy="256" r="240" fill="url(#bgGrad)" stroke="#f5c45e" stroke-width="10"/>
  <circle cx="256" cy="256" r="222" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="3"/>

  <!-- 8 Radios y cabillas (manijas) del timón -->
  <g stroke="url(#wheelGrad)" stroke-linecap="round">
    <line x1="256" y1="36" x2="256" y2="476" stroke-width="22"/>
    <line x1="36" y1="256" x2="476" y2="256" stroke-width="22"/>
    <line x1="100.4" y1="100.4" x2="411.6" y2="411.6" stroke-width="22"/>
    <line x1="411.6" y1="100.4" x2="100.4" y2="411.6" stroke-width="22"/>
  </g>

  <!-- Puntas redondeadas de las 8 cabillas exteriores -->
  <g fill="url(#hubGrad)">
    <circle cx="256" cy="34" r="15"/>
    <circle cx="256" cy="478" r="15"/>
    <circle cx="34" cy="256" r="15"/>
    <circle cx="478" cy="256" r="15"/>
    <circle cx="99" cy="99" r="15"/>
    <circle cx="413" cy="413" r="15"/>
    <circle cx="413" cy="99" r="15"/>
    <circle cx="99" cy="413" r="15"/>
  </g>

  <!-- Aro principal del timón -->
  <circle cx="256" cy="256" r="152" fill="none" stroke="#0b192c" stroke-width="42"/>
  <circle cx="256" cy="256" r="152" fill="none" stroke="url(#wheelGrad)" stroke-width="32"/>
  <circle cx="256" cy="256" r="152" fill="none" stroke="#fff3d1" stroke-opacity="0.45" stroke-width="4"/>

  <!-- Aro interior de refuerzo -->
  <circle cx="256" cy="256" r="88" fill="none" stroke="url(#hubGrad)" stroke-width="10"/>

  <!-- Núcleo / Eje central del timón -->
  <circle cx="256" cy="256" r="46" fill="#0b192c" stroke="url(#wheelGrad)" stroke-width="14"/>
  <circle cx="256" cy="256" r="18" fill="url(#hubGrad)"/>
</svg>
"""


def render_helm_png(size: int = 1024) -> Image.Image:
    """Renderiza el timón de barco en alta resolución con Pillow."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2

    # Colores náuticos: Azul océano profundo y dorado/bronce
    navy_dark = (11, 25, 44, 255)
    navy_mid = (24, 52, 86, 255)
    gold_main = (245, 196, 94, 255)
    gold_warm = (231, 139, 72, 255)
    gold_light = (255, 243, 209, 255)

    # 1. Círculo de fondo marino con borde dorado
    bg_r = int(size * 0.468)
    draw.ellipse((cx - bg_r, cy - bg_r, cx + bg_r, cy + bg_r), fill=navy_dark, outline=gold_main, width=int(size * 0.02))
    inner_bg_r = int(size * 0.43)
    draw.ellipse((cx - inner_bg_r, cy - inner_bg_r, cx + inner_bg_r, cy + inner_bg_r), fill=navy_mid)

    # 2. 8 Radios y cabillas exteriores del timón
    spoke_len = int(size * 0.43)
    spoke_w = int(size * 0.045)
    knob_r = int(size * 0.032)

    for i in range(8):
        angle = i * (math.pi / 4)
        x_end = cx + int(math.cos(angle) * spoke_len)
        y_end = cy + int(math.sin(angle) * spoke_len)
        draw.line((cx, cy, x_end, y_end), fill=gold_warm, width=spoke_w)
        # Cabilla / pomo exterior
        draw.ellipse((x_end - knob_r, y_end - knob_r, x_end + knob_r, y_end + knob_r), fill=gold_light, outline=gold_warm, width=int(size * 0.008))

    # 3. Aro principal del timón
    ring_r = int(size * 0.295)
    ring_outer_w = int(size * 0.082)
    ring_inner_w = int(size * 0.062)
    draw.ellipse(
        (cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r),
        outline=navy_dark,
        width=ring_outer_w,
    )
    draw.ellipse(
        (cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r),
        outline=gold_main,
        width=ring_inner_w,
    )

    # 8 remaches en el aro principal
    rivet_r = int(size * 0.012)
    for i in range(8):
        angle = i * (math.pi / 4)
        rx = cx + int(math.cos(angle) * (ring_r - ring_inner_w * 0.45))
        ry = cy + int(math.sin(angle) * (ring_r - ring_inner_w * 0.45))
        draw.ellipse((rx - rivet_r, ry - rivet_r, rx + rivet_r, ry + rivet_r), fill=gold_light)

    # 4. Aro secundario interior
    inner_ring_r = int(size * 0.17)
    draw.ellipse(
        (cx - inner_ring_r, cy - inner_ring_r, cx + inner_ring_r, cy + inner_ring_r),
        outline=gold_light,
        width=int(size * 0.02),
    )

    # 5. Eje central (Hub)
    hub_r = int(size * 0.095)
    draw.ellipse(
        (cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r),
        fill=navy_dark,
        outline=gold_warm,
        width=int(size * 0.028),
    )
    center_r = int(size * 0.036)
    draw.ellipse(
        (cx - center_r, cy - center_r, cx + center_r, cy + center_r),
        fill=gold_light,
    )

    return img


def main():
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = BRAND_DIR / "noutrora.svg"
    svg_path.write_text(SVG_CONTENT, encoding="utf-8")

    master = render_helm_png(1024)
    resample_filter = getattr(Image, "Resampling", Image).LANCZOS
    master.resize((512, 512), resample_filter).save(BRAND_DIR / "noutrora-512.png")

    for s in (128, 64, 48, 32, 16):
        resized = master.resize((s, s), resample_filter)
        resized.save(BRAND_DIR / f"default{s}.png")

    print("✅ Logo de timón de Noutrora generado en config/branding/")


if __name__ == "__main__":
    main()

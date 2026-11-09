#!/usr/bin/env python3
"""
Genera todos los activos gráficos oficiales de Noutrora sincronizados 100% con
noutrora_landing_page_oficial.html y el Manual de Identidad de Marca v2.0:
1. Isotipo principal: La brújula de la segunda «o» con aguja romboidal bicolor (noutrora.svg + PNGs 16..512px).
2. Logotipo completo: «Noutrora» con síntesis náutica en la segunda «o» (noutrora-wordmark.svg y dark).
3. Colección de 8 iconos vectoriales UI en retícula 24x24 px (config/branding/icons/*.svg).
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "config" / "branding"
ICONS_DIR = BRAND_DIR / "icons"

# Paleta Cromática Oficial — Océano Atlántico y Calma Visual
HEX_ABISMO = "#1B3644"      # (27, 54, 68)   Logotipo principal, tipografía titular, aguja Norte
HEX_BRUMA = "#7A9E9F"       # (122, 158, 159) Acentos de la segunda «o», pestaña activa, foco URL
HEX_ARENA = "#D6D3C9"       # (214, 211, 201) Bordes divisorios sutiles, iconos inactivos
HEX_ESPUMA = "#FAF9F5"      # (250, 249, 245) Fondo principal y Nueva Pestaña
HEX_HORIZONTE94 = "#0F232E" # (15, 35, 46)    Homenaje Netscape '94 / Modo Calma

# 1. ISOTIPO PRINCIPAL — Modo Calma (Fondo Abismo Atlántico #1B3644 + Aguja romboidal bicolor)
ISOTIPO_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none">
  <circle cx="12" cy="12" r="11.2" fill="{HEX_ABISMO}" stroke="{HEX_BRUMA}" stroke-opacity="0.45" stroke-width="0.6"/>
  <circle cx="12" cy="12.4" r="7.5" stroke="{HEX_ESPUMA}" stroke-width="1.65"/>
  <line x1="12" y1="2.8" x2="12" y2="6.1" stroke="{HEX_ESPUMA}" stroke-width="1.65" stroke-linecap="round"/>
  <line x1="12" y1="18.6" x2="12" y2="20.6" stroke="{HEX_BRUMA}" stroke-width="1.35" stroke-linecap="round"/>
  <line x1="3.6" y1="12.4" x2="5.6" y2="12.4" stroke="{HEX_BRUMA}" stroke-width="1.35" stroke-linecap="round"/>
  <line x1="18.4" y1="12.4" x2="20.4" y2="12.4" stroke="{HEX_BRUMA}" stroke-width="1.35" stroke-linecap="round"/>
  <polygon points="12,6.8 13.8,12.4 12,11.1 10.2,12.4" fill="{HEX_ESPUMA}" transform="rotate(24 12 12.4)"/>
  <polygon points="12,18.0 13.6,12.4 12,13.7 10.4,12.4" fill="{HEX_BRUMA}" transform="rotate(24 12 12.4)"/>
  <circle cx="12" cy="12.4" r="1.05" fill="{HEX_ABISMO}" stroke="{HEX_ESPUMA}" stroke-width="0.8"/>
</svg>
"""


def build_wordmark_svg(fg_color: str, accent_color: str, center_fill: str) -> str:
    """
    Construye el logotipo vectorial 'Noutrora' exactamente con las coordenadas de
    noutrora_landing_page_oficial.html (#noutrora-wordmark, viewBox 0 0 585 130).
    """
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 585 130" width="585" height="130" fill="none">
  <!-- N -->
  <path d="M 20 112 L 20 34 L 71 112 L 71 34" fill="none" stroke="{fg_color}" stroke-width="6.2" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- 1.ª o (Completamente limpia y humanista) -->
  <circle cx="127" cy="83" r="29" fill="none" stroke="{fg_color}" stroke-width="6"/>
  <!-- u -->
  <path d="M 183 54 L 183 88 A 24 24 0 0 0 231 88" fill="none" stroke="{fg_color}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="231" y1="54" x2="231" y2="112" stroke="{fg_color}" stroke-width="6" stroke-linecap="round"/>
  <!-- t -->
  <path d="M 271 36 L 271 99 A 13 13 0 0 0 284 112 L 293 112 M 257 56 L 289 56" fill="none" stroke="{fg_color}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- 1.ª r -->
  <path d="M 319 112 L 319 56 M 319 76 A 24 24 0 0 1 343 54 L 349 54" fill="none" stroke="{fg_color}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- 2.ª O: NÚCLEO NÁUTICO (Brújula / Eje Norte / Aguja romboidal a 24°) -->
  <g>
    <circle cx="403" cy="83" r="29" fill="none" stroke="{fg_color}" stroke-width="6"/>
    <line x1="403" y1="42" x2="403" y2="59" stroke="{fg_color}" stroke-width="5.2" stroke-linecap="round"/>
    <line x1="403" y1="105" x2="403" y2="117" stroke="{accent_color}" stroke-width="4" stroke-linecap="round"/>
    <line x1="368" y1="83" x2="380" y2="83" stroke="{accent_color}" stroke-width="4" stroke-linecap="round"/>
    <line x1="426" y1="83" x2="438" y2="83" stroke="{accent_color}" stroke-width="4" stroke-linecap="round"/>
    <polygon points="403,60 409.5,83 403,78 396.5,83" fill="{fg_color}" transform="rotate(24 403 83)"/>
    <polygon points="403,106 408.5,83 403,87 397.5,83" fill="{accent_color}" transform="rotate(24 403 83)"/>
    <circle cx="403" cy="83" r="2.8" fill="{center_fill}" stroke="{fg_color}" stroke-width="2.2"/>
  </g>
  <!-- 2.ª r -->
  <path d="M 465 112 L 465 56 M 465 76 A 24 24 0 0 1 489 54 L 495 54" fill="none" stroke="{fg_color}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- a -->
  <circle cx="537" cy="83" r="28" fill="none" stroke="{fg_color}" stroke-width="6"/>
  <path d="M 565 54 L 565 112" fill="none" stroke="{fg_color}" stroke-width="6" stroke-linecap="round"/>
</svg>
"""


# 3. COLECCIÓN OFICIAL DE 8 ICONOS VECTORIALES (Idénticos a noutrora_landing_page_oficial.html)
UI_ICONS = {
    # 1. Puerto Base (Home)
    "noutrora-home.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <circle cx="12" cy="12.5" r="8.5" stroke="{HEX_ABISMO}" stroke-width="1.8"/>
  <line x1="12" y1="1.8" x2="12" y2="5.5" stroke="{HEX_ABISMO}" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="12" y1="19.5" x2="12" y2="22" stroke="{HEX_BRUMA}" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="2.5" y1="12.5" x2="5" y2="12.5" stroke="{HEX_BRUMA}" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="19" y1="12.5" x2="21.5" y2="12.5" stroke="{HEX_BRUMA}" stroke-width="1.5" stroke-linecap="round"/>
  <polygon points="12,6.2 14,12.5 12,11 10,12.5" fill="{HEX_ABISMO}" transform="rotate(24 12 12.5)"/>
  <polygon points="12,18.8 13.8,12.5 12,14 10.2,12.5" fill="{HEX_BRUMA}" transform="rotate(24 12 12.5)"/>
</svg>
""",
    # 2. Marea (Recargar)
    "noutrora-reload.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <path d="M 3 9.5 C 6.5 6, 9.5 6, 12 9.5 C 14.5 13, 17.5 13, 21 9.5" stroke="{HEX_ABISMO}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M 3 15.5 C 6.5 12, 9.5 12, 12 15.5 C 14.5 19, 17.5 19, 21 15.5" stroke="{HEX_BRUMA}" stroke-width="1.8" stroke-linecap="round"/>
  <polyline points="18,6 21.5,9.5 17.5,12" stroke="{HEX_ABISMO}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
""",
    # 3. Estrella Polar (Bitácora / Marcadores)
    "noutrora-bookmark.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <path d="M 12 2.5 L 14.4 9.6 L 21.5 12 L 14.4 14.4 L 12 21.5 L 9.6 14.4 L 2.5 12 L 9.6 9.6 Z" stroke="{HEX_ABISMO}" stroke-width="1.75" stroke-linejoin="round"/>
  <circle cx="18.5" cy="5.5" r="1.2" fill="{HEX_BRUMA}"/>
</svg>
""",
    # 4. Fondear (Descargas)
    "noutrora-anchor.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <circle cx="12" cy="5" r="2.2" stroke="{HEX_ABISMO}" stroke-width="1.75"/>
  <line x1="12" y1="7.2" x2="12" y2="21" stroke="{HEX_ABISMO}" stroke-width="1.75" stroke-linecap="round"/>
  <line x1="7.5" y1="11" x2="16.5" y2="11" stroke="{HEX_BRUMA}" stroke-width="1.75" stroke-linecap="round"/>
  <path d="M 5 15.5 A 7.5 7.5 0 0 0 19 15.5" stroke="{HEX_ABISMO}" stroke-width="1.75" stroke-linecap="round"/>
</svg>
""",
    # 5. Horizonte (Modo Calma / Lectura)
    "noutrora-zen.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <line x1="2.5" y1="14.5" x2="21.5" y2="14.5" stroke="{HEX_ABISMO}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M 6.5 14.5 A 5.5 5.5 0 0 1 17.5 14.5" stroke="{HEX_BRUMA}" stroke-width="1.8"/>
  <line x1="6" y1="18.5" x2="18" y2="18.5" stroke="{HEX_BRUMA}" stroke-width="1.5" stroke-linecap="round"/>
</svg>
""",
    # 6. Quilla (Escudo Antirrastreo)
    "noutrora-shield.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <path d="M 12 2.5 L 20 6 C 20 13.5, 16.5 18.5, 12 21.5 C 7.5 18.5, 4 13.5, 4 6 Z" stroke="{HEX_ABISMO}" stroke-width="1.8" stroke-linejoin="round"/>
  <line x1="12" y1="5" x2="12" y2="19.5" stroke="{HEX_BRUMA}" stroke-width="1.5"/>
</svg>
""",
    # 7. Cometa '94 (Netscape)
    "noutrora-mosaic94.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <path d="M 3 19 Q 12 12 21 19" stroke="{HEX_BRUMA}" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M 5 14 Q 11 7 18.5 5.5" stroke="{HEX_ESPUMA}" stroke-width="1.6" stroke-dasharray="2 2" stroke-linecap="round"/>
  <circle cx="18.5" cy="5.5" r="2.2" fill="{HEX_ESPUMA}"/>
  <circle cx="10.5" cy="9.5" r="1.2" fill="{HEX_BRUMA}"/>
  <circle cx="5.5" cy="14" r="1" fill="{HEX_BRUMA}"/>
</svg>
""",
    # 8. Camarotes (Contenedores Multi-Cuenta)
    "noutrora-containers.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none">
  <rect x="3.5" y="3.5" width="7" height="7" rx="2" stroke="{HEX_ABISMO}" stroke-width="1.75"/>
  <rect x="13.5" y="3.5" width="7" height="7" rx="2" stroke="{HEX_BRUMA}" stroke-width="1.75"/>
  <rect x="3.5" y="13.5" width="7" height="7" rx="2" stroke="{HEX_ABISMO}" stroke-width="1.75"/>
  <circle cx="17" cy="17" r="3.5" stroke="{HEX_ABISMO}" stroke-width="1.75"/>
</svg>
""",
}


def draw_thick_round_line(draw: ImageDraw.ImageDraw, x1: float, y1: float, x2: float, y2: float, color: tuple, width: int):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    r = width / 2.0
    draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=color)
    draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=color)


def rotate_point(px: float, py: float, cx: float, cy: float, angle_deg: float) -> tuple[float, float]:
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    dx = px - cx
    dy = py - cy
    return (cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a)


def render_compass_isotipo_png(size: int = 2048) -> Image.Image:
    """
    Renderiza el isotipo oficial de Noutrora (Modo Calma #1B3644 + aguja romboidal bicolor a 24°)
    idéntico a #icon-puerto-base de noutrora_landing_page_oficial.html.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size / 2.0

    abismo = (27, 54, 68, 255)      # #1B3644
    bruma = (122, 158, 159, 255)    # #7A9E9F
    bruma_ring = (122, 158, 159, 140)
    espuma = (250, 249, 245, 255)   # #FAF9F5

    # 1. Disco exterior en Abismo Atlántico (#1B3644)
    pad_r = size * 0.468
    border_w = max(2, int(size * 0.022))
    draw.ellipse(
        (cx - pad_r, cy - pad_r, cx + pad_r, cy + pad_r),
        fill=abismo,
        outline=bruma_ring,
        width=border_w,
    )

    # 2. Circunferencia principal de la segunda «o» (Espuma de Sal #FAF9F5)
    ring_r = size * 0.305
    ring_w = max(4, int(size * 0.068))
    draw.ellipse(
        (cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r),
        outline=espuma,
        width=ring_w,
    )

    # 3. Muescas cardinales (Sur, Oeste, Este) en Bruma Costera (#7A9E9F)
    tick_inner = ring_r - ring_w * 0.90
    tick_outer = ring_r + ring_w * 0.45
    tick_w = max(2, int(size * 0.040))
    draw_thick_round_line(draw, cx, cy + tick_inner, cx, cy + tick_outer, bruma, tick_w)
    draw_thick_round_line(draw, cx - tick_outer, cy, cx - tick_inner, cy, bruma, tick_w)
    draw_thick_round_line(draw, cx + tick_inner, cy, cx + tick_outer, cy, bruma, tick_w)

    # 4. Eje Norte prominente (0° arriba) en Espuma de Sal (#FAF9F5)
    north_y1 = cy - ring_r - ring_w * 0.65
    north_y2 = cy - ring_r + ring_w * 0.85
    north_w = max(3, int(size * 0.060))
    draw_thick_round_line(draw, cx, north_y1, cx, north_y2, espuma, north_w)

    # 5. Aguja romboidal bicolor inclinada a 24° (idéntica a noutrora_landing_page_oficial.html)
    north_poly_raw = [
        (cx, cy - ring_r * 0.74),
        (cx + ring_r * 0.23, cy),
        (cx, cy - ring_r * 0.17),
        (cx - ring_r * 0.23, cy),
    ]
    south_poly_raw = [
        (cx, cy + ring_r * 0.74),
        (cx + ring_r * 0.21, cy),
        (cx, cy + ring_r * 0.17),
        (cx - ring_r * 0.21, cy),
    ]
    north_poly = [rotate_point(px, py, cx, cy, 24.0) for (px, py) in north_poly_raw]
    south_poly = [rotate_point(px, py, cx, cy, 24.0) for (px, py) in south_poly_raw]

    draw.polygon(south_poly, fill=bruma)
    draw.polygon(north_poly, fill=espuma)

    # 6. Centro de la aguja
    hub_r = size * 0.044
    draw.ellipse((cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r), fill=espuma)
    inner_hub_r = size * 0.020
    draw.ellipse((cx - inner_hub_r, cy - inner_hub_r, cx + inner_hub_r, cy + inner_hub_r), fill=abismo)

    return img


def main():
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    (BRAND_DIR / "noutrora.svg").write_text(ISOTIPO_SVG, encoding="utf-8")
    (BRAND_DIR / "noutrora-wordmark.svg").write_text(
        build_wordmark_svg(HEX_ABISMO, HEX_BRUMA, HEX_ESPUMA), encoding="utf-8"
    )
    (BRAND_DIR / "noutrora-wordmark-dark.svg").write_text(
        build_wordmark_svg(HEX_ESPUMA, HEX_BRUMA, HEX_HORIZONTE94), encoding="utf-8"
    )

    for filename, svg_code in UI_ICONS.items():
        (ICONS_DIR / filename).write_text(svg_code, encoding="utf-8")

    master = render_compass_isotipo_png(2048)
    resample_filter = getattr(Image, "Resampling", Image).LANCZOS
    master.resize((512, 512), resample_filter).save(BRAND_DIR / "noutrora-512.png")

    for s in (128, 64, 48, 32, 16):
        resized = master.resize((s, s), resample_filter)
        resized.save(BRAND_DIR / f"default{s}.png")

    print("✅ Activos vectoriales y PNGs sincronizados con noutrora_landing_page_oficial.html")


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/scripts/build.py"

APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

cat > "$APPS_DIR/noutrora.desktop" <<EOF
[Desktop Entry]
Version=1.0
Name=Noutrora
Comment=Navegador web ligero y personal
Exec="$DIR/run.sh" %u
Icon=$DIR/config/branding/noutrora-512.png
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
StartupWMClass=Noutrora
EOF

chmod +x "$APPS_DIR/noutrora.desktop"
update-desktop-database "$APPS_DIR" 2>/dev/null || true
echo "✅ Acceso directo e icono v2.0 de Noutrora actualizados ($APPS_DIR/noutrora.desktop)"

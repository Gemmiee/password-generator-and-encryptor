#!/usr/bin/env bash
# Wraps the PyInstaller Linux build into a .deb that Mint/Ubuntu/Debian can install with a double-click.
# Usage: packaging/build-deb.sh <version> <path-to-built-binary> [output-dir]
set -euo pipefail

VERSION="${1#v}"            # accept "v1.0" or "1.0"
BINARY="$2"
OUT_DIR="${3:-.}"
PKG="password-generator"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(mktemp -d)"
trap 'rm -rf "$ROOT"' EXIT
chmod 755 "$ROOT"           # mktemp makes it private; package dirs should be world-readable

# the app itself
install -Dm755 "$BINARY" "$ROOT/usr/bin/$PKG"

# menu entry
install -Dm644 "$HERE/$PKG.desktop" "$ROOT/usr/share/applications/$PKG.desktop"

# icons, one per size so the menu/panel can pick the sharpest
for size in 16 32 48 64; do
  install -Dm644 "$HERE/../icons/icon_$size.png" \
    "$ROOT/usr/share/icons/hicolor/${size}x${size}/apps/$PKG.png"
done

# package info shown by the installer
mkdir -p "$ROOT/DEBIAN"
cat > "$ROOT/DEBIAN/control" <<EOF
Package: $PKG
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Gemmiee <https://github.com/Gemmiee>
Homepage: https://github.com/Gemmiee/password-generator-and-encryptor
Description: Password generator and encryptor
 Generate passwords with 3 difficulty levels and a length of 6-20 characters,
 then encrypt them with SHA-256, SHA-512, MD5 or a Caesar cipher.
EOF

mkdir -p "$OUT_DIR"
dpkg-deb --build --root-owner-group "$ROOT" "$OUT_DIR/${PKG}_${VERSION}_amd64.deb"

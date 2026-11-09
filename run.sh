#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -d "$DIR/base/firefox" ]]; then
  python3 "$DIR/scripts/bootstrap.py"
else
  python3 "$DIR/scripts/build.py"
fi

PROFILE_DIR="$DIR/profile-test"

if [[ "${1:-}" == "--clean" ]]; then
  shift
  rm -rf "$PROFILE_DIR"
elif [[ "${1:-}" == "--lab" ]]; then
  shift
  PROFILE_DIR="$DIR/profile-lab"
elif [[ "${1:-}" == "--clean-lab" ]]; then
  shift
  PROFILE_DIR="$DIR/profile-lab"
  rm -rf "$PROFILE_DIR"
fi

mkdir -p "$PROFILE_DIR"
rm -rf "$PROFILE_DIR/startupCache"
export XDG_DATA_DIRS="$DIR/base/xdg-data:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
export MOZ_APP_REMOTINGNAME="Noutrora"
exec "$DIR/base/firefox/firefox" --class "Noutrora" --name "noutrora" --profile "$PROFILE_DIR" "$@"

#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/scripts/build.py"

PROFILE_DIR="$DIR/profile-test"

if [[ "${1:-}" == "--lab" ]]; then
  shift
  PROFILE_DIR="$DIR/profile-lab"
elif [[ "${1:-}" == "--clean-lab" ]]; then
  shift
  PROFILE_DIR="$DIR/profile-lab"
  rm -rf "$PROFILE_DIR"
fi

mkdir -p "$PROFILE_DIR"
exec "$DIR/base/firefox/firefox" --profile "$PROFILE_DIR" --no-remote "$@"

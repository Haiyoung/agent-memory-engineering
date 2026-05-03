#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

case "${1:-build}" in
  build)
    echo ":: Building book..."
    mdbook build
    echo ":: Done → ./book/"
    ;;
  serve)
    echo ":: Killing existing mdbook process (if any) ..."
    pkill -f "mdbook serve" 2>/dev/null && echo "   killed" || echo "   none running"
    echo ":: Starting dev server at http://localhost:3000 ..."
    mdbook serve --open
    ;;
  clean)
    echo ":: Cleaning build output..."
    mdbook clean
    ;;
  *)
    echo "Usage: $0 [build|serve|clean]"
    exit 1
    ;;
esac

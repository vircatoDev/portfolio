#!/usr/bin/env bash
# Push dist/ to the gh-pages branch; GitHub Pages serves it at https://vircatodev.github.io/portfolio/
# One orphan commit per deploy: the branch holds only the current site.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
remote=$(git -C "$ROOT" remote get-url origin)
commit=$(git -C "$ROOT" rev-parse --short HEAD)
site=$(mktemp -d)
cp -R "$ROOT/dist/." "$site"
touch "$site/.nojekyll"
git -C "$site" init -q -b gh-pages
git -C "$site" add -A
git -C "$site" commit -q -m "Deploy site from $commit"
git -C "$site" push -q -f "$remote" gh-pages
rm -rf "$site"
echo "Published $commit to gh-pages"

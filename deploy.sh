#!/bin/bash
echo "==============================="
echo "🚀 Deploy Hugo ke GitHub Pages"
echo "==============================="

cd "$(dirname "$0")"

echo "[1/4] Build Hugo..."
hugo || exit 1

echo "[2/4] Copy hasil build..."
cp -r public/* .

echo "[3/4] Git commit..."
git add .
git commit -m "deploy site"

echo "[4/4] Git push..."
git push

echo "✅ DEPLOY SELESAI"
echo "🌐 https://chipper26.github.io/efektifpedia/"

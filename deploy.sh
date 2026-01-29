#!/bin/bash

echo "Build Hugo..."
hugo

echo "Deploy blog only (tanpa index.html)..."
rsync -av \
  --exclude 'index.html' \
  public/ .

echo "Done."
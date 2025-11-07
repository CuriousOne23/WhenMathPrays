#!/bin/bash
# Sync local changes with GitHub (safe pull + push)

echo "Syncing with GitHub..."

# Add all changes
git add .

# Commit if there are changes
if git diff --staged --quiet; then
    echo "No changes to commit."
else
    git commit -m "auto: sync local changes"
fi

# Pull with rebase
git pull --rebase

# Push
git push

echo "Sync complete."

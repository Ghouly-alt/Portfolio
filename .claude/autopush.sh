#!/bin/sh
# Commit + push automatique vers Portfolio1 si des fichiers ont changé
cd "$CLAUDE_PROJECT_DIR" || exit 0
[ -n "$(git status --porcelain)" ] || exit 0
git add -A
git commit -q -m "Mise à jour automatique du portfolio

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
git push -q portfolio1 main

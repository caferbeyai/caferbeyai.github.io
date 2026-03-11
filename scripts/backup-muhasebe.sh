#!/bin/bash
# Backup 3CatsMuhasebe to GitHub
cd /home/caferbey/Desktop/3CatsMuhasebe
git add -A
git commit -m "Backup: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || exit 0
git push origin master

@echo off
git add .
git commit -m "Auto push-deploy via batch script"
git push
git push --force space
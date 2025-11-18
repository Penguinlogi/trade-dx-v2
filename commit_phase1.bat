@echo off
chcp 65001
git add .
git commit -m "Phase 1完了: 基盤整備 - config.json, common.py, file_handler.py, テストコード"
git tag -a v1.0-phase1 -m "Phase 1: 基盤整備完了"
echo Phase 1 のコミット完了


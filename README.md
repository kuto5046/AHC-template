# AHC-template
AHCのテンプレート

## 環境構築
- rustはcargo, pythonはryeでプロジェクト管理する。
- 提供されているローカル版のプログラムをtoolsに置く
- inputにデータを用意する(tools/in内のデータをcopyする or genモジュールで生成する)


### 実行方法

```bash
cargo run --release --bin=main < ./input/0000.txt
```

複数のテストケースでの評価
```bash
rye run python utils/evaluate.py
```
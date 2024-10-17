# AHC-template
Atcoder Heuristic Contestのテンプレート  
RustとPythonが実行できる環境を用意している。

### 環境構築
Pythonの場合は以下を実行する
```bash
uv sync
```

### 実行方法

標準入力を受け取って実行
```bash
cargo run --release --bin=main < ./input/0000.txt
```

複数のテストケースの評価
```bash
uv run python tools/evaluate.py
```

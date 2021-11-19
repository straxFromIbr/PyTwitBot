# PyTwitBot
- マルコフ連鎖を用いたPython製Twitter Bot
 
## 依存
- `mecab`
    - 形態素解析ツール

## 依存Pythonパッケージ
- `fugashi`
    - `mecab`のPythonインターフェース
- `emoji`, `neologdn` 
    - 記号除去など文章の正規化
- `markovify`
    - マルコフ連鎖ライブラリ
- `requests-oauthlib`
    - Twitter APIを叩くため

## 使い方
1. `src/config.py`を作成し、APIキーを保存

```python
CONSUMER_KEY = ...
CONSUMER_KEY_SECRET = ...
ACCESS_TOKEN = ...
ACCESS_TOKEN_SECRET = ...
```

2. 実行!
```
./twitbot.sh
```

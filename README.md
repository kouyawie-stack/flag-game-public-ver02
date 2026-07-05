# せかいの こっき クイズ

子ども向けの国旗クイズです。`flag-game.html` だけでゲーム本体が動き、任意で `voice` フォルダを追加するとVOICEVOXの音声を再生できます。

## ファイル構成

- `flag-game.html`: ゲーム本体。国データと国旗SVGをHTML内に含んでいます。
- `make_voices.py`: VOICEVOXから音声ファイルを作る補助スクリプトです。
- `voice/`: 生成後にできる音声フォルダです。Netlify Dropするときは `flag-game.html` と一緒にアップロードします。

## ローカルで遊ぶ

`flag-game.html` をブラウザで開くと遊べます。

音声ファイルの読み込みがブラウザ設定で止まる場合は、フォルダ内で簡易サーバーを起動して開きます。

```powershell
py -m http.server 8000
```

そのあと、ブラウザで次を開きます。

```text
http://localhost:8000/flag-game.html
```

## VOICEVOX音声を作る

1. VOICEVOXを起動します。
2. このフォルダで次を実行します。

```powershell
py make_voices.py
```

別の声にしたい場合は、スピーカーIDを指定します。

```powershell
py make_voices.py 1
```

生成された `voice` フォルダを `flag-game.html` と同じ場所に置くと、ゲーム内で音声ファイルが使われます。

選択肢の番号読み上げ用に `opt1.wav` から `opt4.wav` も作ります。ゲーム側を更新したあとに古い `voice` フォルダを使い続ける場合は、VOICEVOXを起動して `py make_voices.py` をもう一度実行してください。

## クレジット

このゲームの音声にはVOICEVOXを使用しています。

- 音声: VOICEVOX 四国めたん
- VOICEVOX: https://voicevox.hiroshiba.jp/

## GitHub Pagesで公開する

このリポジトリはGitHub Pagesでそのまま公開できます。

1. GitHubのリポジトリ画面で `Settings` を開きます。
2. `Pages` を開きます。
3. `Source` を `Deploy from a branch` にします。
4. `Branch` は `main`、フォルダは `/ root` を選びます。
5. `Save` します。

公開URLは通常、次の形になります。

```text
https://ユーザー名.github.io/リポジトリ名/
```

## Codexで改修するときのメモ

このゲームは1ファイル構成なので公開は簡単です。一方で大きな変更を続けるなら、将来的に `data.js`、`style.css`、`app.js` に分けると編集しやすくなります。

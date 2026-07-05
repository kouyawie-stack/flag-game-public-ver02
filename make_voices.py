# -*- coding: utf-8 -*-
"""
かわいい アニメ風 こえ（VOICEVOX）の おんせいファイルを つくる スクリプト。

つかいかた:
  1) VOICEVOX を ダウンロードして きどう する (https://voicevox.hiroshiba.jp/)
     → エンジンが http://127.0.0.1:50021 で うごきます。
  2) flag-game.html と この make_voices.py を おなじ フォルダに おく。
  3) ターミナル(コマンドプロンプト)で:
        py make_voices.py
     ※ python コマンドが使えるPCでは:  python make_voices.py
     ※ こえを かえたい ときは:  py make_voices.py 1
        (うしろの すうじが スピーカーID。れい: 2=四国めたん ノーマル, 3=ずんだもん,
          0=四国めたん あまあま, 8=春日部つむぎ など)
  4) 「voice」フォルダが できて、その なかに 100カ国ぶん + フレーズの .wav が はいります。
  5) flag-game.html を ひらくと、その こえで しゃべります。
     (ファイルを ひらくだけで うまく ならない ときは、フォルダごと むりょうの
      ホスティング(Netlify Drop など)に あげて URL で ひらくと かくじつです)
"""
import re, json, os, sys, urllib.request, urllib.parse

HTML    = "flag-game.html"
try:
    SPEAKER = int(sys.argv[1]) if len(sys.argv) > 1 else 2   # 2 = 四国めたん(ノーマル)
except ValueError:
    print("!! スピーカーIDは 数字で 指定してください。例: py make_voices.py 3")
    sys.exit(1)
HOST    = "http://127.0.0.1:50021"

PHRASES = {
    "ask":     "これはどこの国の国旗でしょう。",
    "opt1":    "いち、",
    "opt2":    "に、",
    "opt3":    "さん、",
    "opt4":    "よん、",
    "correct": "せいかい！ やったね！",
    "wrong":   "ざんねん。こたえは、",
}

VOICE_TEXT = {
    "gq": "せきどう ぎにあ",
}

def voice_text(text):
    # 現在の解説文は自然な日本語なので、音声用には表示用スペースと引用符だけ整える。
    out = re.sub(r"\s+", "", text)
    out = out.replace("「", "").replace("」", "")
    return out

def post(path, params=None, body=None, ctype=None):
    url = HOST + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, data=(body if body is not None else b""), method="POST")
    if ctype:
        req.add_header("Content-Type", ctype)
    return urllib.request.urlopen(req, timeout=30).read()

def synth(text):
    q = json.loads(post("/audio_query", {"text": text, "speaker": SPEAKER}))
    # 公開版に近い、自然で抑揚のある かわいい かんじに ちょうせい
    q["speedScale"]      = 1.08
    q["pitchScale"]      = 0.04
    q["intonationScale"] = 1.35
    q["volumeScale"]     = 1.0
    q["prePhonemeLength"]  = 0.02  # つなぎ目の まえの 無音を みじかく
    q["postPhonemeLength"] = 0.02  # つなぎ目の あとの 無音を みじかく
    return post("/synthesis", {"speaker": SPEAKER},
                body=json.dumps(q).encode("utf-8"), ctype="application/json")

def main():
    if not os.path.exists(HTML):
        print("!! flag-game.html が みつかりません。おなじ フォルダに おいてください。")
        return
    try:
        urllib.request.urlopen(HOST + "/version", timeout=5).read()
    except Exception:
        print("!! VOICEVOX エンジンに つながりません。VOICEVOX を きどう してから もういちど。")
        return

    html = open(HTML, encoding="utf-8").read()
    m = re.search(r"const FLAGS = (\[.*?\]);", html, re.S)
    if not m:
        print("!! flag-game.html から 国データを 読み取れませんでした。")
        return
    flags = json.loads(m.group(1))

    items = {f["code"]: VOICE_TEXT.get(f["code"], f["name"]) for f in flags}
    items.update({"info_" + f["code"]: voice_text(f["info"]) for f in flags})
    items.update(PHRASES)

    os.makedirs("voice", exist_ok=True)
    total = len(items)
    for i, (key, text) in enumerate(items.items(), 1):
        try:
            wav = synth(text)
            with open(os.path.join("voice", key + ".wav"), "wb") as fp:
                fp.write(wav)
            print(f"[{i}/{total}] ok  {key}  ({text})")
        except Exception as e:
            print(f"[{i}/{total}] NG  {key}  -> {e}")
    print("\nかんりょう！ 『voice』フォルダを flag-game.html と おなじ ばしょに おいてね。")

if __name__ == "__main__":
    main()

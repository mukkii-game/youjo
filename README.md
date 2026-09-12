# ょぅι゛ょ期の終わり

表紙を含む24ページのSF絵本。v0.1.0。

- 読む：`output/youjo-no-owari.html` または `output/youjo-no-owari.pdf`
- 本文を直す：`manuscript.md`
- 仕掛け・調査出典：`notes.md`（結末のネタバレあり）
- 絵：`assets/01.png`〜`08.png`
- 生成プロンプト：`image-prompts.json`

HTMLは単一ファイルで、画像と日本語フォントを内蔵しています。外部通信はありません。

## 再生成

Python 3、fontTools、PyMuPDF、ReportLabで `python3 build.py`。PDFはブラウザの印刷からも出力できます。

`build.py` は `assets` の画像を使用します。フォントはPyMuPDF同梱のDroid Sans Fallbackから本文の文字だけを取り出します。新たな本文に合わせてサブセットを更新します。

保存先は https://github.com/mukkii-game/youjo です。`manuscript.md` を本文の正本として、改稿履歴をGitに記録します。

`output/` は生成物のためGit管理から除外しています。クローン後に `pip install -r requirements.txt` → `python3 build.py` でHTMLとPDFを生成できます。公開状態を変更する処理や自動デプロイは含めていません。

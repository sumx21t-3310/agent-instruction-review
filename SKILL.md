---
name: agent-instruction-review
description: AGENTS.md や CLAUDE.md などのコーディングエージェント向け指示ファイルをレビューし、Baseline・Constitution・Articles の3層に整理する書き換え案を出す。既存の指示から格率を抽出し、普遍化して Constitution の候補を導き、採否は人間が決める。「AGENTS.md をレビューして」「CLAUDE.md を見直して」「指示ファイルを整理して」「エージェント向けの規約が増えすぎた」「Constitution を導いて」で発火。指示ファイルの中身を評価・整理したい場面では、ファイル名が明示されていなくても使う。対象外は、SKILL.md の検査(skill-creator へ渡す)、README や設計文書の添削(document-writing へ渡す)、コードの差分のレビュー(code-review へ渡す)、指示ファイルを白紙から新しく書く依頼(init へ渡す)。
---

# agent-instruction-review

コーディングエージェント向けの指示ファイルを評価し、長く運用できる形に整理する案を出します。
成果物はレビュー報告です。対象ファイルは、ユーザーが書き換えを頼んだときだけ編集します。

指示は、次の3層に整理します。

| 層 | 書く内容 | 変更の重さ |
| :-- | :-- | :-- |
| Baseline | 作業を始めるための入口。Canonical Command と Source of Truth への参照 | 軽い |
| Constitution | 長く維持する上位原則。ファイルパス、ツール名、バージョン、一時的な手順は含めない | 重い。人間が決める |
| Articles | Constitution を具体的な状況へ当てはめた規則 | 中程度 |

規則を先に Constitution と Articles へ振り分けると、既存の規則に合わせた原則をあとから作ることになります。
そのため、先に格率を抽出して原則の候補を導き、候補が確定してから Articles を整理します。

各検査の基準と例は [references/checks.md](references/checks.md) にあります。手順の中で指定した節だけを読みます。

## 手順

1. 対象を集める。
    - 指定されたファイルと、同じリポジトリにある `AGENTS.md`、`CLAUDE.md`、下位ディレクトリの `AGENTS.md` を一覧にする
    - ADR、How-to、設定ファイル、Canonical Command になるスクリプトの有無を調べる。移動先の候補になる
    - 次へ進む条件: 対象ファイルを1つ以上読み込めた。読み込めなければ停止条件に従う
2. Phase 1 の Instruction Hygiene を検査する。`references/checks.md` の「Phase 1」を読み、次の順に検査する。
    1. Information Safety
    2. Drift Resistance
    3. Documentation Responsibility
    4. ADR Separation
    5. Canonical Source
    6. Instruction Clarity
    7. Context Efficiency
    - Information Safety で機密情報を見つけたら、ほかの指摘より先にユーザーへ伝える。報告には値を書かず、場所と種類だけを書く
    - 判定が Revise の指摘には、ここで `Before` と `After` を書く。Phase 1 の書き換えは Constitution の採否に左右されないためである
    - 7項目のあとに、Baseline に残る事実の実在を確かめる。対象は、Canonical Command の入口と、Source of Truth への参照である。Articles の中に書かれた参照も対象にする。基準は `references/checks.md` の「Baseline Organization」の「実在の確認」にある。指摘の `Category` は Baseline Organization とする
    - 実在の確認は、手順6の返事に左右されないので、ここで行う。コマンドは実行しない。動くかどうかは `Reason` に「未確認」と書く
    - Baseline に当たらない事実の記述(アーキテクチャの説明、型やファイルの一覧、進捗)は、正しいかを確かめずに Externalize とする。正しさは、移動先の文書のレビューで確かめる
    - 指摘のなかった検査は、報告の先頭の「指摘なしの検査」に名前を書く
    - 次へ進む条件: 7項目と実在の確認のすべてについて、指摘を書いたか、指摘なしと判断した
3. 格率を抽出する(Maxim Extraction)。Phase 1 で Reject と Externalize にならなかった指示を、1つずつ「条件 → 行動 → 目的」の形に書き直す。
    - 目的は、対象の指示ファイルの、その指示と同じ節に書かれた文から読み取る。参照先の文書にだけ書かれた目的は使わず、「不明」と書く。推測で埋めた目的から原則を導くと、根拠のない原則になる
    - 指示の単位は、1つの条件と1つの行動の組とする。1つの段落に条件が2つあれば、格率を2つ書く
    - 格率は、報告の `## Maxims` の表に書く
    - 次へ進む条件: 対象の指示すべてに格率を書いた
4. 格率を普遍化する(Universalizability)。`references/checks.md` の「Phase 2」を読む。
    - 問いは「同じ条件に置かれたすべてのコーディングエージェントがこの行動を選んでも、行動が頼っている開発上の仕組みは成り立つか」とする
    - 成り立たない格率は Reject とする
    - 成り立つ格率のうち、複数の格率に共通する目的を1文にまとめたものを Constitution の候補とする
    - 候補は、候補がなければ Adopt のままだった指示を、1つ以上 Reject または Revise に変えること。手順2の検査や普遍化だけで Reject または Revise になる指示は、数に入れない
    - この条件を満たさないまとめは候補にせず、もとの格率の分類を「どちらでもない」とする。既存の規則を言い換えただけの原則を除くためである。候補にしなかったまとめは、理由を添えて報告の「候補にしなかったまとめ」に書く
    - 効果に数えた指示が、手順2の判定を変えると効果から外れる場合は、`Effect` にそう書く。候補を採るかどうかを、人間がその前提を知ったうえで決められるようにするためである
    - 実行時間、トークン消費、作業量はここでは評価しない。手順5で評価する
    - 次へ進む条件: すべての格率を、Reject、候補の根拠、どちらでもない、のいずれかに分けた
5. Constitution の候補を検査する。候補ごとに、Engineering Soundness、Operational Sustainability の順に評価する。
    - どちらかで落ちた候補は、落ちた理由を添えて報告に残す。Constitution には採らない
    - 対象ファイルにすでにある Constitution の項目も、同じ検査にかける
    - 次へ進む条件: すべての候補に、2つの評価の結果を書いた
6. 候補の採否を人間に尋ねる(Constitution Approval)。通った候補を `Human Decision Required` として示し、候補ごとに採否を尋ねる。
    - 採用された候補だけを Constitution として扱い、手順7へ進む
    - 返事を得られないときは、手順7と手順8を行わずに手順9へ進む。報告の先頭に、未決定の候補の数を書く
    - 候補が1つもなく、既存の Constitution もないときは、その事実を伝えて手順9へ進む
7. Phase 3 の Structure & Scope を整理する。`references/checks.md` の「Phase 3」を読み、次の順に検査する。
    1. Baseline Organization
    2. Constitution Mapping
    3. Constitution Consistency
    4. Article Scope
    5. Scope Inheritance
    6. Conflict Resolution
    - 対応する Constitution を説明できない Article は、そのまま採らない。Local Article、Baseline、How-to、ADR、Issue、不要、新しい Constitution の候補、のどれに当たるかを判定する
    - 問題のない Article は指摘にせず、`## Maxims` の表の「手順7の判定」に、対応する Constitution を書く
    - 次へ進む条件: すべての Article について、指摘を書いたか、表に判定を書いた
8. Phase 4 の Rewrite を書く。手順7で出した指摘のうち、直せるものに `Before` と `After` を付ける。
    - `After` は、条件と行動が1つの意味に読める文にする
    - 手順2で書いた `After` が、採用された Constitution と合わなくなっていたら書き直す
    - 次へ進む条件: 判定が Revise の指摘すべてに `Before` と `After` がある
9. 報告をファイルに書き出し、検証する。「出力形式」の形で書き、「機械的検証」のコマンドを実行する。
    - 保存先の指定がなければ、一時ディレクトリに置く
    - 次へ進む条件: 出力が `OK` になった。`NG:` の行が出たら、その行が示す箇所を直して再実行する
10. 報告をユーザーに示す。失敗した手順と行わなかった手順は、先頭に書く。

## 停止条件

次のどちらかに当たったら、レビューを止めてユーザーに伝えます。

- 対象の指示ファイルが見つからない、または読み込めない
- Constitution の候補の採否について、返事を得られない。手順6の分岐に従い、Phase 2 までの報告を出して止まる

次のどれかに当たったら、その指摘だけを `Human Decision Required` として報告し、レビューは続けます。

- 移動先(ADR、How-to、Secret Store、設定ファイル)がリポジトリにない。新しい置き場所を決めず、`Destination` に「置き場所は未定」と書く
- 2つの Article が同じ条件で競合し、Constitution に合うほうを1つに決められない。どちらも Constitution から導かれる場合と、どちらも対応する Constitution を持たない場合が当たる。優先順位を決めない

Constitution の追加、変更、削除を、スキルの判断だけで確定してはなりません。Constitution を変えると、そこから導いた Articles すべての根拠が変わるためです。

## 判定

| 判定 | 意味 |
| :-- | :-- |
| Adopt | 今の形で採用できる |
| Revise | 意図は妥当で、表現、条件、責務、適用範囲のどれかを直す |
| Local-only | 共通の原則ではないが、限られたスコープでは有効 |
| Externalize | 必要な情報だが、指示ファイルに置く内容ではない。移動先を `Destination` に書く |
| Reject | 規則または原則として採らない |
| Human Decision Required | 技術的な評価だけでは決められない。Constitution の追加、変更、削除はこの判定にする |

確かめる手段がない指摘(たとえば、参照先のスクリプトが今も動くか)は、誤りと断定せず、`Reason` に「未確認」と書きます。

## 判定が分かれやすい例

Good: 複数の格率から、候補がなければ Adopt のままだった指示を変える原則を導く。

```text
格率: テストが作業完了を妨げているとき、検証を壊して完了させない(目的: 検証可能性の維持)
格率: 失敗を成功として扱わない(目的: 検証可能性の維持)
候補: 変更の検証可能性を損なうことで作業完了を達成してはならない。
効果: 「性能の改善は、体感で速くなっていればよい」を Revise にする(計測で確かめる形へ)。
```

「CI が赤いときは該当テストを skip してよい」は、普遍化だけで Reject になるので、効果には数えない。

Bad: 既存の規則を1つずつ言い換えて候補にする。

```text
規則: すべての Repository に interface を作成する。
候補: Repository は常に抽象化する。
```

Bad と判定する理由: 規則を抽象的な語に置き換えただけで、どの指示も Reject にも Revise にもならず、既存の規則を正当化するための原則になっている。

Good: Constitution に対応しない Article を、置き場所の判定にかける。

```text
Article: Widget を追加するときは、次の8手順に従う。(以下、手順)
判定: Externalize。Destination は How-to。指示ファイルには参照だけを残す。
```

Bad: Constitution に対応しない Article のために、新しい Constitution を作る。

```text
Article: Widget を追加するときは、次の8手順に従う。
候補: Widget の追加は定められた手順で行う。
```

Bad と判定する理由: 1つの Article を説明するためだけの原則で、ほかの状況に当てはまらない。

## 出力形式

報告は次の形で書きます。`### C-NN` が Constitution の候補、`### F-NN` が指摘です。

````markdown
# Review: <対象ファイル>

未決定の Constitution 候補: <数>
行わなかった手順: <なし、または手順の番号と理由>
指摘なしの検査: <なし、または検査の名前>

## Maxims

| ID | 場所 | 条件 | 行動 | 目的 | 分類 | 手順7の判定 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| M-01 | <ファイルと行> | <条件> | <行動> | <目的、または「不明」> | <Reject、C-NN の根拠、どちらでもない> | <Adopt(C-NN)、F-NN、未実施> |

## Constitution Candidates

候補にしなかったまとめ:

- <まとめの1文>: <候補にしなかった理由>

### C-01
- Statement: <候補の1文>
- Derived-from: <もとになった格率と、その指示の場所>
- Effect: <候補がなければ Adopt のままだった指示のうち、この候補で Reject または Revise になるもの>
- Engineering Soundness: <結果と理由>
- Operational Sustainability: <結果と理由>
- Verdict: Human Decision Required

## Findings

### F-01
- Finding: <何を検出したか>
- Location: <ファイルと行>
- Category: <検査の名前>
- Principle: <関連する Constitution。なければ「なし」>
- Reason: <なぜ問題か>
- Verdict: <判定>
- Destination: <移動先。なければ行ごと省く>

Before:
```text
<今の記述>
```

After:
```text
<推奨する記述>
```
````

- `Category` は、手順2、手順4、手順5、手順7に出てくる検査の名前から選ぶ。2つの検査に当たる指摘は、手順で先に出てくる検査を選び、もう一方を `Reason` に書く
- `Principle` に書くのは、人間が採用を決めた Constitution だけとする。採否が決まっていない候補が関わるときは「なし(C-01 は未決定)」と書く
- 問題のない指示は指摘にしない。Adopt の指摘を書くのは、検査が確認を求めている項目(たとえば `CLAUDE.md` が `@AGENTS.md` を参照していること)だけとする
- `Before` と `After` は、Revise では必ず書く。合わない指摘では省く
- Externalize の指摘で、指示ファイルに参照の文を残すときは、残す文を `After` に書く
- 候補にしなかったまとめがなければ、「候補にしなかったまとめ: なし」と書く
- Information Safety の指摘には `Before` を書かない。報告に機密情報を写さないためである
- 人間が採用を決めた候補は、`Verdict` を `Adopt` に変え、`- Approval: <決めた人と日付>` の行を足す

## 機械的検証

報告を書き出したら、次のコマンドで形式を検査します。スキルのフォルダで実行します。

```bash
uv run assets/check-review.py <報告のファイル>
```

出力が `OK`、終了コードが 0 なら合格です。`NG:` の行が出た場合は、その行が示す箇所を直して再実行します。

検査する内容は次のとおりです。

- `## Maxims` の節があること
- 指摘と候補に、必須の項目がそろっていること
- 候補の `Effect` が「なし」ではないこと
- `Category` と `Verdict` が、決められた値であること
- Revise の指摘に `Before` と `After` があること
- Externalize の指摘に `Destination` があること
- Information Safety の指摘に `Before` がないこと
- Constitution の候補の `Verdict` が `Human Decision Required`、`Adopt`、`Reject` のどれかであること。`Adopt` の候補には `Approval` があること

スクリプトが確かめるのは形式です。指摘の内容が妥当かどうかは、手順の各検査で判断します。

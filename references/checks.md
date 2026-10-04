# 検査の基準

SKILL.md の手順から参照する、各検査の基準と例です。手順で指定された Phase の節だけを読みます。

- [Phase 1: Instruction Hygiene](#phase-1-instruction-hygiene)
- [Phase 2: Constitution Derivation](#phase-2-constitution-derivation)
- [Phase 3: Structure & Scope](#phase-3-structure--scope)

情報の置き場所は、次の表で判断します。

| 情報 | 置き場所 |
| :-- | :-- |
| 実行の入口、参照先 | Baseline |
| 上位原則 | Constitution |
| 具体的な行動規則、制約 | Articles |
| 意思決定の理由、比較、経緯 | ADR |
| 特定の作業の手順 | How-to |
| 学習のための段階的な説明 | Tutorial |
| 概念やアーキテクチャの説明 | Explanation |
| SDK のバージョンのような現在値 | 設定ファイル |
| API キーのような秘密 | Secret Store、環境変数 |
| 一時的な作業の状態 | Issue、PR、Task |

## Phase 1: Instruction Hygiene

### Information Safety

機密情報が書かれているかを確かめます。見つけたら、ほかの検査より先に、安全な場所への移動を伝えます。

- 対象: API キー、Access Token、Personal Access Token、パスワード、Cookie、セッション情報、秘密鍵、認証情報を含む接続文字列、非公開の情報、個人情報、顧客に固有の情報
- 指示ファイルには、値ではなく取得方法を書く
- 報告には値を写さない。場所と種類だけを書く

Good:

```text
API キーは OPENAI_API_KEY 環境変数から取得する。
```

Bad:

```text
API キーは sk-xxxx を使う。
```

Bad と判定する理由: 値そのものが、リポジトリと、エージェントに毎回渡すコンテキストの両方に残る。

### Drift Resistance

時間や環境の変化で古くなる値が、固定で書かれているかを確かめます。評価するのは、今正しいかではなく、将来も正しい状態を保てるかです。

- 対象: 絶対パス、ユーザー名を含むパス、一時的なディレクトリ構成、バージョン番号、Issue 番号、PR 番号、一時的なブランチ名、担当者名、一時的な URL、特定の LLM のモデル名、今の進捗、一時的な運用の状態
- 別の Source of Truth があれば、値ではなく参照のしかたを書く

Good:

```text
使用する .NET SDK は global.json の指定に従う。
```

Bad:

```text
.NET SDK 10.0.100 を使用する。
```

Bad と判定する理由: global.json を更新すると、指示ファイルの値だけが古いまま残る。

### Documentation Responsibility

指示ファイルに置く内容ではない文章が混ざっているかを確かめます。Diátaxis の分類では、指示ファイルは Reference に最も近く、エージェントが従う Policy と Constraint も含みます。

| 種類 | 扱い |
| :-- | :-- |
| Reference | 今有効な規則、契約、制約、参照先。指示ファイルの中心になる |
| How-to | 長い手順は別文書へ移し、参照だけを残す |
| Tutorial | 指示ファイルには置かない |
| Explanation | 今守る原則と制約だけを残し、詳しい説明は別文書へ移す |

事実を述べる記述(アーキテクチャの説明、型やファイルの一覧、進捗)は Explanation として移します。記述が正しいかは確かめません。指示ファイルに置いたままだと、コードが変わるたびにずれるためです。

Good:

```text
Widget を追加するときは docs/how-to/add-widget.md の手順に従う。
```

Bad: 8手順の本文を指示ファイルに書く。

Bad と判定する理由: Widget を追加しない作業でも、8手順が毎回コンテキストに入る。

### ADR Separation

意思決定の履歴が混ざっているかを確かめます。ADR は「なぜ決めたか」を扱い、指示ファイルは「今どう行動するか」を扱います。

- ADR へ移す内容: 採用した理由、比較した対象、別案を採らなかった理由、判断した時点の背景、トレードオフ、判断した日時、見直す条件
- 指示ファイルに残す内容: ADR から導かれた、今有効な制約

Good:

```text
Domain から Infrastructure へ依存してはならない。
```

Bad:

```text
以前は Domain から直接 DB を呼んでいたが、テストが遅くなったので、検討の結果、依存を禁止した。
```

Bad と判定する理由: 経緯を読んでも、今の行動は変わらない。

### Canonical Source

共通の規則が複数のファイルに重複しているかを確かめます。エージェント共通の指示は `AGENTS.md` を Canonical Source とします。

- `CLAUDE.md` は `@AGENTS.md` を参照していること
- 共通の規則を `CLAUDE.md` へコピーしていないこと
- 同じ規則に、Source of Truth が2つ以上ないこと
- Claude に固有の指示だけを、`CLAUDE.md` に足してよい

### Instruction Clarity

指示を1つの意味に読めるかを確かめます。

- 判断の基準を持たない語を探す。「適切に」「必要に応じて」「可能なら」「なるべく」「十分に」「適宜」
- 規則が「条件 → 判断 → 行動」として読めること
- 禁止そのものが目的ではない規則は、肯定形にする。秘密情報のコミットの禁止のように、禁止が制約の中身であるときは否定形でよい
- 「原則として」「通常は」と書くときは、例外になる条件を説明できること

Good:

```text
公開 API の振る舞いを変更した場合は、変更された契約を検証するテストを追加する。
```

Bad:

```text
必要に応じてテストを追加する。
```

Bad と判定する理由: 「必要」かどうかを判断する条件がなく、エージェントごとに結果が変わる。

### Context Efficiency

毎回コンテキストに入れる価値のある情報だけが残っているかを確かめます。

- 同じ意味の規則が重複していないこと
- Constitution と Article で、同じ説明を繰り返していないこと
- 使う回数の少ない手順を、毎回読み込ませていないこと
- 詳しい説明を別文書へ移せるか、下位ディレクトリの `AGENTS.md` へスコープを絞れるか、参照だけを残せるかを検討する

Constitution の数に上限は設けません。各原則が、ほかと重ならない役割を持ち、毎回参照する価値があるかで評価します。

## Phase 2: Constitution Derivation

### Maxim Extraction

指示を「条件 → 行動 → 目的」に書き直します。

```text
指示: 失敗したテストを削除して CI を通してはならない。

条件: テストが作業完了を妨げている
行動: 検証を壊すことで作業完了を達成しない
目的: 作業結果の検証可能性を保つ
```

### Universalizability

格率を、同じ条件に置かれたすべてのコーディングエージェントが採ると仮定します。行動が頼っている開発上の仕組みが成り立たなくなる格率は、Reject とします。

```text
格率: テストが失敗した場合、作業完了のために失敗したテストを削除してよい。
普遍化: すべてのエージェントが、失敗した検証を削除して作業を完了させる。
結果: テストによる検証という仕組みが成り立たなくなる。Reject。
```

複数の格率に共通する目的を1文にまとめられたら、Constitution の候補とします。

```text
公開 API 変更時にはテストを追加する。
失敗したテストを削除して CI を通してはならない。
失敗を握りつぶして成功として扱ってはならない。

候補: 変更の検証可能性を損なうことで作業完了を達成してはならない。
```

効率(実行時間、トークン消費、作業量)は、ここでは評価しません。Operational Sustainability で評価します。

### Engineering Soundness

候補を、次の順に評価します。

| 項目 | 確かめること |
| :-- | :-- |
| 責務 | だれが何を担当するかが決まっている。責務の重複と、判断する主体が決まっていない状態を警告する |
| 依存関係 | 依存が明示されている。隠れたグローバル状態と、暗黙の外部依存を生まない |
| 境界と契約 | 公開 API、データモデル、モジュール境界のような、変更コストの高い契約を、内部実装より慎重に扱っている |
| 変更容易性 | 1つの変更が、関係のない多くの箇所へ広がらない。DRY そのものではなく、同じ変更理由がどこまで広がるかを見る |
| 単純さ | KISS と YAGNI に沿う。今要らない抽象化や拡張ポイントを、将来の可能性だけを理由に足さない |
| 検証可能性 | 正しく動いていることを観測し、確かめられる |
| 失敗処理 | 失敗を隠さない。だれが検出し、だれが判断し、だれへ通知し、だれが回復するかを説明できる |

SOLID や特定の設計パターンを、機械的に当てはめる検査ではありません。

### Operational Sustainability

候補を、1年後も同じ原則として運用を続けられるかで評価します。次の変化を想定します。

- 開発者、コード量、Issue と PR が増える
- 担当者が交代する
- 使うツール、LLM、ディレクトリ構成が変わる

規則をすべての対象へ当てはめたときの負荷も確かめます。対象は、実行時間、レビュー時間、トークン消費、CI のコスト、人間の承認の回数、作業のスループットです。

- 普遍化できても、運用コストが大きく続けられない候補は、Constitution に採らない
- 特定の人の記憶、善意、注意力に頼る候補は警告する

### Constitution Approval

Universalizability、Engineering Soundness、Operational Sustainability を通った候補だけを、人間に示します。採否を決めるのは人間です。

## Phase 3: Structure & Scope

### Baseline Organization

実行環境と基本コマンドの情報を Baseline へ整理します。Baseline に残す情報は、次をすべて満たすこと。

- 作業を始めるときに、高い頻度で要る
- Source of Truth が決まっている
- 現在値を二重に管理しない
- 詳しい How-to ではない
- 一時的な作業に限られない

`./scripts/test` のような Canonical Command があれば、内部のテスト対象やオプションを指示ファイルに重ねて書きません。

#### 実在の確認

指示ファイルに残ってよい事実は、Baseline の Canonical Command と Source of Truth への参照だけです。この2つは、実在を確かめます。SKILL.md の手順2で行います。

- 対象: コマンドの入口になるスクリプト、参照先のファイルとディレクトリ。Articles の中に書かれた参照も対象にする
- 確かめ方: ファイルまたはディレクトリがあることを、一覧や検索で確かめる。コマンドは実行しない
- 実在しない参照は Revise とし、`Reason` に、何を探して見つからなかったかを書く。正しい参照先が見つかれば `After` に書き、見つからなければ Human Decision Required とする
- コマンドが今も通るかは確かめない。`Reason` に「未確認」と書く

Good:

```text
Finding: `docs/user/` を編集先として挙げているが、このディレクトリはない。
Reason: `docs/` の下を一覧にして確かめた。
```

Bad:

```text
Finding: アーキテクチャの節にある型名が、コードに見つからない。
```

Bad と判定する理由: アーキテクチャの説明は Baseline に当たらない事実で、Externalize の対象である。型名を1つずつ照合しても、指示ファイルに置く内容にはならない。

### Constitution Mapping

Article ごとに、どの Constitution から導かれるかを確かめます。

```text
Constitution: 現在必要な複雑さだけを導入する。
Article: 複数実装や交換の必要性がない境界には、将来利用する可能性だけを理由に interface を追加しない。
```

対応する Constitution を説明できない Article は、次のどれに当たるかを判定します。

| 当たるもの | 判定 |
| :-- | :-- |
| 特定のスコープだけの規則 | Local-only |
| 実行の入口、参照先 | Revise。Baseline へ移す |
| 手順、意思決定の記録、一時的な作業 | Externalize |
| 不要な規則 | Reject |
| 新しい Constitution が要る | Human Decision Required |

### Constitution Consistency

Article が Constitution と矛盾していないかを確かめます。矛盾する Article は Revise または Reject とします。

```text
Constitution: 現在必要な複雑さだけを導入する。
Article: すべての Repository に interface を作成する。
判定: Article が上位原則と衝突している。Revise または Reject。
```

### Article Scope

Article を置くスコープを確かめます。規則として正しいかに加えて、そのスコープから当てはめてよいかを評価します。

```text
Repository/AGENTS.md          リポジトリ全体に当てはめる原則と条項
src/Rendering/AGENTS.md       Rendering だけに当てはめる条項
tests/AGENTS.md               テストコードだけに当てはめる条項
```

### Scope Inheritance

階層になった `AGENTS.md` の継承を確かめます。

- Constitution はルートで定義する
- 下位の `AGENTS.md` は、対象のスコープに要る Articles を足すか、上位の Article を具体化する
- 下位の `AGENTS.md` は、上位の Constitution を変えず、無効にもしない
- Constitution に反する Local Article は無効とする

```text
Root Constitution: 変更の検証可能性を損なってはならない。
tests/AGENTS.md:   失敗したテストは削除してよい。
判定: Reject。
```

### Conflict Resolution

規則が競合したら、次の順で解決します。より狭いスコープの規則を、そのまま優先してはなりません。

1. Constitution に合うほう
2. より狭いスコープの Article
3. より広いスコープの Article

どちらの Article も Constitution から導かれ、同じ条件で競合するときは、Human Decision Required とします。

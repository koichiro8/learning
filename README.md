# Ward

## モチベーション

Pythonのテストフレームワークの[Ward](https://ward.readthedocs.io/en/latest/)というものが話題になっていたので、Pytestと比較してみた。

## 比較した観点

- テストの書き方
- Fixture
- Mock
- Assert
- Table driven testing (Parameterised testing)
- Coverage
- Mark
- Plugins
- Performance
- Async
- Config
- Tox

## 結論

Pytestに影響を受けていると記載されている通り、Pytestを使ったことがあれば簡単に使える。まだ開発されたばかりということもあり、Pytestから乗り換えるほどのものではない。やはり、Pytestは最高ですね。

## 注意点

Wardのclickのバージョン制約とFastAPIのuvicornのclickのバージョン制約が一致しないので、Poetryなどのパッケージマネージャーを使用する場合は注意。現状FastAPIを使う場合はWardは使わない方が良さそう。（一応、Hypercornというuvicornの代替パッケージはあるが正直イケてない。）

## テストの書き方

- メソッド名がテストケース名にならない。デコレータの引数にテストケース名を指定する。ここは良い点。

## Fixture

- Pytestにある`autouse`がない。DBの初期化などを自動で実行されないのが不便。
- globalのscopeのfixtureを作れない。
  - asyncioのevent_loopの問題？
- builtinのfixtureがない。
- 使用するfixtureは明示的に指定する。conftest.pyのように暗黙に使われることがない。良いような悪いような。

## Mock

- pytest-mockのようなものはない。

## Assert

- `ward.expect`にヘルパーがある。
- `pytest.raises`相当のExceptionを評価する`ward.raises`というものがある。

## Table driven testing (Parameterised testing)

- forループでテストケースを定義する。
- テストケースの引数で`each`を使用する。

## Coverage

- [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/index.html)を使う。
  - `coverage run -m ward`
- pytest-covに慣れていると適切なレポートを出すために`Coverage.py`を調べないといけないのが少し面倒。

## Mark

- tagsに設定できる。
- ファイル単位で設定できないのが不便。

## Plugins

- 現在開発中らしい。

## Performance

- 遅くはない、が、上述したglobalのfixtureが作成できないのでテストケースが増えると遅くなりそう。

## Async

- デフォルトでasyncのテストケースに対応している。

## Config

- pyproject.tomlで設定可能。

## Tox

- Pytestと特に違いはない。

# Pythonユニットテスト入門
～スライムバトルゲームを例に～

## 目次
1. [ユニットテストとは](#ユニットテストとは)
2. [テストの実行方法](#テストの実行方法)
3. [テストコードの構造](#テストコードの構造)
4. [各テストの解説](#各テストの解説)
5. [テストの書き方のコツ](#テストの書き方のコツ)
6. [テストレポートの生成](#テストレポートの生成)

## ユニットテストとは

ユニットテストは、プログラムの小さな部品（ユニット）が正しく動作することを確認するためのテストです。
スライムバトルゲームの場合、以下のような項目をテストします：

- スライムが正しく初期化されるか
- 賢者の呪文が正しく動作するか
- バトルシステムが正しく機能するか
- スライムのビジュアル表現が正しく動作するか

これらのテストを自動化することで：
- バグの早期発見
- 安全なコード修正
- 仕様の明確化
が可能になります。

## テストの実行方法

### 1. 通常のテスト実行

```bash
# 通常実行
python -m unittest test_slime_battle.py

# 詳細な実行結果を表示
python -m unittest test_slime_battle.py -v
```

### 2. テストレポート付きの実行

```bash
# テストレポートを生成しながら実行
python test_report.py
```

### 3. 実行結果の見方

```
test_battle_initialization (test_slime_battle.TestBattle) ... ok
test_battle_first_turn (test_slime_battle.TestBattle) ... ok
test_status_effects (test_slime_battle.TestBattle) ... ok
```

- `ok`: テスト成功
- `FAIL`: テスト失敗
- `ERROR`: エラー発生

## テストコードの構造

テストコードは以下のような構造になっています：

```python
class TestSlimeBase(unittest.TestCase):
    def setUp(self):
        """各テストケース実行前の準備"""
        self.slime = BaseSlime()
        
    def test_slime_initialization(self):
        """基本スライムの初期化テスト"""
        self.assertIsNotNone(self.slime.hp)
        self.assertIsNotNone(self.slime.attack)
        self.assertIsNotNone(self.slime.defense)
        self.assertEqual(self.slime.status_effects, [])

    def test_slime_take_damage(self):
        """ダメージ計算のテスト"""
        initial_hp = self.slime.hp
        damage = 10
        self.slime.take_damage(damage)
        self.assertEqual(self.slime.hp, initial_hp - damage)
```

### 重要な要素

1. **テストクラス**
   - `unittest.TestCase`を継承
   - 関連するテストをグループ化
   - 例：`TestSlimeBase`, `TestSage`, `TestBattle`, `TestSlimeArt`

2. **setUp メソッド**
   - 各テストの前に実行
   - テストに必要な準備を行う
   - 例：テスト用のスライムやプレイヤーの初期化

3. **テストメソッド**
   - `test_`で始まる名前
   - 1つのテストケースを表す
   - docstringでテストの目的を説明

## 各テストの解説

### 1. スライムのテスト（TestSlimeBase）

```python
def test_slime_initialization(self):
    """基本スライムの初期化テスト"""
    self.assertIsNotNone(self.slime.hp)
    self.assertIsNotNone(self.slime.attack)
    self.assertIsNotNone(self.slime.defense)
    self.assertEqual(self.slime.status_effects, [])
```

このテストでは：
- スライムの基本属性（HP、攻撃力、防御力）が設定されているか
- 状態異常リストが正しく初期化されているか
を確認します。

### 2. 賢者のテスト（TestSage）

```python
def test_spell_casting(self):
    """呪文詠唱テスト"""
    target = BaseSlime()
    initial_mp = self.sage.mp
    
    # メラの詠唱テスト
    self.sage.cast_spell("メラ", target)
    self.assertTrue(self.sage.mp < initial_mp)  # MPが消費されているか
    self.assertTrue(target.hp < target.max_hp)  # ダメージが入っているか
```

このテストでは：
- 呪文使用時のMP消費
- 対象へのダメージ処理
- 呪文の効果（ダメージ、回復、状態変化）
を確認します。

### 3. バトルのテスト（TestBattle）

```python
def test_battle_initialization(self):
    """バトル初期化テスト"""
    self.assertIsNone(self.battle.current_enemy)
    self.assertEqual(self.battle.turn_count, 0)
    
    self.battle.start_battle()
    
    self.assertIsNotNone(self.battle.current_enemy)
    self.assertEqual(self.battle.turn_count, 0)
```

このテストでは：
- バトル開始前の初期状態
- バトル開始後の状態変化
- ターン数の管理
を確認します。

### 4. スライムアートのテスト（TestSlimeArt）

```python
def test_get_slime_art(self):
    """スライムのアスキーアート取得テスト"""
    test_slimes = [
        BaseSlime(),        # 通常スライム
        MetalSlime(),       # メタルスライム
        StrayMetal(),       # はぐれメタル（👑なし）
        KingSlime(),        # キングスライム（👑あり）
        PoisonSlime(),      # 毒スライム
        MetalKingSlime()    # メタルキングスライム（👑あり）
    ]
    
    for slime in test_slimes:
        art = self.art.get_slime_art(slime)
        self.assertIsNotNone(art)
        self.assertIsInstance(art, str)
        self.assertTrue(len(art) > 0)
        
        # 特定のスライムの特徴をチェック
        if isinstance(slime, MetalKingSlime):
            self.assertIn("👑", art)  # メタルキングスライムは👑を持つ
        elif isinstance(slime, (MetalSlime, StrayMetal)):
            self.assertNotIn("👑", art)  # メタルスライムとはぐれメタルは👑を持たない
        elif isinstance(slime, KingSlime):
            self.assertIn("👑", art)  # キングスライムは👑を持つ
        elif isinstance(slime, PoisonSlime):
            self.assertIn("☠", art)  # 毒スライムは☠を持つ

def test_get_slime_color(self):
    """スライムの色情報取得テスト"""
    test_slimes = [
        BaseSlime(),        # 青
        MetalSlime(),       # 銀
        KingSlime(),        # 紫
        StrayMetal(),       # 金
        PoisonSlime(),      # 紫
        MetalKingSlime()    # 金
    ]
    
    for slime in test_slimes:
        color = self.art.get_slime_color(slime)
        self.assertIsNotNone(color)
        self.assertIsInstance(color, str)
        self.assertTrue(color.startswith("\033["))
```

このテストでは：
- 各種スライムのアスキーアート生成
- 特定のスライム種別に応じた特徴（👑、☠など）の存在確認
- 色情報の取得と形式
を確認します。

## テストの書き方のコツ

### 1. テストの名前付け
良い例：
```python
def test_slime_takes_damage_when_attacked(self):
def test_sage_learns_new_spells_on_level_up(self):
```
- 何をテストするのか明確
- 期待される結果が分かる
- 具体的な動作を示す

### 2. 1つのテストで1つの機能
良い例：
```python
def test_spell_casting(self):
    self.sage.cast_spell("メラ", target)
    self.assertTrue(self.sage.mp < initial_mp)
```
- メラの詠唱に焦点を当てている
- 確認項目が明確
- 副作用を含まない

### 3. assertの使い方
よく使うassert：
- `assertEqual(a, b)`: aとbが等しいか
- `assertTrue(x)`: xが真か
- `assertIsNotNone(x)`: xがNoneでないか
- `assertIsInstance(x, type)`: xが指定の型か

例：
```python
self.assertEqual(self.slime.hp, initial_hp - damage)  # ダメージ計算
self.assertTrue(len(self.sage.spells) > 0)  # 呪文の存在
self.assertIsInstance(color, str)  # 型チェック
```

### 4. テストの準備
- `setUp`メソッドを活用
- テストに必要な最小限の準備だけを行う
- テストデータは分かりやすい値を使用

```python
def setUp(self):
    self.sage = Sage("テストプレイヤー")
    self.battle = Battle(self.sage, test_mode=True)
```

## テストレポートの生成

テスト結果を分かりやすく記録するために、テストレポートを生成できます：

```python
# test_report.pyを実行
python test_report.py
```

生成されるレポートの形式：
1. Markdown形式 (.md)
   - 実行概要（日時、テスト数、成功/失敗数）
   - テストクラスごとの結果
   - 各テストの詳細（説明、結果、実行時間）

2. HTML形式 (.html)
   - 見やすいレイアウト
   - 色分けされた結果表示
   - 詳細なエラー情報

## まとめ

ユニットテストを書くことで：
1. コードの品質を保証
2. バグの早期発見
3. 安全なコード修正
4. 仕様の明確化
が可能になります。

初めは小さなテストから始めて、徐々にテストケースを増やしていくことをお勧めします。
また、テストレポートを活用することで、テスト結果の管理と共有が容易になります。 
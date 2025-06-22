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

def test_spell_learning_on_level_up(self):
    """レベルアップ時の呪文習得テスト"""
    # レベル3での呪文習得テスト
    while self.sage.level < 3:
        self.sage.level_up()
    self.assertIn("ベホイミ", self.sage.spells)
    self.assertIn("メラミ", self.sage.spells)
    
    # レベル5での呪文習得テスト
    while self.sage.level < 5:
        self.sage.level_up()
    self.assertIn("ベホマ", self.sage.spells)
    self.assertIn("メラゾーマ", self.sage.spells)

def test_equipment(self):
    """装備システムのテスト"""
    # 初期ステータスを保存
    initial_stats = {
        "hp": self.sage.max_hp,
        "mp": self.sage.max_mp,
        "attack": self.sage.attack,
        "defense": self.sage.defense,
        "magic_attack": self.sage.magic_attack,
        "magic_defense": self.sage.magic_defense
    }
    
    # 最強武器の装備テスト
    weapon = UltimateWeapon()
    self.sage.equip(weapon)
    self.assertEqual(self.sage.attack, initial_stats["attack"] + 50)
    self.assertEqual(self.sage.magic_attack, initial_stats["magic_attack"] + 100)
```

このテストでは：
- 呪文使用時のMP消費
- 対象へのダメージ処理
- 呪文の効果（ダメージ、回復、状態変化）
を確認します。

### 3. スライムタイプのテスト（TestSlimeTypes）

```python
def test_metal_slime_properties(self):
    """メタルスライムの特性テスト"""
    metal = MetalSlime()
    self.assertEqual(metal.defense, 255)  # 高防御力
    self.assertEqual(metal.exp, 500)  # 高経験値
    self.assertEqual(metal.color, "銀")

def test_poison_slime_properties(self):
    """毒スライムの特性テスト"""
    poison = PoisonSlime()
    self.assertEqual(poison.color, "紫")
    self.assertEqual(poison.special_ability, "毒攻撃")

def test_king_slime_properties(self):
    """キングスライムの特性テスト"""
    king = KingSlime()
    self.assertTrue(king.hp > BaseSlime().hp)  # 通常より高いHP
    self.assertEqual(king.special_ability, "分裂攻撃")
```

このテストでは：
- 各種スライムの特性確認

### 4. バトルのテスト（TestBattle）

```python
def test_enemy_special_abilities(self):
    """敵の特殊能力テスト"""
    # 毒スライムのテスト
    self.battle.current_enemy = PoisonSlime()
    self.battle.enemy_special_attack()
    self.assertIn("毒", self.player.status_effects)
    
    # キングスライムのテスト
    self.battle.current_enemy = KingSlime()
    initial_hp = self.player.hp
    self.battle.enemy_special_attack()
    self.assertTrue(self.player.hp < initial_hp)  # 分裂攻撃でダメージ

def test_escape_chances(self):
    """逃走確率テスト"""
    # メタルキングスライム（最高逃走率）
    self.battle.current_enemy = MetalKingSlime()
    self.assertEqual(self.battle.get_escape_chance(), 0.9)
    
    # はぐれメタル（高逃走率）
    self.battle.current_enemy = StrayMetal()
    self.assertEqual(self.battle.get_escape_chance(), 0.8)
```

このテストでは：
- 敵の特殊能力テスト
- 逃走確率テスト

### 5. スライムアートのテスト（TestSlimeArt）

```python
def test_get_slime_art(self):
    """スライムのアスキーアート取得テスト"""
    slime = BaseSlime()
    art = self.art.get_slime_art(slime)
    self.assertIsNotNone(art)
    self.assertIsInstance(art, str)
    self.assertTrue(len(art) > 0)

def test_get_slime_color(self):
    """スライムの色情報取得テスト"""
    test_slimes = [
        BaseSlime(),    # 青
        MetalSlime(),   # 銀
        KingSlime(),    # 紫
        StrayMetal()    # 金
    ]
    
    for slime in test_slimes:
        color = self.art.get_slime_color(slime)
        self.assertIsNotNone(color)
        self.assertIsInstance(color, str)
        self.assertTrue(color.startswith("\033["))  # ANSIカラーコードで始まるか
```

このテストでは：
- スライムのアスキーアート生成
- 各種スライムの色情報の取得と形式
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

テスト結果を分かりやすく記録するために、DetailedTestResultクラスを使用してテストレポートを生成します：

```python
def run_tests_with_report():
    # テストスイートの作成
    loader = unittest.TestLoader()
    import test_slime_battle
    suite = loader.loadTestsFromModule(test_slime_battle)

    # テストの実行
    result = DetailedTestResult()
    runner = TextTestRunner(verbosity=2)
    suite.run(result)

    # レポートの生成（Markdown & HTML）
    markdown_report = generate_markdown_report(result)
    html_report = generate_html_report(result)
```

生成されるレポートには以下の情報が含まれます：

1. 実行概要
   - 実行日時
   - 総テスト数
   - 成功/失敗/エラー数

2. テストクラスごとの詳細
   - テスト名
   - テストの説明
   - 実行結果（✅成功/❌失敗）
   - 実行時間
   - エラー詳細（失敗時）

3. 視覚的な表示
   - HTMLレポート：色分けされた結果表示
   - Markdown：絵文字を使用した結果表示

## まとめ

ユニットテストを書くことで：
1. コードの品質を保証
2. バグの早期発見
3. 安全なコード修正
4. 仕様の明確化
が可能になります。

初めは小さなテストから始めて、徐々にテストケースを増やしていくことをお勧めします。
また、テストレポートを活用することで、テスト結果の管理と共有が容易になります。 
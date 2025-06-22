# スライムバトルゲーム解説

このドキュメントでは、Pythonで作成されたドラゴンクエスト風のスライムバトルゲームの実装について解説します。

## 目次
1. [ゲーム概要](#ゲーム概要)
2. [モジュール構成](#モジュール構成)
3. [クラス構造](#クラス構造)
4. [ゲームの機能](#ゲームの機能)
5. [コードの詳細解説](#コードの詳細解説)
6. [テスト機能](#テスト機能)
7. [学習ポイント](#学習ポイント)
8. [発展課題](#発展課題)

## ゲーム概要

このゲームは、プレイヤーが賢者となってさまざまな種類のスライムと戦うRPG風のバトルゲームです。
以下のような特徴があります：

- ターン制バトルシステム
- 多様なスライム（通常、メタル、キング、ポイズンなど）
- 豊富な呪文システム
- レベルアップによる成長要素
- ASCIIアートによるビジュアル表現
- カラー表示対応
- 状態異常システム
- 自動テスト機能

## モジュール構成

### モジュールの依存関係

```
[Module] slime_battle.py（スライムバトルメイン）
    ├── [Module] slime.py（スライム関連）
    │   └── [Class] EnemyCharacter（敵キャラクター）
    │       └── [Class] BaseSlime（基本スライム）
    │           ├── [Class] MetalSlime（メタルスライム）
    │           ├── [Class] StrayMetal（はぐれメタル）
    │           ├── [Class] PoisonSlime（毒スライム）
    │           ├── [Class] KingSlime（キングスライム）
    │           └── [Class] MetalKingSlime（メタルキングスライム）
    ├── [Module] hero.py（勇者関連）
    │   ├── [Class] Equipment（装備品基底クラス）
    │   │   ├── [Class] UltimateWeapon（破壊神の杖）
    │   │   ├── [Class] UltimateArmor（賢者のローブ）
    │   │   └── [Class] UltimateAccessory（精霊の首飾り）
    │   └── [Class] AllyCharacter（味方キャラクター）
    │       └── [Class] Sage（賢者）
    ├── [Class] SlimeArt（スライム表示）
    │   ├── [Method] get_slime_art (static)（スライムのアスキーアート取得）
    │   └── [Method] get_slime_color (static)（スライムの色取得）
    └── [Class] Battle（バトル）
        ├── [Instance] player (Sage)（プレイヤー：賢者）
        ├── [Instance] enemies (List[BaseSlime])（敵リスト：スライム）
        ├── [Instance] current_enemy (BaseSlime)（現在の敵）
        ├── [Method] start_battle（バトル開始）
        ├── [Method] player_turn（プレイヤーターン）
        ├── [Method] enemy_turn（敵ターン）
        └── [Method] process_status_effects（状態異常処理）

[Module] test_slime_battle.py（スライムバトルテスト）
    ├── [Test Class] TestSlimeBase（基本スライムテスト）
    ├── [Test Class] TestSage（賢者テスト）
    ├── [Test Class] TestSlimeTypes（スライムタイプテスト）
    ├── [Test Class] TestBattle（バトルテスト）
    └── [Test Class] TestSlimeArt（スライムアートテスト）

[Module] test_report.py（テストレポート）
    ├── [Class] DetailedTestResult（テスト結果詳細）
    ├── [Method] generate_markdown_report（Markdownレポート生成）
    └── [Method] generate_html_report（HTMLレポート生成）
```

### ファイル構成と役割

1. **slime_battle.py**
   - メインゲームロジック
   - バトルシステムの実装
   - ユーザーインターフェース
   - スライムのビジュアル表現

2. **slime.py**
   - 敵キャラクターの基底クラス
   - スライムの基底クラスと派生クラス
   - 各スライムの特性定義
   - 特殊能力の実装

3. **hero.py**
   - 味方キャラクターの基底クラス
   - プレイヤーキャラクター（賢者）の実装
   - 呪文システム
   - レベルアップ機能

4. **test_slime_battle.py**
   - ユニットテスト
   - 各機能の動作確認
   - 自動テスト

5. **test_report.py**
   - テスト結果のレポート生成
   - HTML/Markdown形式の出力
   - テスト実行の詳細記録

## クラス構造

### 1. EnemyCharacter クラス（敵の基底クラス）
```python
class EnemyCharacter:
    def __init__(self):
        self.hp = 1
        self.max_hp = 1
        self.attack = 1
        self.defense = 1
        self.name = "敵キャラクター"
        self.exp = 0
        self.gold = 0
        self.type = "未設定"
        self.weakness = None
        self.resistance = None
        self.status_effects = []

    def take_damage(self, damage):
        """ダメージを受ける処理"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0  # True if defeated
```

### 2. BaseSlime クラス（スライムの基底クラス）
```python
class BaseSlime(EnemyCharacter):
    def __init__(self):
        super().__init__()
        self.hp = 10
        self.max_hp = 10
        self.attack = 5
        self.defense = 3
        self.name = "スライム"
        self.color = "青"
        self.special_ability = None
        self.exp = 1
        self.gold = 1
        self.type = "スライム系"
        self.weakness = "火"
        self.resistance = "水"
```

### 3. SlimeArt クラス
```python
class SlimeArt:
    @staticmethod
    def get_slime_art(slime):
        """スライムの種類に応じたASCIIアートを返す"""
        base_art = """
         ／￣￣＼
       ／   ●   ●＼
     ｜      ∇      ｜
       ＼＿＿＿／
         ／   ＼
       （＿＿＿）
"""
        metal_art = """
         ／￣￣＼
       ／   ◎   ◎＼
     ｜      ∇      ｜
       ＼＿★＿／
         ／   ＼
       （＿＿＿）
"""
        metal_king_art = """
         ／￣👑￣＼
       ／   ◎   ◎＼
     ｜      ∇      ｜
       ＼＿★＿／
         ／   ＼
       （＿＿＿）
"""
        king_art = """
         ／￣👑￣＼
       ／   ●   ●＼
     ｜      ∇      ｜
       ＼＿♔＿／
         ／   ＼
       （＿＿＿）
"""
        poison_art = """
         ／￣￣＼
       ／   ◉   ◉＼
     ｜      ☠      ｜
       ＼＿∿＿／
         ／   ＼
       （＿＿＿）
"""
        # スライムの種類に応じたアートを返す
        if isinstance(slime, MetalKingSlime):
            return metal_king_art  # メタルキングスライムは👑付き
        elif isinstance(slime, (MetalSlime, StrayMetal)):
            return metal_art       # メタルスライムとはぐれメタルは通常のメタル
        elif isinstance(slime, KingSlime):
            return king_art       # キングスライムは👑付き
        elif isinstance(slime, PoisonSlime):
            return poison_art     # 毒スライムは☠付き
        else:
            return base_art      # 通常スライム

    @staticmethod
    def get_slime_color(slime):
        """スライムの色に応じたカラーコードを返す"""
        color_map = {
            "青": "\033[94m",  # 青
            "銀": "\033[37m",  # 銀（白）
            "金": "\033[93m",  # 金（黄）
            "紫": "\033[95m",  # 紫
        }
        reset = "\033[0m"
        return color_map.get(slime.color, "") + "{}" + reset
```

### 4. Battle クラス
```python
class Battle:
    def __init__(self, player, test_mode=False):
        self.player = player
        self.enemies = [
            BaseSlime(),
            MetalSlime(),
            MetalKing(),
            PoisonSlime(),
            KingSlime(),
            MetalKingSlime()
        ]
        self.current_enemy = None
        self.turn_count = 0
        self.test_mode = test_mode
```

### 5. Sage クラス（賢者）
```python
class Sage(AllyCharacter):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.job = "賢者"
        self.level = 1
        self.hp = 80
        self.max_hp = 80
        self.mp = 100
        self.max_mp = 100
        self.attack = 15
        self.defense = 10
        self.magic_attack = 25
        self.magic_defense = 20
        self.spells = ["ホイミ", "メラ"]  # 初期呪文
```

## ゲームの機能

### 1. 戦闘システム

#### バトルの初期化と進行
```python
def start_battle(self, auto_action=None):
    self.turn_count = 0
    self.current_enemy = random.choice(self.enemies)
    # 敵の情報表示
    # バトル状況の表示
    
    if not self.test_mode:
        # 通常のバトルループ
        while True:
            self.turn_count += 1
            if not self.player_turn():
                break
            if not self.enemy_turn():
                break
            self.process_status_effects()
            self.show_battle_status()
    elif auto_action is not None:
        # テストモード：1ターンだけ実行
        self.turn_count += 1
        if auto_action == 1:
            return self.player_attack()
        elif auto_action == 2:
            return self.player_cast_spell()
        elif auto_action == 3:
            return self.try_escape()
```

#### ダメージ計算
1. 物理攻撃
   ```python
   damage = max(1, attacker.attack - defender.defense // 2)
   ```

2. 魔法攻撃
   ```python
   spell_damage = {
       "メラ": 30,
       "メラミ": 70,
       "メラゾーマ": 150
   }
   # 弱点時は2倍
   if target.weakness == "火":
       damage *= 2
   ```

### 2. 呪文システム

#### 呪文の種類と効果
1. 攻撃呪文
   | 呪文名 | 消費MP | 効果 | 特記事項 |
   |--------|---------|------|----------|
   | メラ | 5 | 30ダメージ | 火属性 |
   | メラミ | 12 | 70ダメージ | 火属性 |
   | メラゾーマ | 25 | 150ダメージ | 火属性 |

2. 回復呪文
   | 呪文名 | 消費MP | 効果 | 特記事項 |
   |--------|---------|------|----------|
   | ホイミ | 4 | 30回復 | - |
   | ベホイミ | 10 | 75回復 | - |
   | ベホマ | 20 | 200回復 | - |

3. 補助呪文
   | 呪文名 | 消費MP | 効果 | 持続時間 |
   |--------|---------|------|----------|
   | バイキルト | 15 | 攻撃力2倍 | 3ターン |
   | マホカンタ | 30 | 魔法反射 | 3ターン |
   | ルーラ | 8 | 逃走成功率UP | 即時 |
   | ザオラル | 50 | 復活 | 即時 |

### 3. 状態異常システム

#### 実装されている状態異常
1. 毒
   ```python
   if "毒" in self.status_effects:
       poison_damage = max(1, self.max_hp // 10)
       self.hp -= poison_damage
   ```

### 4. レベルアップシステム

#### 経験値計算
```python
def get_next_level_exp(self):
    base = 100
    multiplier = 1.5
    return int(base * (multiplier ** (self.level - 1)))
```

#### ステータス成長（賢者）
```python
def level_up(self):
    self.level += 1
    self.max_hp += 5
    self.hp = self.max_hp
    self.max_mp += 8
    self.mp = self.max_mp
    self.attack += 2
    self.defense += 2
    self.magic_attack += 3
    self.magic_defense += 2
```

### 5. 装備システム

#### 装備品の基底クラス
```python
class Equipment:
    def __init__(self, name, equipment_type, stats):
        self.name = name
        self.equipment_type = equipment_type  # "武器", "防具", "装飾品"
        self.stats = stats  # 装備品のステータス変更値を辞書で保持
```

#### 装備の種類と効果
1. 武器（破壊神の杖）
```python
class UltimateWeapon(Equipment):
    def __init__(self):
        super().__init__(
            name="破壊神の杖",
            equipment_type="武器",
            stats={
                "attack": 50,
                "magic_attack": 100,
                "mp": 50
            }
        )
```

2. 防具（賢者のローブ）
```python
class UltimateArmor(Equipment):
    def __init__(self):
        super().__init__(
            name="賢者のローブ",
            equipment_type="防具",
            stats={
                "defense": 45,
                "magic_defense": 65,
                "hp": 100
            }
        )
```

3. 装飾品（精霊の首飾り）
```python
class UltimateAccessory(Equipment):
    def __init__(self):
        super().__init__(
            name="精霊の首飾り",
            equipment_type="装飾品",
            stats={
                "mp": 100,
                "magic_attack": 30,
                "magic_defense": 30
            }
        )
```

#### 装備の着用と効果
```python
def equip(self, equipment):
    """装備を着用し、ステータスを更新する"""
    if equipment.equipment_type not in self.equipment:
        return f"その装備品は装備できない！"

    # 既存の装備を外す
    old_equipment = self.equipment[equipment.equipment_type]
    if old_equipment:
        for stat, value in old_equipment.stats.items():
            if stat == "hp":
                self.max_hp -= value
                self.hp = min(self.hp, self.max_hp)
            elif stat == "mp":
                self.max_mp -= value
                self.mp = min(self.mp, self.max_mp)
            else:
                setattr(self, stat, getattr(self, stat) - value)

    # 新しい装備を付ける
    self.equipment[equipment.equipment_type] = equipment
    for stat, value in equipment.stats.items():
        if stat == "hp":
            self.max_hp += value
            self.hp = min(self.hp, self.max_hp)
        elif stat == "mp":
            self.max_mp += value
            self.mp = min(self.mp, self.max_mp)
        else:
            setattr(self, stat, getattr(self, stat) + value)

    return f"{equipment.name}を装備した！"
```

#### 装備のテスト
```python
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
    self.assertEqual(self.sage.equipment["武器"], weapon)
    self.assertEqual(self.sage.attack, initial_stats["attack"] + 50)
    self.assertEqual(self.sage.magic_attack, initial_stats["magic_attack"] + 100)
    self.assertEqual(self.sage.max_mp, initial_stats["mp"] + 50)
    
    # 最強防具の装備テスト
    armor = UltimateArmor()
    self.sage.equip(armor)
    self.assertEqual(self.sage.equipment["防具"], armor)
    self.assertEqual(self.sage.defense, initial_stats["defense"] + 45)
    self.assertEqual(self.sage.magic_defense, initial_stats["magic_defense"] + 65)
    self.assertEqual(self.sage.max_hp, initial_stats["hp"] + 100)
    
    # 最強装飾品の装備テスト
    accessory = UltimateAccessory()
    self.sage.equip(accessory)
    self.assertEqual(self.sage.equipment["装飾品"], accessory)
    self.assertEqual(self.sage.max_mp, initial_stats["mp"] + 50 + 100)  # 武器とアクセサリーのMP合計
    self.assertEqual(self.sage.magic_attack, initial_stats["magic_attack"] + 100 + 30)  # 武器とアクセサリーの魔力合計
    self.assertEqual(self.sage.magic_defense, initial_stats["magic_defense"] + 65 + 30)  # 防具とアクセサリーの魔法防御合計
```

## テスト機能

### 1. テストケース一覧

1. **TestSlimeBase**
   - test_slime_initialization: 基本スライムの初期化テスト
   - test_slime_take_damage: ダメージ計算のテスト

2. **TestSage**
   - test_sage_initialization: 賢者の初期化テスト
   - test_level_up: レベルアップ時のステータス上昇テスト
   - test_spell_casting: 呪文詠唱テスト
   - test_spell_learning_on_level_up: レベルアップ時の呪文習得テスト
   - test_equipment: 装備システムのテスト

3. **TestSlimeTypes**
   - test_metal_slime_properties: メタルスライムの特性テスト
   - test_stray_metal_properties: はぐれメタルの特性テスト
   - test_poison_slime_properties: 毒スライムの特性テスト
   - test_king_slime_properties: キングスライムの特性テスト
   - test_metal_king_properties: メタルキングスライムの特性テスト

4. **TestBattle**
   - test_battle_initialization: バトル初期化テスト
   - test_battle_first_turn: 最初のターンのテスト
   - test_status_effects: 状態異常の処理テスト
   - test_enemy_special_abilities: 敵の特殊能力テスト
   - test_escape_chances: 逃走確率テスト

5. **TestSlimeArt**
   - test_get_slime_art: スライムのアスキーアート取得テスト
   - test_get_slime_color: スライムの色情報取得テスト

## 学習ポイント

### 1. オブジェクト指向プログラミング
- クラスとインスタンス
- 継承と多態性
- カプセル化
- メソッドのオーバーライド

### 2. Pythonの基本機能
- 条件分岐（if文）
- 繰り返し処理（while文）
- リスト操作
- 例外処理
- 文字列フォーマット
- 静的メソッド

### 3. ゲームプログラミングの基礎
- ターン制システムの実装
- キャラクターステータスの管理
- 戦闘システムの設計
- ユーザー入力の処理
- ゲームバランスの調整

### 4. テスト駆動開発
- ユニットテストの作成
- テストケースの設計
- テスト結果の可視化
- 自動テストの実行

## 発展課題

1. 機能拡張のアイデア
   - セーブ/ロードシステムの実装
   - 装備システムの追加
   - より多様な敵キャラクターの追加
   - 戦闘アニメーションの実装
   - BGMや効果音の追加

2. コード改善のポイント
   - さらなるユニットテストの追加
   - コンフィグファイルの導入
   - ロギングシステムの実装
   - パフォーマンス最適化
   - 国際化対応

3. 学習の次のステップ
   - データベースとの連携
   - GUIフレームワークの導入
   - ネットワーク対戦の実装
   - AIの導入
   - デザインパターンの適用

## まとめ

このゲームは、Pythonプログラミングの学習に最適な教材です。
基本的なプログラミング概念から、より高度なオブジェクト指向プログラミング、
そしてテスト駆動開発まで、様々な要素を実践的に学ぶことができます。

また、このコードをベースに機能を拡張することで、
より深いプログラミングの理解と実践的なスキルを身につけることができます。 
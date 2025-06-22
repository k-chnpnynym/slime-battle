import unittest
from slime import BaseSlime, MetalSlime, StrayMetal, PoisonSlime, KingSlime, MetalKingSlime
from hero import Sage, UltimateWeapon, UltimateArmor, UltimateAccessory
from slime_battle import Battle, SlimeArt

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

class TestSage(unittest.TestCase):
    def setUp(self):
        """各テストケース実行前の準備"""
        self.sage = Sage("テストプレイヤー")
        
    def test_sage_initialization(self):
        """賢者の初期化テスト"""
        self.assertEqual(self.sage.name, "テストプレイヤー")
        self.assertIsNotNone(self.sage.hp)
        self.assertIsNotNone(self.sage.mp)
        self.assertTrue(len(self.sage.spells) > 0)

    def test_level_up(self):
        """レベルアップ時のステータス上昇テスト"""
        initial_hp = self.sage.max_hp
        initial_mp = self.sage.max_mp
        initial_attack = self.sage.attack
        
        self.sage.level_up()
        
        self.assertTrue(self.sage.max_hp > initial_hp)
        self.assertTrue(self.sage.max_mp > initial_mp)
        self.assertTrue(self.sage.attack > initial_attack)

    def test_spell_casting(self):
        """呪文詠唱テスト"""
        target = BaseSlime()
        initial_mp = self.sage.mp
        
        # メラの詠唱テスト
        self.sage.cast_spell("メラ", target)
        self.assertTrue(self.sage.mp < initial_mp)  # MPが消費されているか
        self.assertTrue(target.hp < target.max_hp)  # ダメージが入っているか

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
        
        # レベル7での呪文習得テスト
        while self.sage.level < 7:
            self.sage.level_up()
        self.assertIn("ルーラ", self.sage.spells)

    def test_all_spell_effects(self):
        """全呪文の効果テスト"""
        target = BaseSlime()
        target.hp = target.max_hp
        
        # 回復呪文のテスト
        self.sage.hp = 1  # HPを減らす
        self.sage.cast_spell("ホイミ", self.sage)
        self.assertTrue(self.sage.hp > 1)  # 回復されているか
        
        # 攻撃呪文のテスト（弱点あり）
        target.weakness = "火"  # 火属性弱点
        initial_hp = target.hp
        self.sage.cast_spell("メラ", target)
        self.assertTrue(target.hp < initial_hp)  # ダメージが入っているか
        
        # MPが足りない場合のテスト
        self.sage.mp = 0
        result = self.sage.cast_spell("メラ", target)
        self.assertTrue("MPが足りない" in result)

class TestSlimeTypes(unittest.TestCase):
    """各スライムタイプのテスト"""
    
    def test_metal_slime_properties(self):
        """メタルスライムの特性テスト"""
        metal = MetalSlime()
        self.assertEqual(metal.defense, 255)  # 高防御力
        self.assertEqual(metal.exp, 500)  # 高経験値
        self.assertEqual(metal.color, "銀")
        
    def test_stray_metal_properties(self):
        """はぐれメタルの特性テスト"""
        stray = StrayMetal()
        self.assertEqual(stray.defense, 255)
        self.assertEqual(stray.exp, 2000)  # 非常に高い経験値
        self.assertTrue("非常に高確率で逃げる" in stray.special_ability)
        
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
        
    def test_metal_king_properties(self):
        """メタルキングスライムの特性テスト"""
        metal_king = MetalKingSlime()
        self.assertEqual(metal_king.defense, 255)
        self.assertEqual(metal_king.exp, 5000)  # 最高の経験値
        self.assertEqual(metal_king.color, "金")

class TestBattle(unittest.TestCase):
    def setUp(self):
        """各テストケース実行前の準備"""
        self.player = Sage("テストプレイヤー")
        self.battle = Battle(self.player, test_mode=True)
        
    def test_battle_initialization(self):
        """バトル初期化テスト"""
        # バトル開始前の状態確認
        self.assertIsNone(self.battle.current_enemy)
        self.assertEqual(self.battle.turn_count, 0)
        
        # バトル開始（アクションなし）
        self.battle.start_battle()
        
        # バトル開始直後の状態確認
        self.assertIsNotNone(self.battle.current_enemy)
        self.assertEqual(self.battle.turn_count, 0)

    def test_battle_first_turn(self):
        """最初のターンのテスト"""
        # バトル開始（逃げるアクション）
        self.battle.start_battle(auto_action=3)
        
        # ターン数の確認
        self.assertEqual(self.battle.turn_count, 1)

    def test_status_effects(self):
        """状態異常の処理テスト"""
        self.player.status_effects.append("毒")
        initial_hp = self.player.hp
        
        self.battle.process_status_effects()
        self.assertTrue(self.player.hp < initial_hp)  # 毒ダメージが入っているか

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
        
        # 通常スライム（逃走しない）
        self.battle.current_enemy = BaseSlime()
        self.assertEqual(self.battle.get_escape_chance(), 0.0)

class TestSlimeArt(unittest.TestCase):
    def setUp(self):
        """各テストケース実行前の準備"""
        self.art = SlimeArt()
        
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
            StrayMetal()     # 金
        ]
        
        for slime in test_slimes:
            color = self.art.get_slime_color(slime)
            self.assertIsNotNone(color)
            self.assertIsInstance(color, str)
            self.assertTrue(color.startswith("\033["))  # ANSIカラーコードで始まるか

if __name__ == '__main__':
    unittest.main() 
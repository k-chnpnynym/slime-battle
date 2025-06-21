import unittest
from slime import BaseSlime, MetalSlime, MetalKing, PoisonSlime, KingSlime, MetalKingSlime
from hero import Sage
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
            MetalKing()     # 金
        ]
        
        for slime in test_slimes:
            color = self.art.get_slime_color(slime)
            self.assertIsNotNone(color)
            self.assertIsInstance(color, str)
            self.assertTrue(color.startswith("\033["))  # ANSIカラーコードで始まるか

if __name__ == '__main__':
    unittest.main() 
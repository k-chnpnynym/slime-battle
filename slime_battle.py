import random
import time
from slime import BaseSlime, MetalSlime, StrayMetal, PoisonSlime, KingSlime, MetalKingSlime
from hero import Sage

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
        
        if isinstance(slime, MetalKingSlime):
            return metal_king_art
        elif isinstance(slime, (MetalSlime, StrayMetal)):
            return metal_art
        elif isinstance(slime, KingSlime):
            return king_art
        elif isinstance(slime, PoisonSlime):
            return poison_art
        else:
            return base_art

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

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.attack = 15
        self.defense = 10
        self.level = 1
        self.exp = 0
        self.status_effects = []

    def get_status(self):
        return {
            "名前": self.name,
            "HP": f"{self.hp}/{self.max_hp}",
            "MP": f"{self.mp}/{self.max_mp}",
            "攻撃力": self.attack,
            "防御力": self.defense,
            "レベル": self.level,
            "経験値": self.exp,
            "状態": self.status_effects
        }

class Battle:
    def __init__(self, player, test_mode=False):
        self.player = player
        self.enemies = [
            BaseSlime(),
            MetalSlime(),
            StrayMetal(),
            PoisonSlime(),
            KingSlime(),
            MetalKingSlime()
        ]
        self.current_enemy = None
        self.turn_count = 0
        self.test_mode = test_mode  # テストモード用フラグ

    def start_battle(self, auto_action=None):
        """バトルを開始する
        
        Args:
            auto_action: テストモード時の自動アクション（1: 攻撃, 2: 呪文, 3: 逃げる）
        """
        self.turn_count = 0  # ターン数を初期化
        self.current_enemy = random.choice(self.enemies)
        print("\n" + "="*50)
        
        # 敵の出現メッセージと情報
        print(f"野生の{self.current_enemy.name}が現れた！")
        print(f"\n【敵の情報】")
        print(f"種類: {self.current_enemy.type}")
        print(f"HP: {self.current_enemy.hp}")
        print(f"攻撃力: {self.current_enemy.attack}")
        print(f"防御力: {self.current_enemy.defense}")
        if self.current_enemy.special_ability:
            print(f"特殊能力: {self.current_enemy.special_ability}")
        print(f"弱点: {self.current_enemy.weakness}")
        print(f"耐性: {self.current_enemy.resistance}")
        
        # スライムのアスキーアート表示
        art = SlimeArt.get_slime_art(self.current_enemy)
        color_format = SlimeArt.get_slime_color(self.current_enemy)
        print(color_format.format(art))
        
        self.show_battle_status()
        
        if not self.test_mode:
            # 通常のバトルループ
            while True:
                self.turn_count += 1
                print("\n" + "-"*20 + f" ターン {self.turn_count} " + "-"*20)
                
                if not self.player_turn():
                    break
                
                if not self.enemy_turn():
                    break
                
                self.process_status_effects()
                self.show_battle_status()
        elif auto_action is not None:
            # テストモード：1ターンだけ実行
            self.turn_count += 1
            print("\n" + "-"*20 + f" ターン {self.turn_count} " + "-"*20)
            
            if auto_action == 1:
                return self.player_attack()
            elif auto_action == 2:
                return self.player_cast_spell()
            elif auto_action == 3:
                return self.try_escape()

    def player_turn(self):
        """プレイヤーのターン処理"""
        print("\nあなたのターン！")
        print("1: 攻撃")
        print("2: 呪文")
        print("3: 逃げる")
        
        if self.test_mode:
            # テストモード時は入力をスキップ
            return True
            
        while True:
            try:
                choice = int(input("行動を選択してください (1-3): "))
                if 1 <= choice <= 3:
                    break
            except ValueError:
                pass
            print("無効な選択です。1から3の数字を入力してください。")

        if choice == 1:
            return self.player_attack()
        elif choice == 2:
            return self.player_cast_spell()
        elif choice == 3:
            return self.try_escape()

    def player_cast_spell(self):
        """呪文選択と使用"""
        print("\n使用可能な呪文:")
        spells = self.player.spells
        for i, spell in enumerate(spells, 1):
            print(f"{i}: {spell}")
        print(f"{len(spells) + 1}: 戻る")

        while True:
            try:
                choice = int(input(f"呪文を選択してください (1-{len(spells) + 1}): "))
                if 1 <= choice <= len(spells) + 1:
                    break
            except ValueError:
                pass
            print("無効な選択です。")

        if choice == len(spells) + 1:
            return self.player_turn()

        selected_spell = spells[choice - 1]
        
        # 攻撃呪文の場合
        if selected_spell in ["メラ", "メラミ", "メラゾーマ"]:
            result = self.player.cast_spell(selected_spell, self.current_enemy)
            print("\n" + result)
            
            # ダメージ計算
            spell_damage = {
                "メラ": 30,
                "メラミ": 70,
                "メラゾーマ": 150
            }
            
            base_damage = spell_damage[selected_spell]
            # 弱点の場合、ダメージ2倍
            if self.current_enemy.weakness == "火":
                base_damage *= 2
                print("効果は抜群だ！")
            
            self.current_enemy.take_damage(base_damage)
            print(f"{self.current_enemy.name}に{base_damage}のダメージ！")
            
            if self.current_enemy.hp <= 0:
                return self.win_battle()
            return True

    def player_attack(self):
        """プレイヤーの通常攻撃"""
        damage = max(1, self.player.attack - self.current_enemy.defense // 2)
        hit_chance = 0.95  # 通常攻撃の命中率

        if random.random() < hit_chance:
            self.current_enemy.hp -= damage
            print(f"\n{self.player.name}の攻撃！")
            print(f"{self.current_enemy.name}に{damage}のダメージ！")
            
            if self.current_enemy.hp <= 0:
                self.win_battle()
                return False
        else:
            print(f"\n{self.player.name}の攻撃！しかし、外れてしまった！")
        
        return True

    def try_escape(self):
        """逃走を試みる"""
        escape_chance = 0.5
        if random.random() < escape_chance:
            print(f"\n{self.player.name}は逃げ出した！")
            return False
        else:
            print("\n逃げ出せなかった！")
        return True

    def enemy_turn(self):
        """敵のターン処理"""
        if random.random() < self.get_escape_chance():
            print(f"\n{self.current_enemy.name}は逃げ出した！")
            self.player.exp += self.current_enemy.exp // 3
            print(f"逃げられてしまった... 経験値を{self.current_enemy.exp // 3}獲得！")
            return False

        # 特殊能力の発動判定
        if self.current_enemy.special_ability and random.random() < 0.3:
            return self.enemy_special_attack()
        else:
            return self.enemy_normal_attack()

    def enemy_normal_attack(self):
        """敵の通常攻撃"""
        damage = max(1, self.current_enemy.attack - self.player.defense // 2)
        self.player.hp -= damage
        print(f"\n{self.current_enemy.name}の攻撃！")
        print(f"{self.player.name}に{damage}のダメージ！")

        if self.player.hp <= 0:
            self.lose_battle()
            return False
        return True

    def enemy_special_attack(self):
        """敵の特殊攻撃"""
        if isinstance(self.current_enemy, PoisonSlime):
            if "毒" not in self.player.status_effects:
                self.player.status_effects.append("毒")
                print(f"\n{self.current_enemy.name}の毒攻撃！")
                print(f"{self.player.name}は毒状態になった！")
        elif isinstance(self.current_enemy, KingSlime):
            damage = max(1, self.current_enemy.attack * 2 - self.player.defense // 2)
            self.player.hp -= damage
            print(f"\n{self.current_enemy.name}の分裂攻撃！")
            print(f"{self.player.name}に{damage}のダメージ！")
        else:
            return self.enemy_normal_attack()

        if self.player.hp <= 0:
            self.lose_battle()
            return False
        return True

    def get_escape_chance(self):
        """敵の逃走確率を取得"""
        if isinstance(self.current_enemy, MetalKingSlime):
            return 0.9
        elif isinstance(self.current_enemy, StrayMetal):
            return 0.8
        elif isinstance(self.current_enemy, MetalSlime):
            return 0.7
        return 0.0

    def process_status_effects(self):
        """状態異常の処理"""
        if "毒" in self.player.status_effects:
            poison_damage = max(1, self.player.max_hp // 10)
            self.player.hp -= poison_damage
            print(f"\n毒のダメージ！{self.player.name}に{poison_damage}のダメージ！")
            
            if self.player.hp <= 0:
                self.lose_battle()
                return False
        return True

    def win_battle(self):
        """勝利時の処理"""
        print(f"\n{self.current_enemy.name}を倒した！")
        exp_gained = self.current_enemy.exp
        gold_gained = self.current_enemy.gold
        self.player.exp += exp_gained
        print(f"経験値を{exp_gained}獲得！")
        print(f"ゴールドを{gold_gained}獲得！")
        
        # レベルアップ判定
        while self.player.exp >= self.player.get_next_level_exp():
            self.level_up()

    def lose_battle(self):
        """敗北時の処理"""
        print(f"\n{self.player.name}は力尽きた...")
        print("ゲームオーバー")

    def get_next_level_exp(self):
        """次のレベルに必要な経験値を計算"""
        return self.player.level * 100

    def level_up(self):
        """レベルアップ処理"""
        self.player.level_up()
        print(f"\nレベルアップ！ {self.player.level}になった！")
        print("ステータスが上昇した！")

    def show_battle_status(self):
        """バトル状況の表示"""
        print("\n" + "="*50)
        print(f"【{self.player.name}】")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"MP: {self.player.mp}/{self.player.max_mp}")
        if self.player.status_effects:
            print(f"状態: {', '.join(self.player.status_effects)}")
        
        print(f"\n【{self.current_enemy.name}】")
        print(f"HP: {self.current_enemy.hp}")
        
        # スライムのアスキーアート表示（簡易版）
        art = SlimeArt.get_slime_art(self.current_enemy)
        color_format = SlimeArt.get_slime_color(self.current_enemy)
        print(color_format.format(art))
        
        print("="*50)

def main():
    print("スライムバトル！")
    player_name = input("あなたの名前を入力してください: ")
    player = Sage(player_name)  # プレイヤーは賢者として開始
    
    while True:
        battle = Battle(player)
        battle.start_battle()
        
        if player.hp <= 0:
            break
            
        print("\n1: 続ける")
        print("2: 終了")
        try:
            choice = int(input("選択してください (1-2): "))
            if choice == 2:
                break
        except ValueError:
            pass

if __name__ == "__main__":
    main() 
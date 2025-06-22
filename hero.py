class Equipment:
    def __init__(self, name, equipment_type, stats):
        self.name = name
        self.equipment_type = equipment_type  # "武器", "防具", "装飾品"
        self.stats = stats  # 装備品のステータス変更値を辞書で保持

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

class AllyCharacter:
    def __init__(self):
        self.hp = 1
        self.max_hp = 1
        self.mp = 1
        self.max_mp = 1
        self.attack = 1
        self.defense = 1
        self.name = "味方キャラクター"
        self.exp = 0
        self.level = 1
        self.job = "未設定"
        self.magic_attack = 1
        self.magic_defense = 1
        self.spells = []
        self.status_effects = []  # 状態異常を管理するリストを追加
        self.equipment = {
            "武器": None,
            "防具": None,
            "装飾品": None
        }

    def get_status(self):
        return {
            "名前": self.name,
            "職業": self.job,
            "レベル": self.level,
            "HP": f"{self.hp}/{self.max_hp}",
            "MP": f"{self.mp}/{self.max_mp}",
            "攻撃力": self.attack,
            "防御力": self.defense,
            "魔力": self.magic_attack,
            "魔法防御": self.magic_defense,
            "経験値": self.exp,
            "使用可能な呪文": self.spells,
            "武器": self.equipment["武器"].name if self.equipment["武器"] else "なし",
            "防具": self.equipment["防具"].name if self.equipment["防具"] else "なし",
            "装飾品": self.equipment["装飾品"].name if self.equipment["装飾品"] else "なし"
        }

    def level_up(self):
        """レベルアップ時のステータス上昇"""
        self.level += 1
        self.max_hp += 5
        self.hp = self.max_hp
        self.max_mp += 3
        self.mp = self.max_mp
        self.attack += 2
        self.defense += 2
        self.magic_attack += 2
        self.magic_defense += 2

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
        self.status_effects = []
        self.equipment = {
            "武器": None,
            "防具": None,
            "装飾品": None
        }

    def level_up(self):
        """レベルアップ時のステータス上昇と新しい呪文の習得"""
        self.level += 1
        self.max_hp += 5
        self.hp = self.max_hp
        self.max_mp += 8
        self.mp = self.max_mp
        self.attack += 2
        self.defense += 2
        self.magic_attack += 3
        self.magic_defense += 2

        # 新しい呪文の習得（重複を防ぐ）
        new_spells = []
        if self.level == 3:
            new_spells = ["ベホイミ", "メラミ"]
        elif self.level == 5:
            new_spells = ["ベホマ", "メラゾーマ"]
        elif self.level == 7:
            new_spells = ["ルーラ"]
        elif self.level == 10:
            new_spells = ["バイキルト", "マホカンタ"]
        elif self.level == 15:
            new_spells = ["ザオラル"]

        # 重複を防いで追加
        for spell in new_spells:
            if spell not in self.spells:
                self.spells.append(spell)

    def get_next_level_exp(self):
        """次のレベルに必要な経験値を計算"""
        base = 100
        multiplier = 1.5
        return int(base * (multiplier ** (self.level - 1)))

    def cast_spell(self, spell_name, target=None):
        """呪文を使用する"""
        spell_costs = {
            "ホイミ": 4,
            "ベホイミ": 10,
            "ベホマ": 20,
            "メラ": 5,
            "メラミ": 12,
            "メラゾーマ": 25,
            "ルーラ": 8,
            "バイキルト": 15,
            "マホカンタ": 30,
            "ザオラル": 50
        }

        spell_damage = {
            "メラ": 30,
            "メラミ": 70,
            "メラゾーマ": 150
        }

        if spell_name not in self.spells:
            return f"{self.name}は{spell_name}を使えない！"
        
        cost = spell_costs.get(spell_name, 0)
        if self.mp < cost:
            return f"MPが足りない！ あと{cost - self.mp}必要"

        self.mp -= cost
        
        # 呪文の効果
        if spell_name == "ホイミ":
            heal = 30
            if target:
                target.hp = min(target.max_hp, target.hp + heal)
            return f"{target.name if target else self.name}のHPが{heal}回復した！"
        
        elif spell_name == "ベホイミ":
            heal = 75
            if target:
                target.hp = min(target.max_hp, target.hp + heal)
            return f"{target.name if target else self.name}のHPが{heal}回復した！"
        
        elif spell_name == "ベホマ":
            heal = 200
            if target:
                target.hp = min(target.max_hp, target.hp + heal)
            return f"{target.name if target else self.name}のHPが{heal}回復した！"
        
        elif spell_name in ["メラ", "メラミ", "メラゾーマ"]:
            if target:
                damage = spell_damage[spell_name]
                target.take_damage(damage)
            return f"{self.name}は{spell_name}を唱えた！\n炎のダメージ（{'小' if spell_name == 'メラ' else '中' if spell_name == 'メラミ' else '大'}）"
        
        elif spell_name == "ルーラ":
            return f"{self.name}はルーラを唱えた！\n好きな場所に移動できる！"
        
        elif spell_name == "バイキルト":
            if target:
                target.attack *= 2
            return f"{target.name if target else self.name}の攻撃力が2倍になった！"
        
        elif spell_name == "マホカンタ":
            return f"{self.name}は魔法を跳ね返すバリアを張った！"
        
        elif spell_name == "ザオラル":
            return f"{self.name}は復活の呪文を唱えた！"


if __name__ == "__main__":
    # 賢者のインスタンスを作成してテスト
    sage = Sage("てるた")
    
    # 最強装備を作成
    ultimate_weapon = UltimateWeapon()
    ultimate_armor = UltimateArmor()
    ultimate_accessory = UltimateAccessory()
    
    print("【初期ステータス】")
    status = sage.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # 最強装備を装着
    print("\n【最強装備装着】")
    print(sage.equip(ultimate_weapon))
    print(sage.equip(ultimate_armor))
    print(sage.equip(ultimate_accessory))
    
    print("\n【最終ステータス】")
    status = sage.get_status()
    for key, value in status.items():
        print(f"{key}: {value}") 
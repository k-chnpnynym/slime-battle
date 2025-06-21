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
            "装備": self.equipment
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
    
    # ステータスを表示
    print("【初期ステータス】")
    status = sage.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # 呪文を使ってみる
    print("\n【呪文テスト】")
    print(sage.cast_spell("ホイミ"))
    print(f"残りMP: {sage.mp}/{sage.max_mp}")
    
    print("\nメラを使用")
    print(sage.cast_spell("メラ"))
    print(f"残りMP: {sage.mp}/{sage.max_mp}")
    
    # レベルアップのテスト
    print("\n【レベルアップテスト】")
    for _ in range(5):
        sage.level_up()
    print(f"レベル{sage.level}になった！")
    status = sage.get_status()
    for key, value in status.items():
        print(f"{key}: {value}") 
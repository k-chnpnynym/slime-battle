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

    def get_status(self):
        return {
            "名前": self.name,
            "タイプ": self.type,
            "HP": f"{self.hp}/{self.max_hp}",
            "攻撃力": self.attack,
            "防御力": self.defense,
            "弱点": self.weakness,
            "耐性": self.resistance,
            "経験値": self.exp,
            "ゴールド": self.gold
        }


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


class MetalSlime(BaseSlime):
    def __init__(self):
        super().__init__()
        self.name = "メタルスライム"
        self.color = "銀"
        self.hp = 4
        self.max_hp = 4
        self.attack = 5
        self.defense = 255
        self.special_ability = "高確率で逃げる"
        self.exp = 500
        self.gold = 6
        self.weakness = "火"
        self.resistance = "水"


class StrayMetal(BaseSlime):
    def __init__(self):
        super().__init__()
        self.name = "はぐれメタル"
        self.color = "銀"
        self.hp = 6
        self.attack = 5
        self.defense = 255
        self.special_ability = "非常に高確率で逃げる"
        self.exp = 2000
        self.gold = 15
        self.weakness = "火"
        self.resistance = "水"


class PoisonSlime(BaseSlime):
    def __init__(self):
        super().__init__()
        self.name = "ポイズンスライム"
        self.color = "紫"
        self.hp = 15
        self.attack = 8
        self.special_ability = "毒攻撃"
        self.exp = 5
        self.gold = 4


class KingSlime(BaseSlime):
    def __init__(self):
        super().__init__()
        self.name = "キングスライム"
        self.color = "青"
        self.hp = 30
        self.attack = 15
        self.defense = 8
        self.special_ability = "分裂攻撃"
        self.exp = 28
        self.gold = 15


class MetalKingSlime(BaseSlime):
    def __init__(self):
        super().__init__()
        self.name = "メタルキングスライム"
        self.color = "金"
        self.hp = 8
        self.attack = 10
        self.defense = 255
        self.special_ability = "非常に高確率で逃げる"
        self.exp = 5000
        self.gold = 30
        self.weakness = "火"
        self.resistance = "水"


if __name__ == "__main__":
    # 各スライムのインスタンスを作成
    normal_slime = BaseSlime()
    metal_slime = MetalSlime()
    stray_metal = StrayMetal()
    poison_slime = PoisonSlime()
    king_slime = KingSlime()
    metal_king_slime = MetalKingSlime()

    # 各スライムの情報を表示
    slimes = [normal_slime, metal_slime, stray_metal, poison_slime, king_slime, metal_king_slime]
    
    for slime in slimes:
        status = slime.get_status()
        print(f"\n{status['名前']}の情報:")
        for key, value in status.items():
            if key != "名前":  # 名前は既に表示したのでスキップ
                print(f"{key}: {value}")
        # 色は EnemyCharacter には無い特別な属性なので個別に表示
        print(f"色: {slime.color}")
        if slime.special_ability:
            print(f"特殊能力: {slime.special_ability}") 
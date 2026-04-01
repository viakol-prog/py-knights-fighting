from typing import Dict, Any


class Knight:
    def __init__(self, config_dict: Dict[str, Any]) -> None:
        self.name = config_dict.get("name")
        self.hp = config_dict.get("hp", 100)
        self.power = config_dict.get("power", 0)
        self.protection = config_dict.get("protection", 0)
        self.weapon = config_dict.get("weapon")
        self.armour = config_dict.get("armour", [])
        self.potion = config_dict.get("potion")
        self._base_hp = self.hp
        self._base_power = self.power
        self._base_protection = self.protection
        self._prepared = False

    def prepare(self) -> None:
        """Merges all stats from gear and potions once."""
        if self._prepared:
            return

        effect = (self.potion or {}).get("effect", {})
        weapon_power = (self.weapon or {}).get("power", 0)
        armour_protection = sum(p.get("protection", 0) for p in self.armour)

        # Calculate final stats
        self.hp = self._base_hp + self._to_num(effect.get("hp", 0))
        self.power = (self._base_power + weapon_power
                      + self._to_num(effect.get("power", 0)))
        self.protection = (self._base_protection + armour_protection
                           + self._to_num(effect.get("protection", 0)))

        self._prepared = True

    @staticmethod
    def _to_num(value: Any) -> int | float:
        return value if isinstance(value, (int, float)) else 0

    def take_damage(self, opponent_power: int) -> None:
        damage = max(opponent_power - self.protection, 0)
        self.hp = max(self.hp - damage, 0)

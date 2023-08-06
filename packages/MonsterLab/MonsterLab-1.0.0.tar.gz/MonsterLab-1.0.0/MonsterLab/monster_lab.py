import datetime
from .monster_data import Random


class Monster:

    def __init__(self, name=None, monster_type=None, level=None, rank=None):
        self.type = monster_type or Random.random_type()
        self.name = name or Random.random_name(self.type)
        self.level = level or Random.random_level()
        self.rank = rank or Random.random_rank()
        self.damage = f"{self.level}d{Random.dice_lookup[self.rank]}"
        self.time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.health = Random.resource(self.level, self.rank)
        self.energy = Random.resource(self.level, self.rank)
        self.sanity = Random.resource(self.level, self.rank)

    def to_dict(self):
        return {
            "Name": self.name,
            "Type": self.type,
            "Level": self.level,
            "Rarity": self.rank,
            "Damage": self.damage,
            "Health": self.health,
            "Energy": self.energy,
            "Sanity": self.sanity,
            "Time Stamp": self.time_stamp,
        }

    def __repr__(self):
        output = (f"{key}: {val}" for key, val in self.to_dict().items())
        return "\n".join(output)

    def __str__(self):
        return self.__repr__() + "\n"


if __name__ == '__main__':
    for _ in range(50):
        print(Monster())

from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1,
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        # super().__init__()
        self.base = base

    @abstractmethod
    def get_stats(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects().copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects().copy()


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_negative_effects(self):
        pass


class Berserk(AbstractPositive):
    stats_change = {
        "HP": +50,

        "Strength": +7,
        "Endurance": +7,
        "Agility": +7,
        "Luck": +7,

        "Perception": -3,
        "Charisma": -3,
        "Intelligence": -3,
    }

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Berserk")
        return positive_effects.copy()

    def get_stats(self):
        stats = self.base.get_stats()
        for stat, change in self.stats_change.items():
            stats[stat] += change
        return stats.copy()


class Blessing(AbstractPositive):
    stats_change = {
        "Strength": +2,
        "Perception": +2,
        "Endurance": +2,
        "Charisma": +2,
        "Intelligence": +2,
        "Agility": +2,
        "Luck": +2,
    }

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append("Blessing")
        return positive_effects.copy()

    def get_stats(self):
        stats = self.base.get_stats()
        for stat, change in self.stats_change.items():
            stats[stat] += change
        return stats.copy()


class Weakness(AbstractNegative):
    stats_change = {
        "Strength": -4,
        "Endurance": -4,
        "Agility": -4,
    }

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Weakness")
        return negative_effects.copy()

    def get_stats(self):
        stats = self.base.get_stats()
        for stat, change in self.stats_change.items():
            stats[stat] += change
        return stats.copy()


class EvilEye(AbstractNegative):
    stats_change = {
        "Luck": -10,
    }

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("EvilEye")
        return negative_effects.copy()

    def get_stats(self):
        stats = self.base.get_stats()
        for stat, change in self.stats_change.items():
            stats[stat] += change
        return stats.copy()


class Curse(AbstractNegative):
    stats_change = {
        "Strength": -2,
        "Perception": -2,
        "Endurance": -2,
        "Charisma": -2,
        "Intelligence": -2,
        "Agility": -2,
        "Luck": -2,
    }

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append("Curse")
        return negative_effects.copy()

    def get_stats(self):
        stats = self.base.get_stats()
        for stat, change in self.stats_change.items():
            stats[stat] += change
        return stats.copy()

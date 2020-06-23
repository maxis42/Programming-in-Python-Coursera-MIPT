from abc import ABC, abstractmethod
import pygame
import random
import Service


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.stats = stats
        self.xp = xp
        self.position = position

    def interact(self, engine, hero):
        enemy_hp = 5 + self.stats["endurance"] * 2

        while enemy_hp > 0 and hero.hp > 0:
            hero_hit = hero.stats["strength"] + random.randint(0, 10)
            enemy_hit = self.stats["strength"]
            if hero_hit > enemy_hit:
                enemy_hp -= 5
            elif hero_hit == enemy_hit:
                continue
            else:
                hero.hp -= 10

        n = hero.level
        if hero.hp > 0:
            hero.exp += self.stats["experience"]
            hero.level_up()
            if hero.level > n:
                engine.notify(f"Level up {hero.level}")
        if hero.hp <= 0:
            hero.hp = 0
            hero.level -= 1
            hero.exp = 0
            engine.notify(f"Level low {hero.level}")
        if hero.level <= 0:
            engine.notify(f"Game Over")
            engine.level = 4
            Service.reload_game(engine, hero)


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

# FIXME
# add classes
class Berserk(Effect):

    def apply_effect(self):
        self.stats["strength"] += 5
        self.stats["endurance"] += 5
        self.stats["intelligence"] -= 5
        return self.stats


class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 3
        self.stats["intelligence"] += 1
        return self.stats


class Weakness(Effect):

    def apply_effect(self):
        self.stats["strength"] -= 2
        self.stats["endurance"] -= 3
        self.stats["intelligence"] += 1
        return self.stats


class Lucky(Effect):

    def apply_effect(self):
        self.stats["luck"] += 5
        return self.stats

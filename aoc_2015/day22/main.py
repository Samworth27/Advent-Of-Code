from aoc_util.inputs import parse_input
import re
from random import choice
DAY = 22
YEAR = 2015


class Character:
    def __init__(self, name, hp, mana, attack, spell_list: list['Spell'], armour=0, effects=None):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.armour = armour
        self.effects = effects if effects else {}
        self.spell_list = spell_list
        self.attack = attack
        self.hard_mode = False

    def effects_tick(self, opponent):
        for effect, time_remaining in [*self.effects.items()]:
            effect(self, opponent)
            time_remaining -= 1
            # print(f"{self.name} effected by {effect.__name__}, {time_remaining} left")
            if time_remaining == 0:
                del self.effects[effect]
                continue
            self.effects[effect] = time_remaining

    def melee_attack(self, opponent):
        opponent.receive_damage(self.attack)

    def add_effect(self, effect, duration):
        self.effects[effect] = duration

    def cast_spell(self, spell: 'Spell', opponent: 'Character'):
        # print(f"{self.name} cast {spell.effect.__name__}")
        self.consume_mana(spell.cost)
        if spell.duration == 0:
            spell.effect(self, opponent)
            return
        if spell.target_self:
            self.add_effect(spell.effect, spell.duration)
        else:
            # print(f"{spell.effect.__name__} given to {opponent.name}")
            opponent.add_effect(spell.effect, spell.duration)

    def castable_spells(self, opponent: 'Character') -> list['Spell']:
        castable = []
        for spell in self.spell_list:
            if self.mana < spell.cost:
                continue
            if spell.target_self:
                if self.has_effect(spell.effect):
                    continue
            else:
                if opponent.has_effect(spell.effect):
                    continue
            castable.append(spell)
        return castable

    def has_effect(self, effect):
        return effect in self.effects

    def receive_damage(self, damage):
        damage = max(1, damage - self.armour)
        # print(f"{self.name} took {damage} damage")
        self.hp -= damage

    def heal(self, amount):
        self.hp += amount

    def consume_mana(self, amount):
        self.mana -= amount

    def generate_mana(self, amount):
        self.mana += amount

    def gain_armour(self, amount):
        self.armour += amount

    def reset_armour(self):

        self.armour = 0

    @property
    def alive(self):
        return self.hp > 0

    def __str__(self):
        return f"({self.name} HP: {self.hp} Mana: {self.mana} Armour: {self.armour} Effects: {self.effects})"

    def __repr__(self):
        return f"<Character {str(self)} >"

# Define Spells


class Effects:
    members = []

    def __init__(self):
        self.add_member(self)

    @classmethod
    def add_member(cls, new_member):
        cls.members.append(new_member)

    def __str__(self):
        return f"{self.effect.__name__}"

    def __repr__(self):
        return f"<Spell| {str(self)}>"


class Spell(Effects):
    members = []

    def __init__(self, cost, effect, duration, target_self):
        self.target_self = target_self
        self.cost = cost
        self.effect = effect
        self.duration = duration
        self.add_member(self)


class Modifier(Effects):
    members = []

    def __init__(self, effect):
        self.effect = effect
        self.duration = float('inf')
        self.add_member(self)


def magic_missile_effect(caster: Character, target: Character):
    target.receive_damage(4)


def drain_effect(caster: Character, target: Character):
    caster.heal(2)
    target.receive_damage(2)


def shield_effect(caster: Character, target: Character):
    caster.gain_armour(7)


# target and caster are swapped so when the effect is given to the opponent
# damage will be applied appropriately
def poison_effect(target: Character, caster: Character):
    target.receive_damage(3)


def recharge_effect(caster: Character, target: Character):
    caster.generate_mana(101)


def hard_mode_effect(caster: Character, target: Character):
    caster.receive_damage(1)


magic_missile = Spell(53, magic_missile_effect, 0, False)
drain = Spell(73, drain_effect, 0, False)
shield = Spell(113, shield_effect, 6, True)
poison = Spell(173, poison_effect, 6, False)
recharge = Spell(229, recharge_effect, 5, True)

hard_mode = Modifier(hard_mode_effect)


def score(path):
    if len(path) == 0:
        return float('inf')
    return sum(spell.cost for spell in path)


def dfs(player: Character, boss: Character, path=[], spell=None):
    # print('start', player.hp, boss.hp)

    if spell:
        if player.alive:
            player.cast_spell(spell, boss)
            path = [*path, spell]
        player.effects_tick(boss)
        boss.effects_tick(player)
        if boss.alive:
            boss.melee_attack(player)
        # print('end',player.hp, boss.hp)
        if player.hard_mode:
            player.hp -= 1
    if player.alive:
        player.reset_armour()
        player.effects_tick(boss)
        boss.effects_tick(player)

    if player.alive and boss.alive:
        choices = player.castable_spells(boss)
        if len(choices) == 0:
            player.hp = 0
    else:
        if player.alive:
            # print('player survived')
            # print(path)
            return path
        else:
            # print(player.alive, player.hp,boss.hp)
            return []
    best = []
    valid = False
    for next_spell in sorted(choices, key=lambda x: x.cost, reverse=True):
        # print([*path,spell],next_spell)
        new_player = Character(player.name, player.hp,
                               player.mana, player.attack, player.spell_list, player.armour, player.effects)
        new_player.hard_mode = player.hard_mode
        new_boss = Character(boss.name, boss.hp, boss.mana,
                             boss.attack, boss.spell_list, 0, boss.effects)
        new_path = dfs(new_player, new_boss, [
            *path] if spell else [], next_spell)
        if score(new_path) < score(best):
            # print(new_path)
            valid = True
            best = new_path
    return best


def part1():
    player = Character('player', 50, 500, 0, Spell.members)
    boss = Character('boss', 71, 500, 10, [])
    print(score(dfs(player, boss)))


def part2():
    player = Character('player', 50, 500, 0, Spell.members)
    player.hard_mode = True
    boss = Character('boss', 71, 500, 10, [])
    print(score(dfs(player, boss)))


part1()
part2()
